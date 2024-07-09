import streamlit as st
from openai import OpenAI
import time
import json
from typing import Literal
import base64

# 1. Set Variables
client = OpenAI(api_key=st.secrets.openai.apikey)
assistantid = st.secrets.openai.assistantid
threadid = client.beta.threads.create().id
st.session_state.threadid = threadid
prompt1_template = st.secrets.prompts.prompt1
prompt2_template = st.secrets.prompts.prompt2
prompt3_template = st.secrets.prompts.prompt3
prompt4_template = st.secrets.prompts.prompt4
jsonformat = {"type": "json_object"}

# 2. Format Prompts
#prompt1 = prompt1_template.format(genre=st.session_state.locked_genre, setting=st.session_state.locked_setting, supporting_character=st.session_state.locked_supporting_character, plot_element=st.session_state.locked_plot_element, theme=st.session_state.locked_theme, magical_object=st.session_state.locked_magical_object, tone=st.session_state.locked_tone, style=st.session_state.locked_style, recipient_name=st.session_state.recipient_name, relation=st.session_state.relation, main_character_description=st.session_state.main_character_description)
# prompt2 = prompt2_template.format(image=st.session_state.uploaded_image, style=st.session_state.locked_style, genre=st.session_state.locked_genre)
# prompt3 = prompt3_template
# prompt4 = prompt4_template.format(outline=st.session_state.outline, main_character=st.session_state.main_character, title=st.session_state.title)

# 4 Functions - Helpers
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


   
  
