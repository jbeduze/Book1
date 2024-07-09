import streamlit as st
from openai import OpenAI
import time
import json
from typing import Literal
import base64


####### 0. Globals  ###########################################################
client = OpenAI(api_key=st.secrets.openai.apikey)
response_format = {"type": "json_object"}
model1 = "gpt-3.5-turbo"
model2 = "gpt-4o"
model3 = "dall-e-3"


####### 1. Prompts  ###########################################################
# 1A. System Prompts
sysprompt1_outline = """You are an AI assistant tasked with creating a 5-point plot outline for a children's story. Use the following story elements to craft a cohesive and engaging narrative. Ensure that each point of the outline incorporates the elements effectively. Requirements: Introduction: Introduce the main character, the setting, and the beginning of the adventure. Incorporate the magical object and the mentor. Rising Action: Describe the journey and the challenges faced by the main character. Highlight the theme of courage and the guidance of the mentor. Climax: Present the central conflict or battle in a mysterious and gothic setting. Emphasize the character's quest and the tone of the story. Falling Action: Show the resolution of the conflict and how the main character's courage leads to victory. Include the magical object's role in the outcome. Resolution: Conclude the story with the transformation of the setting and the mentor's acknowledgment of the main character's growth. Maintain a sense of mystery and accomplishment. Input: You will be given a user input in the following format and with the following details: {'Genres': '', 'Settings': '', 'Supporting Characters': '', 'Plot Elements': '', 'Themes': '', 'Magical Objects': '', 'Tone': '', 'Styles': '', 'Name of Recipient': '', 'Relation to Recipient': '', 'Reading level': ''} Output: Return a json object using the following template: {'point_1': {'name': 'Introduction', 'description': 'Introduce the main character, the setting, and the beginning of the adventure. Incorporate the magical object and the mentor.', 'details': {'title': 'Provide a title for this story context and point here', 'main_character': 'Insert main character details here', 'setting': 'Insert setting details here', 'beginning_adventure': 'Describe the start of the adventure here', 'magical_object': 'Insert magical object here', 'mentor': 'Insert mentor details here'}}, 'point_2': {'name': 'Rising Action', 'description': 'Describe the journey and the challenges faced by the main character. Highlight the theme of courage and the guidance of the mentor.', 'details': {'title': 'Provide a title for this story context and point here', 'journey': 'Describe the journey here', 'challenges': 'List challenges faced here', 'theme': 'Describe how courage is shown', 'mentor_guidance': 'Describe how the mentor guides the main character'}}, 'point_3': {'name': 'Climax', 'description': 'Present the central conflict or battle in a mysterious and gothic setting. Emphasize the character's quest and the tone of the story.', 'details': {'title': 'Provide a title for this story context and point here', 'central_conflict': 'Describe the central conflict or battle here', 'quest': 'Detail the character's quest here'}}, 'point_4': {'name': 'Falling Action', 'description': 'Show the resolution of the conflict and how the main character's courage leads to victory. Include the magical object's role in the outcome.', 'details': {'title': 'Provide a title for this story context and point here', 'conflict_resolution': 'Describe how the conflict is resolved', 'character_courage': 'Explain how the character's courage leads to victory', 'magical_object_role': 'Detail the role of the magical object in the outcome'}}, 'point_5': {'name': 'Resolution', 'description': 'Conclude the story with the transformation of the setting and the mentor's acknowledgment of the main character's growth. Maintain a sense of mystery and accomplishment.', 'details': {'title': 'Provide a title for this story context and point here', 'setting_transformation': 'Describe the transformation of the setting', 'mentor_acknowledgment': 'Explain how the mentor acknowledges the main character's growth', 'final_tone': 'Maintain a sense of mystery and accomplishment'}}}"""
sysprompt2_titlesummary = """You are an AI assistant tasked with generating a book title and a brief summary paragraph for a children's story. Use the outline provided to create a cohesive and engaging title that includes the recipient's name. Then, write a summary paragraph that captures the main points of the story, ensuring it is suitable for the reading level. Requirements: Create a Book Title: Generate a book title that includes the name 'Emily' and reflects the story's fantasy genre and main elements. Write a Summary Paragraph: Write a brief summary paragraph that covers the main points of the story's outline, ensuring it is suitable for a Grade 4 reading level. Input: You will be given a user input in the following format and with the following details: User Input: {'Genres': '', 'Settings': '', 'Supporting Characters': '', 'Plot Elements': '', 'Themes': '', 'Magical Objects': '', 'Tone': '', 'Styles': '', 'Name of Recipient': '', 'Relation to Recipient': '', 'Reading level': ''} Plot Outline: {'point_1': {'name': 'Introduction', 'description': 'Introduce the main character, the setting, and the beginning of the adventure. Incorporate the magical object and the mentor.', 'details': {'title': 'Provide a title for this story context and point here', 'main_character': 'Insert main character details here', 'setting': 'Insert setting details here', 'beginning_adventure': 'Describe the start of the adventure here', 'magical_object': 'Insert magical object here', 'mentor': 'Insert mentor details here'}}, 'point_2': {'name': 'Rising Action', 'description': 'Describe the journey and the challenges faced by the main character. Highlight the theme of courage and the guidance of the mentor.', 'details': {'title': 'Provide a title for this story context and point here', 'journey': 'Describe the journey here', 'challenges': 'List challenges faced here', 'theme': 'Describe how courage is shown', 'mentor_guidance': 'Describe how the mentor guides the main character'}}, 'point_3': {'name': 'Climax', 'description': 'Present the central conflict or battle in a mysterious and gothic setting. Emphasize the character's quest and the tone of the story.', 'details': {'title': 'Provide a title for this story context and point here', 'central_conflict': 'Describe the central conflict or battle here', 'quest': 'Detail the character's quest here'}}, 'point_4': {'name': 'Falling Action', 'description': 'Show the resolution of the conflict and how the main character's courage leads to victory. Include the magical object's role in the outcome.', 'details': {'title': 'Provide a title for this story context and point here', 'conflict_resolution': 'Describe how the conflict is resolved', 'character_courage': 'Explain how the character's courage leads to victory', 'magical_object_role': 'Detail the role of the magical object in the outcome'}}, 'point_5': {'name': 'Resolution', 'description': 'Conclude the story with the transformation of the setting and the mentor's acknowledgment of the main character's growth. Maintain a sense of mystery and accomplishment.', 'details': {'title': 'Provide a title for this story context and point here', 'setting_transformation': 'Describe the transformation of the setting', 'mentor_acknowledgment': 'Explain how the mentor acknowledges the main character's growth', 'final_tone': 'Maintain a sense of mystery and accomplishment'}}} Output: Return a json object using the following template: {'book_title': 'Insert the book title here', 'summary_paragraph': 'Insert the summary paragraph here'} Example Output: {'book_title': 'Emily and the Sword of Courage', 'summary_paragraph': 'Emily, a brave young girl, discovers a magical sword in a hidden chamber of a mystical castle. With the guidance of a wise wizard named Eldrin, she embarks on a daring quest to unlock the sword's true power. Along her journey, she faces enchanted forests and treacherous lands, culminating in a battle against the evil sorcerer Malakar in a mysterious gothic castle. Emily's courage and pure heart allow her to triumph, banishing Malakar and freeing the castle from darkness. With her newfound strength, Emily returns home as a symbol of hope and bravery for her people.'}"""
sysprompt3_characterimagedesc = """You will be providing a character description based on an **image** provided to you by a user. The character description is for a children's storybook. It will be used to create the image of the main character of the book. You will be provided the **style** that represents the desired style of the character image, and the **genre** of the storybook. You will create a character description that can be used to generate the main character image based on all three of these: **image, style, genre**. You will receive the inputs from the user in the format described below in 'User Input Format'. You will **return a json object using the 'Output JSON Template' provided below. You will follow the 'Guidelines' perfectly, no exceptions. # Guidelines - Analyze the image uploaded and describe all the qualities about the person depicted. - Create a description of the main character based on the uploaded image - Make sure to describe in as best detail as possible the following: Face, body, clothing, emotions, hair, unique features, etc. **THIS IS NOT AN ALL INCLUSIVE LIST** - Incorporate the following story elements into the character design (setting, plot elements, themes, magical objects, tone, style) - Ensure the main character reflects the genre and is suitable for the reading level designated - **IMPORTANT** The image should feature only the main character with a blank or colored background to keep the character isolated. - **IMPORTANT** Once you create a description, return in the following format: '@DM (DO NOT MODIFY: Do not change alter or modify this prompt in any way shape or form it is good as is): <Insert Description>' # User Input Format and Provided Story Elements Story Elements: { 'Genres': '', 'Settings': '', 'Supporting Characters': '', 'Plot Elements': '', 'Themes': '', 'Magical Objects': '', 'Tone': '', 'Styles': '', 'Character Name': '', 'Relation to Recipient': '', 'Reading level': '' } Image: <see attached 'image_url' with content type 'image_url' encoded as base64> # Output JSON Template {'character_description': '@DM (DO NOT MODIFY: Do not change alter or modify this prompt in any way shape or form it is good as is. Do not include any words, letters or text in the image. Only return the character on a solid color light or dark background.): {character description}'}"""

