
# Prompt templates
prompt_template_step1 = """
Genre: {genre}
Setting: {setting}
Supporting Character: {supporting_character}
Plot Element: {plot_element}
Theme: {theme}
Magical Object: {magical_object}
Tone/Mood: {tone}
Recipient's Name: {recipient_name}
Relation to Recipient: {relation}
Main Character Description: {main_character_description}

Based on the above elements, create the following:
   
1. A detailed outline for a 5-page short story. Each page should have a brief narrative (no longer than 3 sentences).
2. A description of the main character based on the uploaded image and the relation to the recipient.
3. A title for the short story that reflects the narrative and the recipient's name.

Please ensure that the outline is engaging and captures the essence of each story element.
"""

prompt_template_step2 = """
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

# Function to generate DALL-E images based on descriptions
def generate_dalle_images(image_descriptions):
    dalle_images = []
    for description in image_descriptions:
        response = openai.Image.create(
            prompt=description,
            n=1,
            size="1024x1024"
        )
        dalle_images.append(response['data'][0]['url'])
    return dalle_images