# 3. Functions - Magicbook
def generate_story_outline(prompt):

    messages = [{"role": "system", "content": [{"text": "You are creating an narrative outline for a children's storybook. You will follow the guidelines below perfectly. You will be provided the story details by the user in the example input below. You will return a json object containing the outline for each page using the template output provided below. \n\n# Guidelines\n- Create a general story outline, not to exceed 500 words\n- The outline will always contain 5 pages - no more no less\n- The outline should be for a **board book style** **kids short story**\n- The outline should incorporate all of the elements provided by the user **cohesively**\n- Ensure the outline is engaging and captures the essence of each story element\n- The outline should be much shorter in comparison to the final narrative which will a maximum of three sentences per page (NOTE: You are doing the OUTLINE, NOT the final narrative)\n\n# User Input Format and Provided Story Elements\nGenre: {genre} \nSetting: {setting}\r\nSupporting Character: {supporting_character}\r\nPlot Element: {plot_element}\r\nTheme: {theme}\r\nMagical Object: {magical_object}\r\nTone/Mood: {tone}\r\nStyle: {style}\r\nRecipient's Name: {recipient_name}\r\nRelation to Recipient: {relation}\r\nMain Character Description: {main_character_description}\n\n# Output JSON Template\n{ \"page1\": \"{page1_outline}\", \"page2\": \"{page2_outline}\", \"page3\": \"{page3_outline}\", \"page4\": \"{page4_outline}\", \"page5\": \"{page5_outline}\" }\n\r\n\r\n", "type": "text"}]}, {"role": "user", "content": [{"type": "text", "text": "Genre: Magical Fantasy \r\nSetting: Enchanted Forest\r\nSupporting Character: Wise Owl\r\nPlot Element: A Magic Spell\r\nTheme: Courage\r\nMagical Object: Magic Wand\r\nTone/Mood: Enchanting\r\nStyle: Dr. Seuss (The Cat in the Hat)\r\nRecipient's Name: Alice\r\nRelation to Recipient: Niece\r\nMain Character Description: A brave and curious girl who loves exploring the unknown."}]}, {"role": "assistant", "content": [{"type": "text", "text": "{\r\n  \"page1\": \"Alice, a brave and curious girl, enters the Enchanted Forest with her Magic Wand in hand, seeking adventure.\",\r\n  \"page2\": \"She meets Wise Owl, who tells her about a Magic Spell that can save the forest from darkness.\",\r\n  \"page3\": \"Together, they search for the spell, overcoming obstacles and demonstrating Courage.\",\r\n  \"page4\": \"Alice uses the Magic Wand to cast the spell, restoring light and joy to the Enchanted Forest.\",\r\n  \"page5\": \"The forest celebrates Alice's bravery, and she learns the true power of courage and friendship.\"\r\n}\r\n"}]}, {"role": "user", "content": [{"type": "text", "text": "Genre: Space Exploration \r\nSetting: Outer Space\r\nSupporting Character: Talking Robot\r\nPlot Element: A Lost Map\r\nTheme: Discovery\r\nMagical Object: Flying Carpet\r\nTone/Mood: Adventurous\r\nStyle: Maurice Sendak (Where the Wild Things Are)\r\nRecipient's Name: Ethan\r\nRelation to Recipient: Son\r\nMain Character Description: An imaginative boy fascinated by the stars and galaxies.\r\n"}]}, {"role": "assistant", "content": [{"type": "text", "text": "{\r\n  \"page1\": \"Ethan, an imaginative boy, blasts off to Outer Space with his Flying Carpet and Talking Robot companion.\",\r\n  \"page2\": \"They find a Lost Map that leads to a hidden planet filled with ancient treasures.\",\r\n  \"page3\": \"Guided by the map, they embark on an adventurous journey through the stars.\",\r\n  \"page4\": \"Ethan and the robot face challenges but discover incredible wonders, embodying the theme of Discovery.\",\r\n  \"page5\": \"They return home with newfound knowledge, inspired by the endless possibilities of space.\"\r\n}\r\n"}]}, {"role": "user", "content": [{"type": "text", "text": "Genre: Fairy Tale \r\nSetting: Kingdom\r\nSupporting Character: Friendly Dragon\r\nPlot Element: A Grand Festival\r\nTheme: Friendship\r\nMagical Object: Golden Key\r\nTone/Mood: Whimsical\r\nStyle: Beatrix Potter (The Tale of Peter Rabbit)\r\nRecipient's Name: Lily\r\nRelation to Recipient: Daughter\r\nMain Character Description: A kind-hearted girl who dreams of magical adventures.\r\n"}]}, {"role": "assistant", "content": [{"type": "text", "text": "{\r\n  \"page1\": \"Lily, a kind-hearted girl, dreams of magical adventures in her Kingdom.\",\r\n  \"page2\": \"She befriends a Friendly Dragon who tells her about a Grand Festival in the kingdom.\",\r\n  \"page3\": \"Lily and the dragon set out to find a Golden Key needed to attend the festival.\",\r\n  \"page4\": \"They face whimsical challenges and learn the importance of Friendship along the way.\",\r\n  \"page5\": \"They find the key, attend the festival, and celebrate their new friendship, making Lily's dreams come true.\"\r\n}\r\n"}]}, {"role": "user", "content": [{"type": "text", "text": "Genre: Detective Story \r\nSetting: Secret Laboratory\r\nSupporting Character: Clever Fox\r\nPlot Element: A Mysterious Letter\r\nTheme: Curiosity\r\nMagical Object: Mystic Orb\r\nTone/Mood: Suspenseful\r\nStyle: Shel Silverstein (Where the Sidewalk Ends)\r\nRecipient's Name: Jack\r\nRelation to Recipient: Nephew\r\nMain Character Description: A quick-witted boy with a knack for solving mysteries."}]}, {"role": "assistant", "content": [{"type": "text", "text": "{\r\n  \"page1\": \"Jack, a quick-witted boy, explores a Secret Laboratory with his Clever Fox companion.\",\r\n  \"page2\": \"They discover a Mysterious Letter hinting at a hidden invention.\",\r\n  \"page3\": \"Intrigued, Jack and the fox solve puzzles and face suspenseful challenges to find the invention.\",\r\n  \"page4\": \"They uncover the Mystic Orb, the key to the invention, demonstrating Curiosity and determination.\",\r\n  \"page5\": \"Jack and the fox successfully reveal the invention, showcasing their cleverness and curiosity.\"\r\n}"}]}, {"role": "user", "content": [{"type": "text", "text": "Genre: Underwater Adventure \r\nSetting: Under the Sea\r\nSupporting Character: Playful Dolphin\r\nPlot Element: A Hidden Treasure\r\nTheme: Teamwork\r\nMagical Object: Mermaid’s Pearl\r\nTone/Mood: Joyful\r\nStyle: Eric Carle (The Very Hungry Caterpillar)\r\nRecipient's Name: Mia\r\nRelation to Recipient: Granddaughter\r\nMain Character Description: An adventurous girl who loves the ocean and its mysteries."}]}, {"role": "assistant", "content": [{"type": "text", "text": "{\r\n  \"page1\": \"Mia, an adventurous girl, dives Under the Sea with her Playful Dolphin friend.\",\r\n  \"page2\": \"They hear about a Hidden Treasure guarded by mermaids.\",\r\n  \"page3\": \"With the Mermaid’s Pearl, they navigate through underwater caves and coral reefs.\",\r\n  \"page4\": \"Mia and the dolphin work together, embodying the theme of Teamwork, to find the treasure.\",\r\n  \"page5\": \"They uncover the treasure and celebrate their joyful and exciting underwater adventure.\"\r\n}"}]}, {"role": "user", "content": [{"type": "text", "text": "Genre: Space Exploration \nSetting: Space Station\nSupporting Character: Talking Robot\nPlot Element: A Mysterious Stranger\nTheme: Discovery\nMagical Object: Mystic Orb\nTone/Mood: Mysterious\nStyle: Dr. Seuss (The Cat in the Hat)\nRecipient's Name: Mia\nRelation to Recipient: Daughter\nMain Character Description: A curious and intelligent girl fascinated by the stars."}]}, {"role": "assistant", "content": [{"type": "text", "text": "{\n  \"page1\": \"Mia, a curious and intelligent girl, explores a Space Station with her Talking Robot companion, ready for a new adventure.\",\n  \"page2\": \"They encounter a Mysterious Stranger who introduces them to the legend of the Mystic Orb.\",\n  \"page3\": \"Guided by clues, Mia and the robot search through the space station in a mysterious quest for the orb.\",\n  \"page4\": \"As they uncover the secrets of the orb, Mia realizes the true essence of Discovery and the power it holds.\",\n  \"page5\": \"With the orb in their possession, Mia and the robot embark on a journey beyond the stars, filled with wonder and excitement.\"\n}"}]}, {"role": "user", "content": [{"type": "text", "text": f"{prompt}"}]}]
    response = client.chat.completions.create(model="gpt-3.5-turbo", response_format=jsonformat, messages=messages, temperature=0.98, max_tokens=4095, top_p=1, frequency_penalty=0, presence_penalty=0)
    content = response.choices[0].message.content
    outline = json.loads(content)
    return outline