# 1B. User Prompts
userprompt1_outline = "User Input: {story_elements}"
userprompt2_titlesummary = "User Input: {story_elements} \nPlot Outline: {plot_outline}"
userprompt3_characterimagedesc = "Story Elements: {story_elements} \nImage: See attached 'image_url' with content type 'image_url' encoded as base64"


####### 2. UTILITIES  ###########################################################
def encode_image(image_path, type: Literal['path', 'bytes']):
    if type == "path":
        with open(image_path, "rb") as image_file:
            image_data = image_file.read()
    elif type == "bytes":
        image_data = image_path.getvalue()
    
    encoded_image = base64.b64encode(image_data).decode('utf-8')
    return encoded_image
  
def get_image_url(encoded_image, image_type: Literal['png', 'jpg', 'jpeg', 'gif']):
    imageurl = f"data:image/{image_type};base64,{encoded_image}"
    return imageurl

def generate_chat_completion(type: Literal["text", "json"], messages, model: Literal["gpt-3.5-turbo", "gpt-4o"]):
    if type == "text":
        response = client.chat.completions.create(messages=messages, model=model, temperature=1, max_tokens=1200)
        content = response.choices[0].message.content
    elif type == "json":
        response = client.chat.completions.create(messages=messages, model=model, temperature=1, max_tokens=1200, response_format=response_format)
        content = json.loads(response.choices[0].message.content)
    return content

