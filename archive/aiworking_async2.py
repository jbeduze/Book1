import asyncio
from typing import List, Literal
import base64
import streamlit as st
from openai import OpenAI
import time
import json


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


 
# Placeholder for the OpenAI client setup and image encoding functions
# Assuming these are similar to what you've provided before

class StoryBook:
    def __init__(self, title: str):
        self.title = title
        self.outline = None
        self.character_descriptions = []

    async def generate_outline(self, prompt: str) -> None:
        # Simulate an asynchronous operation, such as fetching data or processing
        await asyncio.sleep(2)  # Simulating a delay
        self.outline = f"Outline of the story: {prompt}"
        print(f"Outline generated: {self.outline}")

    async def generate_character_description(self, character_name: str) -> None:
        # Simulate an asynchronous operation, such as fetching data or processing
        await asyncio.sleep(2)  # Simulating a delay
        description = f"Description of character: {character_name}"
        self.character_descriptions.append(description)
        print(f"Character description generated: {description}")

    async def generate_story_details(self, prompt: str, character_names: List[str]) -> None:
        await self.generate_outline(prompt)
        await asyncio.gather(*(self.generate_character_description(name) for name in character_names))

# Example usage in the context of the Magicbook app
async def main():
    title = "The Adventure of Async"
    character_names = ["Alice", "Bob", "Charlie"]

    # Example values based on the previous context
    genre = "Magical Fantasy"
    setting = "Enchanted Forest"
    supporting_character = "Wise Owl"
    plot_element = "A Magic Spell"
    theme = "Courage"
    magical_object = "Magic Wand"
    tone = "Enchanting"
    style = "Dr. Seuss (The Cat in the Hat)"
    recipient_name = "Alice"
    relation = "Niece"
    main_character_description = "A brave and curious girl who loves exploring the unknown."

    # Generating the prompt based on the given values
    prompt = f"""
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
    """

    # Create the StoryBook instance and generate the story details
    story_book = StoryBook(title)
    await story_book.generate_story_details(prompt, character_names)

    # Accessing the generated details
    print("Story Outline:", story_book.outline)
    print("Character Descriptions:", story_book.character_descriptions)

# Running the example
asyncio.run(main())