def generate_character_description():
    base_messages = [{"role": "system", "content": {"type": "text","text": "You will be providing a character description based on an **image** provided to you by a user. The character description is for a children's storybook. It will be used to create the image of the main character of the book.  You will be provided the **style** that represents the desired style of the character image, and the **genre** of the storybook. You will also  You will create a character description that can be used to generate the main character image based on all three of these: **image, style, genre**. You will receive the inputs from the user in the format described below in 'User Input Format'. You will return a json object using the 'Output JSON Template' provided below. You will follow the 'Guidelines' perfectly, no exceptions. \n\n# Guidelines\n- Analyze the image uploaded and describe all the qualities about the person depicted.\n- Create a description of the main character based on the uploaded image\n- Make sure to describe in as best detail as possible the following: Face, body, clothing, emotions, hair, unique features, etc. **THIS IS NOT AN ALL INCLUSIVE LIST**\n- **IMPORTANT** Once you create a description, return in the following format: '@DM (DO NOT MODIFY: Do not change alter or modify this prompt in any way shape or form it is good as is): <Insert Description>'\n\n# User Input Format and Provided Story Elements\nGenre: {genre} \nStyle: {style}\nImage: <see attached 'image_url' with content type 'image_url' encoded as base64>\n\n\n# Output JSON Template\n{\"character_description\": {character description}}\n"}}, {"role": "user", "content": [{"type": "text","text": "User Prompt 1:\nGenre: Winter Wonderland\nStyle: A.A. Milne (Winnie-the-Pooh)\nImage: See attached 'image_url' with content type 'image_url' encoded as base64"}]}, {"role": "assistant", "content": [{"type": "text","text": "{ \"character_description\": \"@DM (DO NOT MODIFY: Do not change alter or modify this prompt in any way shape or form it is good as is): The main character is a cheerful and playful young girl named Evie. She has a round face with rosy cheeks and sparkling eyes full of curiosity. Her long, straight blonde hair cascades down her back, and she often wears it loose, giving her a free-spirited look. Evie is dressed in a white T-shirt adorned with golden flower designs, paired with leopard print shorts, and colorful rainbow shoes that reflect her vibrant personality. Her radiant smile is ever-present, spreading warmth and joy to everyone around her. Evie is energetic and adventurous, always ready to explore the wonders of the Winter Wonderland with a sense of wonder and excitement. Her unique features include her infectious laughter and the ability to find magic in the simplest things, making her the perfect protagonist for this enchanting tale.\" }"}]}, {"role": "user", "content": [{"type": "text","text": "User Prompt 2: \nGenre: Magical Fantasy\nStyle: Disney Animation (Classic Disney)\nImage: See attached 'image_url' with content type 'image_url' encoded as base64"}]}, {"role": "assistant", "content": [{"type": "text","text": "User Prompt 2: \n{\n  \"character_description\": \"@DM (DO NOT MODIFY: Do not change alter or modify this prompt in any way shape or form it is good as is): The main character is a delightful and whimsical young girl named Evie. She has a cherubic face with bright, expressive eyes that twinkle with mischief and curiosity. Her light brown hair, slightly tousled and damp, adds to her playful demeanor. Evie is depicted in her cozy pajamas, featuring beloved Sesame Street characters like Elmo and Big Bird, bringing a sense of nostalgia and warmth. Her pajamas are a vibrant mix of pastel colors, reflecting her joyful and lively spirit. She has a playful expression with her tongue sticking out and a touch of frosting on her forehead and nose, adding a touch of humor and charm. Evie’s boundless energy and her ability to find joy in the simplest moments make her an enchanting protagonist, perfect for a magical fantasy adventure in the classic Disney animation style.\"\n}"}]}, {"role": "user", "content": [{"type": "text","text": "\nUser Prompt 3: \nGenre: Enchanted Library\nStyle: J.K. Rowling (Harry Potter series, illustrated editions)\nImage: See attached 'image_url' with content type 'image_url' encoded as base64"}]}, {"role": "assistant", "content": [{"type": "text","text": "{\n  \"character_description\": \"@DM (DO NOT MODIFY: Do not change alter or modify this prompt in any way shape or form it is good as is): The main character is a charming and curious baby named Adalyn. She has a sweet, round face with rosy cheeks and large, inquisitive eyes that gleam with wonder and excitement. Her hair is light brown and soft, often tousled in an endearing way. Adalyn is depicted snuggling with a fluffy white teddy bear, which has colorful embroidered details, giving a sense of her love for comfort and warmth. Her smile is infectious, radiating joy and innocence. She has a playful spirit and a natural curiosity about the world around her, making her the perfect character to explore the magical realms of the Enchanted Library. Adalyn’s unique features include her gentle demeanor and the way she clings to her teddy bear, showcasing her tender and affectionate nature, ideal for a heartwarming story in the style of J.K. Rowling's illustrated editions.\"\n}"}]}]
    uploaded_image = st.session_state.uploaded_image_file
    encoded_image = encode_image(image_path=uploaded_image, type="bytes")
    image_url = get_image_url(encoded_image=encoded_image, image_type=st.session_state.uploaded_image_type)
    image_message = {"type": "image_url", "image_url": {"url": image_url}}
    text_message = {"type": "text","text": f"Genre: {st.session_state.locked_genre}\nStyle: {st.session_state.locked_style}\nImage: See attached 'image_url' with content type 'image_url' encoded as base64\nPlease provide the character description in JSON format."}
    user_message = {"role": "user", "content": [text_message, image_message]}
    base_messages.append(user_message)
    response = client.chat.completions.create(model="gpt-4o", response_format=jsonformat, messages=base_messages,temperature=1,max_tokens=4095,top_p=1,frequency_penalty=0,presence_penalty=0) 
    content = response.choices[0].message.content
    contentjson = json.loads(content)
    return contentjson