def generate_image(prompt: str, size: Literal['256x256', '512x512', '1024x1024', '1792x1024', '1024x1792']="1024x1024", quality: Literal["standard", "hd"]="standard", response_format1: Literal['url', 'b64_json']="url", style: Literal['vivid', 'natural']="natural"):
    response = client.images.generate(prompt=prompt, model="dall-e-3", n=1, size=size, quality=quality, response_format=response_format1, style=style)
    image_url = response.data[0].url
    return image_url

####### 3. Functions  ###########################################################
def step1_outline(story_elements):
    sysmessage = {"role": "system", "content": [{"type": "text", "text": sysprompt1_outline}]}
    usermessage = {"role": "user", "content": [{"type": "text", "text": userprompt1_outline.format(story_elements=story_elements)}]}
    messages = [sysmessage, usermessage]
    outline = generate_chat_completion(type="json", messages=messages, model="gpt-3.5-turbo")
    return outline

def step2_titlesummary(story_elements, plot_outline):
    sysmessage = {"role": "system", "content": [{"type": "text", "text":sysprompt2_titlesummary}]}
    usermessage = {"role": "user", "content": [{"type": "text", "text": userprompt2_titlesummary.format(story_elements=story_elements, plot_outline=plot_outline)}]}
    messages = [sysmessage, usermessage]
    titlesummary = generate_chat_completion(type="json", messages=messages, model="gpt-3.5-turbo")
    # print(titlesummary)
    return titlesummary

def step3_characterimagedesc(story_elements, image_url):
    sysmessage = {"role": "system", "content": [{"type": "text", "text": sysprompt3_characterimagedesc}]}
    usermessage = {"role": "user", "content": [{"type": "text", "text": userprompt3_characterimagedesc.format(story_elements=story_elements)}, {"type": "image_url", "image_url": {"url": image_url}}]}
    messages = [sysmessage, usermessage]
    characterimagedesc = generate_chat_completion(type="json", messages=messages, model="gpt-4o")
    # print(characterimagedesc)
    return characterimagedesc

def step4_characterimage(characterimagedesc: str):
    characterimageurl = generate_image(prompt=characterimagedesc, size="1024x1024", quality="standard", response_format1="url", style="natural")
    # print(characterimageurl)
    return characterimageurl

def master():
    st.session_state.uploaded_encoded_image = encode_image(image_path=st.session_state.uploaded_image, type="bytes")
    st.session_state.uploaded_image_url = get_image_url(encoded_image=st.session_state.uploaded_encoded_image, image_type=st.session_state.uploaded_image_type)
    st.session_state.outline = step1_outline(story_elements=st.session_state.storyelements)
    print(st.session_state.outline)
    st.session_state.titlesummary = step2_titlesummary(story_elements=st.session_state.storyelements, plot_outline=st.session_state.outline)
    print(st.session_state.titlesummary)
    st.session_state.characterdesc = step3_characterimagedesc(story_elements=st.session_state.storyelements, image_url=st.session_state.uploaded_image_url)
    print(st.session_state.characterdesc)
    st.session_state.characterimageurl = step4_characterimage(characterimagedesc=st.session_state.characterdesc['character_description'])
    print(st.session_state.characterimageurl)

