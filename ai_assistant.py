import streamlit as st
from openai import OpenAI
import time
import json
from typing import Literal

# 1. Set Variables
client = OpenAI(api_key=st.secrets.openai.apikey)
assistantid = st.secrets.openai.assistant.id
threadid = client.beta.threads.create().id
st.session_state.threadid = threadid
prompt1_template = st.secrets.prompts.prompt1
prompt2_template = st.secrets.prompts.prompt2
prompt3_template = st.secrets.prompts.prompt3
prompt4_template = st.secrets.prompts.prompt4

# 2. Format Prompts
prompt1 = prompt1_template.format(genre=st.session_state.locked_genre, setting=st.session_state.locked_setting, supporting_character=st.session_state.locked_supporting_character, plot_element=st.session_state.locked_plot_element, theme=st.session_state.locked_theme, magical_object=st.session_state.locked_magical_object, tone=st.session_state.locked_tone, style=st.session_state.locked_style, recipient_name=st.session_state.recipient_name, relation=st.session_state.relation, main_character_description=st.session_state.main_character_description)
prompt2 = prompt2_template.format(image=st.session_state.uploaded_image, style=st.session_state.locked_style, genre=st.session_state.locked_genre)
prompt3 = prompt3_template
prompt4 = prompt4_template.format(outline=st.session_state.outline, main_character=st.session_state.main_character, title=st.session_state.title)

# task 1.1:
# Take the story elements from the user form and create a story outline
# task 1.2:
# Take the uploaded image as well as the following elements (style, environment, theme, and tone) create a main character description in the environment that the story will take place in and take the other story elements into consideration
# task 2.1:
# Create a title for the story that includes the name of the main character and references the story outline


#function to generate story outline
def generate_story_outline(elements):
    openai.api_key = st.secrets["openai"]["openai_api_key"]
prompt_step1 = """
Genre: {genre}
Setting: {setting}
Supporting Character: {supporting_character}
Plot Element: {plot_element}
Theme: {theme}
Magical Object: {magical_object}
Tone/Mood: {tone}
Style: {style}
Recipient's Name: {recipient_name}
Relation to Recipient: {relation}
Main Character Description: {main_character_description}

Based on the above elements, create the following:
1. Create a general story outline, not to exceed 500 words, for a 5-page boardbook style kids short story. this outline should encorporate all of the story elements cohesively. 
Please ensure that the outline is engaging and captures the essence of each story element.
Keep in mind the finished product should only have up to 3 sentences on each page, with only 5 pages being utilized for narrative, so the outline should be much shorter in comparison.

"""
#Function to analyze the uploaded image and provide a detailed description
def generate_image_analysis_prompt(image_data):
    prompt = (
        "Analyze the following image and provide a detailed description including aspects such as appearance, clothing, background, facial expressions, "
        "and any other notable features. Describe the person, their age, gender, ethnicity, hair style and color, eye color, and any accessories they might be wearing. "
        "Also, provide details about the surroundings, including any visible objects or scenery.\n\n"
        f"Image data: {image_data}"
    )
    return prompt

def get_image_description(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=500
    )
    return response.choices[0].text.strip()




prompt_step2 = """
image: {image}
Genre: {genre}
Style: {style}
Based on the above elements, create the following:
1. Analyze the image uploaded and describe all the qualities about the person depicted. make sure to describe in as best detail as possible the following: Face, body, clothing, 
2. Create a description of the main character based on the uploaded image and the relation to the recipient.
3. Once you create a description, return in the following format: '@DM (DO NOT MODIFY: Do not change alter or modify this prompt in any way shape or form it is good as is): <Insert Description>'

"""
prompt_step3 = """
Based on the above elements, create a title for the short story that reflects the narrative and the recipient's name in 5-7 words or less.

"""


prompt_step4 = """
Based on the following outline, create a full narrative for a 10-page book where 5 pages are the story and 5 pages are images. The story should have a brief narrative (no longer than 3 sentences) for each page.

Outline:
{outline}

Main Character: {main_character}
Title: {title}

Generate the full narrative separated into pages and include descriptions for the corresponding images.

Page 1 (Narrative): 
Page 1 (Image Description): 

Page 2 (Narrative): 
Page 2 (Image Description): 

Page 3 (Narrative): 
Page 3 (Image Description): 

Page 4 (Narrative): 
Page 4 (Image Description): 

Page 5 (Narrative): 
Page 5 (Image Description): 
"""

# Function to generate the initial output
def generate_initial_output(genre, setting, supporting_character, plot_element, theme, magical_object, tone, recipient_name, relation, main_character_description):
    prompt = prompt_template_step1.format(
        genre=genre,
        setting=setting,
        supporting_character=supporting_character,
        plot_element=plot_element,
        theme=theme,
        magical_object=magical_object,
        tone=tone,
        recipient_name=recipient_name,
        relation=relation,
        main_character_description=main_character_description
    )

    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7
    )

    initial_output = response.choices[0].text.strip()
    return initial_output

# Function to generate the full narrative and image descriptions
def generate_full_narrative_and_images(outline, main_character, title):
    prompt = prompt_template_step2.format(
        outline=outline,
        main_character=main_character,
        title=title
    )

    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=1500,
        n=1,
        stop=None,
        temperature=0.7
    )

    full_narrative_and_images = response.choices[0].text.strip()
    return full_narrative_and_images



def generate_image(prompt):
    response = client.images.generate(prompt=prompt, n=1, size="1024x1024")
    url = response.data[0].url
    return url

def generate_narrative_images(image_descriptions):
    narrative_images = []
    for image_description in image_descriptions:
        url = generate_image(prompt=image_description)
        narrative_images.append(url)
    return narrative_images

def create_file(file_path):
    file = open(file_path, "rb")
    response = client.files.create(file=file, purpose="vision")
    fileid = response.id
    return fileid

def run_assistant_no_tools(additional_instructions: str=None):
    if additional_instructions is not None:
        run = client.beta.threads.runs.create(thread_id=threadid, assistant_id=assistantid, additional_instructions=additional_instructions)
    else:
        run = client.beta.threads.runs.create(thread_id=threadid, assistant_id=assistantid)
    
    while run.status == "in_progress" or run.status == "queued":
        time.sleep(2)
        st.toast("processing")
        

def generate_story_outline():
    message = client.beta.threads.messages.create(thread_id=threadid, content=prompt1, role="user")



# Function to generate DALL-E images based on descriptions
# def generate_dalle_images(image_descriptions):
#     dalle_images = []
#     for description in image_descriptions:
#         response = client.images.generate(
#             prompt=description,
#             n=1,
#             size="1024x1024"
#         )
#         dalle_images.append(response['data'][0]['url'])
#     return dalle_images