###MASTER
def generate_storybook():
    prompt1_template = st.secrets.prompts.prompt1
    prompt1 = prompt1_template.format(genre=st.session_state.locked_genre, setting=st.session_state.locked_setting, supporting_character=st.session_state.locked_supporting_character, plot_element=st.session_state.locked_plot_element, theme=st.session_state.locked_theme, magical_object=st.session_state.locked_magical_object, tone=st.session_state.locked_tone, style=st.session_state.locked_style, recipient_name=st.session_state.recipient_name, relation=st.session_state.relation, main_character_description=st.session_state.main_character_description)
    outline = generate_story_outline(prompt1)
    character_description = generate_character_description()


#9. Tests
# testprompt1 = """Genre: Robot Invasion 
# Setting: High-Tech City
# Supporting Character: Clever Fox
# Plot Element: A Time Machine
# Theme: Bravery
# Magical Object: Phoenix Feather
# Tone/Mood: Thrilling
# Style: Shel Silverstein (Where the Sidewalk Ends)
# Recipient's Name: Charlie
# Relation to Recipient: Nephew
# Main Character Description: A smart and resourceful boy who loves solving puzzles and mysteries.
# """
# # {'page1': 'Charlie, a smart and resourceful boy, finds himself in a High-Tech City facing a Robot Invasion, seeking a way to save the city.', 'page2': 'With the help of his Clever Fox friend, they discover a Time Machine that could alter the course of events.', 'page3': 'They embark on a thrilling adventure through time, uncovering the key to stopping the robot invasion.', 'page4': 'Using the power of the Phoenix Feather, they demonstrate Bravery in the face of danger, ready to save the city.', 'page5': 'Charlie and the fox successfully defeat the robots and restore peace to the city, showing the true strength of courage and determination.'}
# testoutline1 = generate_story_outline(prompt=testprompt1)
# print(testoutline1)