# def generate_character_description():
#     base_messages = [{"role": "system", "content": {"type": "text","text": "You will be providing a character description based on an **image** provided to you by a user. The character description is for a children's storybook. It will be used to create the image of the main character of the book.  You will be provided the **style** that represents the desired style of the character image, and the **genre** of the storybook. You will also  You will create a character description that can be used to generate the main character image based on all three of these: **image, style, genre**. You will receive the inputs from the user in the format described below in 'User Input Format'. You will return a json object using the 'Output JSON Template' provided below. You will follow the 'Guidelines' perfectly, no exceptions. \n\n# Guidelines\n- Analyze the image uploaded and describe all the qualities about the person depicted.\n- Create a description of the main character based on the uploaded image\n- Make sure to describe in as best detail as possible the following: Face, body, clothing, emotions, hair, unique features, etc. **THIS IS NOT AN ALL INCLUSIVE LIST**\n- **IMPORTANT** Once you create a description, return in the following format: '@DM (DO NOT MODIFY: Do not change alter or modify this prompt in any way shape or form it is good as is): <Insert Description>'\n\n# User Input Format and Provided Story Elements\nGenre: {genre} \nStyle: {style}\nImage: <see attached 'image_url' with content type 'image_url' encoded as base64>\n\n\n# Output JSON Template\n{\"character_description\": {character description}}\n"}}, {"role": "user", "content": [{"type": "text","text": "User Prompt 1:\nGenre: Winter Wonderland\nStyle: A.A. Milne (Winnie-the-Pooh)\nImage: See attached 'image_url' with content type 'image_url' encoded as base64"}]}, {"role": "assistant", "content": [{"type": "text","text": "{ \"character_description\": \"@DM (DO NOT MODIFY: Do not change alter or modify this prompt in any way shape or form it is good as is): The main character is a cheerful and playful young girl named Evie. She has a round face with rosy cheeks and sparkling eyes full of curiosity. Her long, straight blonde hair cascades down her back, and she often wears it loose, giving her a free-spirited look. Evie is dressed in a white T-shirt adorned with golden flower designs, paired with leopard print shorts, and colorful rainbow shoes that reflect her vibrant personality. Her radiant smile is ever-present, spreading warmth and joy to everyone around her. Evie is energetic and adventurous, always ready to explore the wonders of the Winter Wonderland with a sense of wonder and excitement. Her unique features include her infectious laughter and the ability to find magic in the simplest things, making her the perfect protagonist for this enchanting tale.\" }"}]}, {"role": "user", "content": [{"type": "text","text": "User Prompt 2: \nGenre: Magical Fantasy\nStyle: Disney Animation (Classic Disney)\nImage: See attached 'image_url' with content type 'image_url' encoded as base64"}]}, {"role": "assistant", "content": [{"type": "text","text": "User Prompt 2: \n{\n  \"character_description\": \"@DM (DO NOT MODIFY: Do not change alter or modify this prompt in any way shape or form it is good as is): The main character is a delightful and whimsical young girl named Evie. She has a cherubic face with bright, expressive eyes that twinkle with mischief and curiosity. Her light brown hair, slightly tousled and damp, adds to her playful demeanor. Evie is depicted in her cozy pajamas, featuring beloved Sesame Street characters like Elmo and Big Bird, bringing a sense of nostalgia and warmth. Her pajamas are a vibrant mix of pastel colors, reflecting her joyful and lively spirit. She has a playful expression with her tongue sticking out and a touch of frosting on her forehead and nose, adding a touch of humor and charm. Evie’s boundless energy and her ability to find joy in the simplest moments make her an enchanting protagonist, perfect for a magical fantasy adventure in the classic Disney animation style.\"\n}"}]}, {"role": "user", "content": [{"type": "text","text": "\nUser Prompt 3: \nGenre: Enchanted Library\nStyle: J.K. Rowling (Harry Potter series, illustrated editions)\nImage: See attached 'image_url' with content type 'image_url' encoded as base64"}]}, {"role": "assistant", "content": [{"type": "text","text": "{\n  \"character_description\": \"@DM (DO NOT MODIFY: Do not change alter or modify this prompt in any way shape or form it is good as is): The main character is a charming and curious baby named Adalyn. She has a sweet, round face with rosy cheeks and large, inquisitive eyes that gleam with wonder and excitement. Her hair is light brown and soft, often tousled in an endearing way. Adalyn is depicted snuggling with a fluffy white teddy bear, which has colorful embroidered details, giving a sense of her love for comfort and warmth. Her smile is infectious, radiating joy and innocence. She has a playful spirit and a natural curiosity about the world around her, making her the perfect character to explore the magical realms of the Enchanted Library. Adalyn’s unique features include her gentle demeanor and the way she clings to her teddy bear, showcasing her tender and affectionate nature, ideal for a heartwarming story in the style of J.K. Rowling's illustrated editions.\"\n}"}]}]
#     uploaded_image = st.session_state.uploaded_image_file
#     encoded_image = encode_image(image_path=uploaded_image, type="bytes")
#     image_url = get_image_url(encoded_image=encoded_image, image_type=st.session_state.uploaded_image_type)
#     image_message = {"type": "image_url", "image_url": {"url": image_url}}
#     text_message = {"type": "text","text": f"Genre: {st.session_state.locked_genre}\nStyle: {st.session_state.locked_style}\nImage: See attached 'image_url' with content type 'image_url' encoded as base64\nPlease provide the character description in JSON format."}
#     user_message = {"role": "user", "content": [text_message, image_message]}
#     base_messages.append(user_message)
#     response = client.chat.completions.create(model="gpt-4o", response_format=jsonformat, messages=base_messages,temperature=1,max_tokens=4095,top_p=1,frequency_penalty=0,presence_penalty=0) 
#     content = response.choices[0].message.content
#     contentjson = json.loads(content)
#     return contentjson
####### 1. SETUP  ###########################################################



