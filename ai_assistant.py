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
jsonformat = {"type": "json_object"}

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


def generate_story_outline(prompt):
    messages = [{"role": "system", "content": [{"text": "You are creating an narrative outline for a children's storybook. You will follow the guidelines below perfectly. You will be provided the story details by the user in the example input below. You will return a json object containing the outline for each page using the template output provided below. \n\n# Guidelines\n- Create a general story outline, not to exceed 500 words\n- The outline will always contain 5 pages - no more no less\n- The outline should be for a **board book style** **kids short story**\n- The outline should incorporate all of the elements provided by the user **cohesively**\n- Ensure the outline is engaging and captures the essence of each story element\n- The outline should be much shorter in comparison to the final narrative which will a maximum of three sentences per page (NOTE: You are doing the OUTLINE, NOT the final narrative)\n\n# User Input Format and Provided Story Elements\nGenre: {genre} \nSetting: {setting}\r\nSupporting Character: {supporting_character}\r\nPlot Element: {plot_element}\r\nTheme: {theme}\r\nMagical Object: {magical_object}\r\nTone/Mood: {tone}\r\nStyle: {style}\r\nRecipient's Name: {recipient_name}\r\nRelation to Recipient: {relation}\r\nMain Character Description: {main_character_description}\n\n# Output JSON Template\n{ \"page1\": \"{page1_outline}\", \"page2\": \"{page2_outline}\", \"page3\": \"{page3_outline}\", \"page4\": \"{page4_outline}\", \"page5\": \"{page5_outline}\" }\n\r\n\r\n", "type": "text"}]}, {"role": "user", "content": [{"type": "text", "text": "Genre: Magical Fantasy \r\nSetting: Enchanted Forest\r\nSupporting Character: Wise Owl\r\nPlot Element: A Magic Spell\r\nTheme: Courage\r\nMagical Object: Magic Wand\r\nTone/Mood: Enchanting\r\nStyle: Dr. Seuss (The Cat in the Hat)\r\nRecipient's Name: Alice\r\nRelation to Recipient: Niece\r\nMain Character Description: A brave and curious girl who loves exploring the unknown."}]}, {"role": "assistant", "content": [{"type": "text", "text": "{\r\n  \"page1\": \"Alice, a brave and curious girl, enters the Enchanted Forest with her Magic Wand in hand, seeking adventure.\",\r\n  \"page2\": \"She meets Wise Owl, who tells her about a Magic Spell that can save the forest from darkness.\",\r\n  \"page3\": \"Together, they search for the spell, overcoming obstacles and demonstrating Courage.\",\r\n  \"page4\": \"Alice uses the Magic Wand to cast the spell, restoring light and joy to the Enchanted Forest.\",\r\n  \"page5\": \"The forest celebrates Alice's bravery, and she learns the true power of courage and friendship.\"\r\n}\r\n"}]}, {"role": "user", "content": [{"type": "text", "text": "Genre: Space Exploration \r\nSetting: Outer Space\r\nSupporting Character: Talking Robot\r\nPlot Element: A Lost Map\r\nTheme: Discovery\r\nMagical Object: Flying Carpet\r\nTone/Mood: Adventurous\r\nStyle: Maurice Sendak (Where the Wild Things Are)\r\nRecipient's Name: Ethan\r\nRelation to Recipient: Son\r\nMain Character Description: An imaginative boy fascinated by the stars and galaxies.\r\n"}]}, {"role": "assistant", "content": [{"type": "text", "text": "{\r\n  \"page1\": \"Ethan, an imaginative boy, blasts off to Outer Space with his Flying Carpet and Talking Robot companion.\",\r\n  \"page2\": \"They find a Lost Map that leads to a hidden planet filled with ancient treasures.\",\r\n  \"page3\": \"Guided by the map, they embark on an adventurous journey through the stars.\",\r\n  \"page4\": \"Ethan and the robot face challenges but discover incredible wonders, embodying the theme of Discovery.\",\r\n  \"page5\": \"They return home with newfound knowledge, inspired by the endless possibilities of space.\"\r\n}\r\n"}]}, {"role": "user", "content": [{"type": "text", "text": "Genre: Fairy Tale \r\nSetting: Kingdom\r\nSupporting Character: Friendly Dragon\r\nPlot Element: A Grand Festival\r\nTheme: Friendship\r\nMagical Object: Golden Key\r\nTone/Mood: Whimsical\r\nStyle: Beatrix Potter (The Tale of Peter Rabbit)\r\nRecipient's Name: Lily\r\nRelation to Recipient: Daughter\r\nMain Character Description: A kind-hearted girl who dreams of magical adventures.\r\n"}]}, {"role": "assistant", "content": [{"type": "text", "text": "{\r\n  \"page1\": \"Lily, a kind-hearted girl, dreams of magical adventures in her Kingdom.\",\r\n  \"page2\": \"She befriends a Friendly Dragon who tells her about a Grand Festival in the kingdom.\",\r\n  \"page3\": \"Lily and the dragon set out to find a Golden Key needed to attend the festival.\",\r\n  \"page4\": \"They face whimsical challenges and learn the importance of Friendship along the way.\",\r\n  \"page5\": \"They find the key, attend the festival, and celebrate their new friendship, making Lily's dreams come true.\"\r\n}\r\n"}]}, {"role": "user", "content": [{"type": "text", "text": "Genre: Detective Story \r\nSetting: Secret Laboratory\r\nSupporting Character: Clever Fox\r\nPlot Element: A Mysterious Letter\r\nTheme: Curiosity\r\nMagical Object: Mystic Orb\r\nTone/Mood: Suspenseful\r\nStyle: Shel Silverstein (Where the Sidewalk Ends)\r\nRecipient's Name: Jack\r\nRelation to Recipient: Nephew\r\nMain Character Description: A quick-witted boy with a knack for solving mysteries."}]}, {"role": "assistant", "content": [{"type": "text", "text": "{\r\n  \"page1\": \"Jack, a quick-witted boy, explores a Secret Laboratory with his Clever Fox companion.\",\r\n  \"page2\": \"They discover a Mysterious Letter hinting at a hidden invention.\",\r\n  \"page3\": \"Intrigued, Jack and the fox solve puzzles and face suspenseful challenges to find the invention.\",\r\n  \"page4\": \"They uncover the Mystic Orb, the key to the invention, demonstrating Curiosity and determination.\",\r\n  \"page5\": \"Jack and the fox successfully reveal the invention, showcasing their cleverness and curiosity.\"\r\n}"}]}, {"role": "user", "content": [{"type": "text", "text": "Genre: Underwater Adventure \r\nSetting: Under the Sea\r\nSupporting Character: Playful Dolphin\r\nPlot Element: A Hidden Treasure\r\nTheme: Teamwork\r\nMagical Object: Mermaid’s Pearl\r\nTone/Mood: Joyful\r\nStyle: Eric Carle (The Very Hungry Caterpillar)\r\nRecipient's Name: Mia\r\nRelation to Recipient: Granddaughter\r\nMain Character Description: An adventurous girl who loves the ocean and its mysteries."}]}, {"role": "assistant", "content": [{"type": "text", "text": "{\r\n  \"page1\": \"Mia, an adventurous girl, dives Under the Sea with her Playful Dolphin friend.\",\r\n  \"page2\": \"They hear about a Hidden Treasure guarded by mermaids.\",\r\n  \"page3\": \"With the Mermaid’s Pearl, they navigate through underwater caves and coral reefs.\",\r\n  \"page4\": \"Mia and the dolphin work together, embodying the theme of Teamwork, to find the treasure.\",\r\n  \"page5\": \"They uncover the treasure and celebrate their joyful and exciting underwater adventure.\"\r\n}"}]}, {"role": "user", "content": [{"type": "text", "text": "Genre: Space Exploration \nSetting: Space Station\nSupporting Character: Talking Robot\nPlot Element: A Mysterious Stranger\nTheme: Discovery\nMagical Object: Mystic Orb\nTone/Mood: Mysterious\nStyle: Dr. Seuss (The Cat in the Hat)\nRecipient's Name: Mia\nRelation to Recipient: Daughter\nMain Character Description: A curious and intelligent girl fascinated by the stars."}]}, {"role": "assistant", "content": [{"type": "text", "text": "{\n  \"page1\": \"Mia, a curious and intelligent girl, explores a Space Station with her Talking Robot companion, ready for a new adventure.\",\n  \"page2\": \"They encounter a Mysterious Stranger who introduces them to the legend of the Mystic Orb.\",\n  \"page3\": \"Guided by clues, Mia and the robot search through the space station in a mysterious quest for the orb.\",\n  \"page4\": \"As they uncover the secrets of the orb, Mia realizes the true essence of Discovery and the power it holds.\",\n  \"page5\": \"With the orb in their possession, Mia and the robot embark on a journey beyond the stars, filled with wonder and excitement.\"\n}"}]}, {"role": "user", "content": [{"type": "text", "text": f"{prompt}"}]}]
    response = client.chat.completions.create(model="gpt-3.5-turbo", response_format=jsonformat, messages=messages, temperature=0.98, max_tokens=4095, top_p=1, frequency_penalty=0, presence_penalty=0)
    content = response.choices[0].message.content
    outline = json.loads(content)
    return outline




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