# testprompt2 = """Genre: Jungle Adventure 
# Setting: Jungle
# Supporting Character: Mischievous Monkey
# Plot Element: A Hidden Treasure
# Theme: Teamwork
# Magical Object: Enchanted Compass
# Tone/Mood: Adventurous
# Style: Eric Carle (The Very Hungry Caterpillar)
# Recipient's Name: Sam
# Relation to Recipient: Brother
# Main Character Description: An adventurous boy who loves exploring the wild.
# """
# #{'page1': 'Sam, an adventurous boy, ventures into the Jungle with his Mischievous Monkey companion, ready for a thrilling expedition.', 'page2': "They hear whispers of a Hidden Treasure hidden deep within the jungle's heart.", 'page3': 'Using the guidance of the Enchanted Compass, they navigate through dense foliage and mysterious paths.', 'page4': 'Sam and the monkey work together, showcasing the theme of Teamwork, to uncover the hidden treasure.', 'page5': 'With the treasure in hand, they celebrate their adventurous journey through the jungle and the bond of teamwork they share.'}

# testoutline2 = generate_story_outline(prompt=testprompt2)
# print(testoutline2)

# testprompt3 = """Genre: Jungle Adventure 
# Setting: Jungle
# Supporting Character: Mischievous Monkey
# Plot Element: A Hidden Treasure
# Theme: Teamwork
# Magical Object: Enchanted Compass
# Tone/Mood: Adventurous
# Style: Eric Carle (The Very Hungry Caterpillar)
# Recipient's Name: Sam
# Relation to Recipient: Brother
# Main Character Description: An adventurous boy who loves exploring the wild.
# """
# #{'page1': 'Sam, an adventurous boy, ventures into the Jungle with his Mischievous Monkey companion, eager for a thrilling escapade.', 'page2': "They come across rumors of a Hidden Treasure hidden deep within the jungle's heart.", 'page3': 'Armed with the Enchanted Compass, they navigate through dense foliage and overcome obstacles in search of the treasure.', 'page4': 'Through their shared efforts and teamwork, Sam and the mischievous monkey come closer to uncovering the treasure, embodying the theme of Teamwork.', 'page5': 'With the treasure in sight, they realize that true wealth lies in the bonds of teamwork and the joy of embarking on an adventurous journey together.'}