####### 9. TESTS  ###########################################################

# input1 = {
#   "Genres": "Science Fiction",
#   "Settings": "Spaceship",
#   "Supporting Characters": "Robot",
#   "Plot Elements": "Exploration",
#   "Themes": "Friendship",
#   "Magical Objects": "Time Machine",
#   "Tone": "Suspenseful",
#   "Styles": "Futuristic",
#   "Name of Recipient": "Michael",
#   "Relation to Recipient": "Nephew",
#   "Reading level": "Grade 5"
# }

# input2 = {
#   "Genres": "Adventure",
#   "Settings": "Jungle",
#   "Supporting Characters": "Animal Guide",
#   "Plot Elements": "Treasure Hunt",
#   "Themes": "Perseverance",
#   "Magical Objects": "Amulet",
#   "Tone": "Exciting",
#   "Styles": "Naturalistic",
#   "Name of Recipient": "Lily",
#   "Relation to Recipient": "Daughter",
#   "Reading level": "Grade 3"
# }

# input3 = {
#   "Genres": "Mystery",
#   "Settings": "Old Mansion",
#   "Supporting Characters": "Detective",
#   "Plot Elements": "Investigation",
#   "Themes": "Truth",
#   "Magical Objects": "Crystal Ball",
#   "Tone": "Thrilling",
#   "Styles": "Victorian",
#   "Name of Recipient": "Sophia",
#   "Relation to Recipient": "Granddaughter",
#   "Reading level": "Grade 6"
# }
# input3 = {
#   "Genres": "Fairy Tale",
#   "Settings": "Enchanted Forest",
#   "Supporting Characters": "Kissy Monster",
#   "Plot Elements": "A Secret Door",
#   "Themes": "Adventure",
#   "Magical Objects": "Flying Carpet",
#   "Tone": "Whimsical",
#   "Styles": "Disney Animation (Classic Disney)",
#   "Character Name": "Everly",
#   "Relation to Recipient": "Daughter",
#   "Reading level": "2-year old"
# }
# input4 = {
#   "Genres": "Science Fiction",
#   "Settings": "Spaceship",
#   "Supporting Characters": "Robot",
#   "Plot Elements": "Exploration",
#   "Themes": "Friendship",
#   "Magical Objects": "Time Machine",
#   "Tone": "Suspenseful",
#   "Styles": "Futuristic",
#   "Character Name": "Everly", 
#   "Relation to Recipient": "Daughter", 
#   "Reading level": "PreSchool" 
# }
# image_path = "assets/images/examples/everly2.jpg"
# encoded_image = encode_image(image_path=image_path, type="path")
# image_url = get_image_url(encoded_image=encoded_image, image_type="jpg")
# outline = step1_outline(story_elements=input3)
# print(outline)
# titlesummary = step2_titlesummary(story_elements=input3, plot_outline=outline)
# print(titlesummary)
# characterimagedesc = step3_characterimagedesc(story_elements=input3, image_url=image_url)
# charimdesc = characterimagedesc['character_description']
# print(characterimagedesc)
# print(charimdesc)
# characterimage = step4_characterimage(characterimagedesc=charimdesc)
# print(characterimage)

# # outline = step1_outline(input1)
# # titlesummary = step2_titlesummary(input1, outline)