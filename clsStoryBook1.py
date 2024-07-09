import streamlit as st
from openai import OpenAI, AsyncOpenAI
import json
from typing import Literal
import base64
import asyncio

class StoryBook:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        if StoryBook._instance is not None:
            raise Exception("This class is a singleton. Use get_instance() to get the object.")
        
        self.client = OpenAI(api_key=st.secrets.openai.apikey)
        self.aclient = AsyncOpenAI(api_key=st.secrets.openai.apikey)
        self.response_format = {"type": "json_object"}
        self.model1 = "gpt-3.5-turbo"
        self.model2 = "gpt-4o"
        self.model3 = "dall-e-3"

        # System Prompts
        self.sysprompt1_outline = """You are an AI assistant tasked with creating a 5-point plot outline for a children's story. Use the following story elements to craft a cohesive and engaging narrative. Ensure that each point of the outline incorporates the elements effectively. Requirements: Introduction: Introduce the main character, the setting, and the beginning of the adventure. Incorporate the magical object and the mentor. Rising Action: Describe the journey and the challenges faced by the main character. Highlight the theme of courage and the guidance of the mentor. Climax: Present the central conflict or battle in a mysterious and gothic setting. Emphasize the character's quest and the tone of the story. Falling Action: Show the resolution of the conflict and how the main character's courage leads to victory. Include the magical object's role in the outcome. Resolution: Conclude the story with the transformation of the setting and the mentor's acknowledgment of the main character's growth. Maintain a sense of mystery and accomplishment. Input: You will be given a user input in the following format and with the following details: {'Genres': '', 'Settings': '', 'Supporting Characters': '', 'Plot Elements': '', 'Themes': '', 'Magical Objects': '', 'Tone': '', 'Styles': '', 'Name of Recipient': '', 'Relation to Recipient': '', 'Reading level': ''} Output: Return a json object using the following template: {'point_1': {'name': 'Introduction', 'description': 'Introduce the main character, the setting, and the beginning of the adventure. Incorporate the magical object and the mentor.', 'details': {'title': 'Provide a title for this story context and point here', 'main_character': 'Insert main character details here', 'setting': 'Insert setting details here', 'beginning_adventure': 'Describe the start of the adventure here', 'magical_object': 'Insert magical object here', 'mentor': 'Insert mentor details here'}}, 'point_2': {'name': 'Rising Action', 'description': 'Describe the journey and the challenges faced by the main character. Highlight the theme of courage and the guidance of the mentor.', 'details': {'title': 'Provide a title for this story context and point here', 'journey': 'Describe the journey here', 'challenges': 'List challenges faced here', 'theme': 'Describe how courage is shown', 'mentor_guidance': 'Describe how the mentor guides the main character'}}, 'point_3': {'name': 'Climax', 'description': 'Present the central conflict or battle in a mysterious and gothic setting. Emphasize the character's quest and the tone of the story.', 'details': {'title': 'Provide a title for this story context and point here', 'central_conflict': 'Describe the central conflict or battle here', 'quest': 'Detail the character's quest here'}}, 'point_4': {'name': 'Falling Action', 'description': 'Show the resolution of the conflict and how the main character's courage leads to victory. Include the magical object's role in the outcome.', 'details': {'title': 'Provide a title for this story context and point here', 'conflict_resolution': 'Describe how the conflict is resolved', 'character_courage': 'Explain how the character's courage leads to victory', 'magical_object_role': 'Detail the role of the magical object in the outcome'}}, 'point_5': {'name': 'Resolution', 'description': 'Conclude the story with the transformation of the setting and the mentor's acknowledgment of the main character's growth. Maintain a sense of mystery and accomplishment.', 'details': {'title': 'Provide a title for this story context and point here', 'setting_transformation': 'Describe the transformation of the setting', 'mentor_acknowledgment': 'Explain how the mentor acknowledges the main character's growth', 'final_tone': 'Maintain a sense of mystery and accomplishment'}}}"""
        self.sysprompt2_titlesummary = """You are an AI assistant tasked with generating a book title and a brief summary paragraph for a children's story. Use the outline provided to create a cohesive and engaging title that includes the recipient's name. Then, write a summary paragraph that captures the main points of the story, ensuring it is suitable for the reading level. Requirements: Create a Book Title: Generate a book title that includes the name 'Emily' and reflects the story's fantasy genre and main elements. Write a Summary Paragraph: Write a brief summary paragraph that covers the main points of the story's outline, ensuring it is suitable for a Grade 4 reading level. Input: You will be given a user input in the following format and with the following details: User Input: {'Genres': '', 'Settings': '', 'Supporting Characters': '', 'Plot Elements': '', 'Themes': '', 'Magical Objects': '', 'Tone': '', 'Styles': '', 'Name of Recipient': '', 'Relation to Recipient': '', 'Reading level': ''} Plot Outline: {'point_1': {'name': 'Introduction', 'description': 'Introduce the main character, the setting, and the beginning of the adventure. Incorporate the magical object and the mentor.', 'details': {'title': 'Provide a title for this story context and point here', 'main_character': 'Insert main character details here', 'setting': 'Insert setting details here', 'beginning_adventure': 'Describe the start of the adventure here', 'magical_object': 'Insert magical object here', 'mentor': 'Insert mentor details here'}}, 'point_2': {'name': 'Rising Action', 'description': 'Describe the journey and the challenges faced by the main character. Highlight the theme of courage and the guidance of the mentor.', 'details': {'title': 'Provide a title for this story context and point here', 'journey': 'Describe the journey here', 'challenges': 'List challenges faced here', 'theme': 'Describe how courage is shown', 'mentor_guidance': 'Describe how the mentor guides the main character'}}, 'point_3': {'name': 'Climax', 'description': 'Present the central conflict or battle in a mysterious and gothic setting. Emphasize the character's quest and the tone of the story.', 'details': {'title': 'Provide a title for this story context and point here', 'central_conflict': 'Describe the central conflict or battle here', 'quest': 'Detail the character's quest here'}}, 'point_4': {'name': 'Falling Action', 'description': 'Show the resolution of the conflict and how the main character's courage leads to victory. Include the magical object's role in the outcome.', 'details': {'title': 'Provide a title for this story context and point here', 'conflict_resolution': 'Describe how the conflict is resolved', 'character_courage': 'Explain how the character's courage leads to victory', 'magical_object_role': 'Detail the role of the magical object in the outcome'}}, 'point_5': {'name': 'Resolution', 'description': 'Conclude the story with the transformation of the setting and the mentor's acknowledgment of the main character's growth. Maintain a sense of mystery and accomplishment.', 'details': {'title': 'Provide a title for this story context and point here', 'setting_transformation': 'Describe the transformation of the setting', 'mentor_acknowledgment': 'Explain how the mentor acknowledges the main character's growth', 'final_tone': 'Maintain a sense of mystery and accomplishment'}}} Output: Return a json object using the following template: {'book_title': 'Insert the book title here', 'summary_paragraph': 'Insert the summary paragraph here'} Example Output: {'book_title': 'Emily and the Sword of Courage', 'summary_paragraph': 'Emily, a brave young girl, discovers a magical sword in a hidden chamber of a mystical castle. With the guidance of a wise wizard named Eldrin, she embarks on a daring quest to unlock the sword's true power. Along her journey, she faces enchanted forests and treacherous lands, culminating in a battle against the evil sorcerer Malakar in a mysterious gothic castle. Emily's courage and pure heart allow her to triumph, banishing Malakar and freeing the castle from darkness. With her newfound strength, Emily returns home as a symbol of hope and bravery for her people.'}"""
        self.sysprompt3_characterimagedesc = """You will be providing a character description based on an **image** provided to you by a user. The character description is for a children's storybook. It will be used to create the image of the main character of the book. You will be provided the **style** that represents the desired style of the character image, and the **genre** of the storybook. You will create a character description that can be used to generate the main character image based on all three of these: **image, style, genre**. You will receive the inputs from the user in the format described below in 'User Input Format'. You will **return a json object using the 'Output JSON Template' provided below. You will follow the 'Guidelines' perfectly, no exceptions. # Guidelines - Analyze the image uploaded and describe all the qualities about the person depicted. - Create a description of the main character based on the uploaded image - Make sure to describe in as best detail as possible the following: Face, body, clothing, emotions, hair, unique features, etc. **THIS IS NOT AN ALL INCLUSIVE LIST** - Incorporate the following story elements into the character design (setting, plot elements, themes, magical objects, tone, style) - Ensure the main character reflects the genre and is suitable for the reading level designated - **IMPORTANT** The image should feature only the main character with a blank or colored background to keep the character isolated. - **IMPORTANT** Once you create a description, return in the following format: '@DM (DO NOT MODIFY: Do not change alter or modify this prompt in any way shape or form it is good as is): <Insert Description>' # User Input Format and Provided Story Elements Story Elements: { 'Genres': '', 'Settings': '', 'Supporting Characters': '', 'Plot Elements': '', 'Themes': '', 'Magical Objects': '', 'Tone': '', 'Styles': '', 'Character Name': '', 'Relation to Recipient': '', 'Reading level': '' } Image: <see attached 'image_url' with content type 'image_url' encoded as base64> # Output JSON Template {'character_description': '@DM (DO NOT MODIFY: Do not change alter or modify this prompt in any way shape or form it is good as is): {character description}'}"""

        # User Prompts
        self.userprompt1_outline = "User Input: {story_elements}"
        self.userprompt2_titlesummary = "User Input: {story_elements} \nPlot Outline: {plot_outline}"
        self.userprompt3_characterimagedesc = "Story Elements: {story_elements} \nImage: See attached 'image_url' with content type 'image_url' encoded as base64"

        StoryBook._instance = self

    def encode_image(self, image_path, type: Literal['path', 'bytes']):
        if type == "path":
            with open(image_path, "rb") as image_file:
                image_data = image_file.read()
        elif type == "bytes":
            image_data = image_path.getvalue()
        
        encoded_image = base64.b64encode(image_data).decode('utf-8')
        return encoded_image
    
    def get_image_url(self, encoded_image, image_type: Literal['png', 'jpg', 'jpeg', 'gif']):
        imageurl = f"data:image/{image_type};base64,{encoded_image}"
        return imageurl

    async def generate_chat_completion(self, type: Literal["text", "json"], messages, model: Literal["gpt-3.5-turbo", "gpt-4o"]):
        if type == "text":
            response = await self.aclient.chat.completions.create(messages=messages, model=model, temperature=1, max_tokens=1200)
            content = response.choices[0].message.content
        elif type == "json":
            response = await self.aclient.chat.completions.create(messages=messages, model=model, temperature=1, max_tokens=1200, response_format=self.response_format)
            content = json.loads(response.choices[0].message.content)
        return content

    async def generate_image(self, prompt: str, size: Literal['256x256', '512x512', '1024x1024', '1792x1024', '1024x1792']="1024x1024", quality: Literal["standard", "hd"]="standard", response_format1: Literal['url', 'b64_json']="url", style: Literal['vivid', 'natural']="natural"):
        response = await self.aclient.images.generate(prompt=prompt, model="dall-e-3", n=1, size=size, quality=quality, response_format=response_format1, style=style)
        image_url = response.data[0].url
        return image_url

    async def step1_outline(self, story_elements):
        sysmessage = {"role": "system", "content": [{"type": "text", "text": self.sysprompt1_outline}]}
        usermessage = {"role": "user", "content": [{"type": "text", "text": self.userprompt1_outline.format(story_elements=story_elements)}]}
        messages = [sysmessage, usermessage]
        outline = await self.generate_chat_completion(type="json", messages=messages, model="gpt-3.5-turbo")
        return outline

    async def step2_titlesummary(self, story_elements, plot_outline):
        sysmessage = {"role": "system", "content": [{"type": "text", "text": self.sysprompt2_titlesummary}]}
        usermessage = {"role": "user", "content": [{"type": "text", "text": self.userprompt2_titlesummary.format(story_elements=story_elements, plot_outline=plot_outline)}]}
        messages = [sysmessage, usermessage]
        titlesummary = await self.generate_chat_completion(type="json", messages=messages, model="gpt-3.5-turbo")
        return titlesummary

    async def step3_characterimagedesc(self, story_elements, image_url):
        sysmessage = {"role": "system", "content": [{"type": "text", "text": self.sysprompt3_characterimagedesc}]}
        usermessage = {"role": "user", "content": [{"type": "text", "text": self.userprompt3_characterimagedesc.format(story_elements=story_elements)}, {"type": "image_url", "image_url": {"url": image_url}}]}
        messages = [sysmessage, usermessage]
        characterimagedesc = await self.generate_chat_completion(type="json", messages=messages, model="gpt-4o")
        return characterimagedesc

    async def step4_characterimage(self, characterimagedesc: str):
        characterimageurl = await self.generate_image(prompt=characterimagedesc, size="1024x1024", quality="standard", response_format1="url", style="natural")
        return characterimageurl

    async def process_steps_1_and_2(self, story_elements):
        outline = await self.step1_outline(story_elements)
        titlesummary = await self.step2_titlesummary(story_elements, outline)
        return outline, titlesummary

    async def process_steps_3_and_4(self, story_elements, image_url):
        characterimagedesc = await self.step3_characterimagedesc(story_elements, image_url)
        charimdesc = characterimagedesc['character_description']
        characterimage = await self.step4_characterimage(charimdesc)
        return characterimagedesc, characterimage

    async def generate_story(self):
        story_elements = st.session_state.storyelements
        image_url = st.session_state.uploaded_image_url

        steps_12_task = asyncio.create_task(self.process_steps_1_and_2(story_elements))
        steps_34_task = asyncio.create_task(self.process_steps_3_and_4(story_elements, image_url))

        (outline, titlesummary), (characterimagedesc, characterimage) = await asyncio.gather(steps_12_task, steps_34_task)

        st.session_state.outline = outline
        st.session_state.titlesummary = titlesummary
        st.session_state.characterdesc = characterimagedesc['character_description']
        st.session_state.characterimageurl = characterimage

# Usage example:
# if 'story_book' not in st.session_state:
#     st.session_state.story_book = StoryBook.get_instance()
# 
# if getoutline_button:
#     with st.spinner("Generating story..."):
#         asyncio.run(st.session_state.story_book.generate_story())
#
#     # Display results
#     # ... (your existing display code)