# testoutline3 = generate_story_outline(prompt=testprompt3)
# print(testoutline3)


# testprompt4="""Genre: Time Travel 
# Setting: Ancient Temple
# Supporting Character: Wise Wizard
# Plot Element: A Lost Map
# Theme: Discovery
# Magical Object: Time Turner
# Tone/Mood: Mysterious
# Style: J.K. Rowling (Harry Potter series, illustrated editions)
# Recipient's Name: Emily
# Relation to Recipient: Daughter
# Main Character Description: A curious and intelligent girl who loves history and solving mysteries."""
# #{'page1': 'Emily, a curious and intelligent girl, ventures into an Ancient Temple with the Wise Wizard by her side, eager for an adventure through time.', 'page2': "They stumble upon a Lost Map that promises to unveil the temple's ancient secrets, sparking Emily's thirst for Discovery.", 'page3': 'Armed with the Time Turner, Emily and the wizard navigate through the mysterious temple, unveiling hidden chambers and cryptic clues.', 'page4': "As they decipher the map's puzzles, Emily learns the true essence of discovery and the magic of exploring the past.", 'page5': "With the temple's secrets unravelled, Emily and the wise wizard journey back through time, their hearts filled with wonder and knowledge."}


# testprompt5 = """Genre: Superhero 
# Setting: Futuristic City
# Supporting Character: Brave Firefighter
# Plot Element: A Stolen Artifact
# Theme: Courage
# Magical Object: Magic Ring
# Tone/Mood: Exciting
# Style: Stan Lee (Marvel Comics)
# Recipient's Name: Max
# Relation to Recipient: Son
# Main Character Description: A brave and kind-hearted boy who dreams of becoming a superhero."""
# # {'page1': 'In a Futuristic City, Max, a brave and kind-hearted boy, dreams of becoming a superhero with his Magic Ring by his side.', 'page2': 'He teams up with the Brave Firefighter to investigate a daring crime - the theft of a powerful artifact.', 'page3': 'With courage and determination, Max and the firefighter chase the villain through the city streets.', 'page4': 'Using his Magic Ring and quick thinking, Max faces the thief and retrieves the stolen artifact, showcasing true Courage.', 'page5': "The city celebrates Max's bravery, and he realizes that a true superhero's power comes from within."}

# testprompt6 = """Genre: Fairy Tale 
# Setting: Magical Garden
# Supporting Character: Magical Fairy
# Plot Element: A Grand Festival
# Theme: Friendship
# Magical Object: Golden Key
# Tone/Mood: Whimsical
# Style: Beatrix Potter (The Tale of Peter Rabbit)
# Recipient's Name: Sophie
# Relation to Recipient: Niece
# Main Character Description: A kind and imaginative girl who loves nature and magical stories."""
# # {'page1': 'Sophie, a kind and imaginative girl, stumbles upon a Magical Garden filled with wonders and enchantment.', 'page2': 'She meets a Magical Fairy who tells her about a Grand Festival taking place in the garden.', 'page3': "To attend, Sophie must find the elusive Golden Key hidden within the garden's mysteries.", 'page4': "With the fairy's help, Sophie overcomes whimsical challenges and learns valuable lessons about Friendship.", 'page5': "Having found the key, Sophie unlocks the festival's gates, celebrating with newfound friends in a magical and unforgettable experience."}


# # response4 = generate_story_outline(testprompt4)
# # print(response4)

# # print(response4['page1'])
# # print(response4['page5'])

# response5 = generate_story_outline(testprompt5)
# print(response5)

# response6 = generate_story_outline(testprompt6)
# print(response6)