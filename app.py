import streamlit as st
from openai import OpenAI
import random
from PIL import Image
import base64
from streamlit_extras.stylable_container import stylable_container
from clsSessionState import SessionState
from clsStorybook import generate_story
import asyncio
from typing import Literal
from io import BytesIO

# Access OpenAI API key from secrets
# openai.api_key = st.secrets["openai"]["openai_api_key"]

#0. Set Page config
st.set_page_config(page_icon=st.secrets.paths.icon, page_title="MagicBook", layout="wide", initial_sidebar_state="collapsed")
#st.logo(image=open(st.secrets.paths.logo, "rb").read(), icon_image=open(st.secrets.paths.icon, "rb").read())

# 1. Set Session State
ss = SessionState.get()

# 2. Set Variables - Lists
genres = st.secrets["genres"]["options"]
settings = st.secrets["settings"]["options"]
supporting_characters_list = st.secrets["supporting_characters"]["options"]
plot_elements_list = st.secrets["plot_elements"]["options"]
themes_list = st.secrets["themes"]["options"]
magical_objects_list = st.secrets["magical_objects"]["options"]
tone_list = st.secrets["tone"]["options"]
style_list = st.secrets["styles"]["options"]

# 3. Set Variables - OpenAI
client = OpenAI(api_key=st.secrets.openai.apikey)
prompt1_template = st.secrets.prompts.prompt1


# 4. Set Functions - Callbacks
def lock_variable(key, value):
    st.session_state[key] = value

# 5. Set Functions - Other
def encode_image(image_input, type: Literal['path', 'bytes', 'pil']):
    if type == "path":
        with open(image_input, "rb") as image_file:
            image_data = image_file.read()
    elif type == "bytes":
        image_data = image_input.getvalue()
    elif type == "pil":
        buffered = BytesIO()
        image_input.save(buffered, format="PNG")
        image_data = buffered.getvalue()
    else:
        raise ValueError("Invalid type. Must be 'path', 'bytes', or 'pil'.")
    
    encoded_image = base64.b64encode(image_data).decode('utf-8')
    return encoded_image
  
def get_image_url(encoded_image, image_type: Literal['png', 'jpg', 'jpeg', 'gif']):
    imageurl = f"data:image/{image_type};base64,{encoded_image}"
    return imageurl

def select_random_elements(options, count=10):
    elements = random.sample(options, min(count, len(options)))
    if "surprise me" not in elements:
        elements.append("surprise me")
    return elements


def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
            background-size: cover
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

add_bg_from_local('Bookshelf.png')

def create_story_form():
    with st.expander("Choose Story Elements"):
        genre_select = st.selectbox("Choose the Genre:", options=st.session_state.selected_genres, key='genre_select')
        selected_genre = st.button("Lock Genre", on_click=lock_variable, args=('locked_genre', genre_select))
        if st.session_state.locked_genre:
            st.write(f"**Genre:** {st.session_state.locked_genre}")
            st.session_state.storyelements['genre'] = st.session_state.locked_genre

        setting_select = st.selectbox("Choose the Setting:", options=st.session_state.selected_settings, key='setting_select')
        selected_setting = st.button("Lock Setting", on_click=lock_variable, args=('locked_setting', setting_select))
        if st.session_state.locked_setting:
            st.write(f"**Setting:** {st.session_state.locked_setting}")
            st.session_state.storyelements['setting'] = st.session_state.locked_setting

        supporting_character_select = st.selectbox("Choose Supporting Character(s):", options=st.session_state.selected_supporting_characters, key='supporting_character_select')
        selected_supporting_character = st.button("Lock Supporting Character", on_click=lock_variable, args=('locked_supporting_character', supporting_character_select))
        if st.session_state.locked_supporting_character:
            st.write(f"**Supporting Character:** {st.session_state.locked_supporting_character}")
            st.session_state.storyelements['supporting_character'] = st.session_state.locked_supporting_character

        plot_element_select = st.selectbox("Choose Plot Elements:", options=st.session_state.selected_plot_elements, key='plot_element_select')
        selected_plot_element = st.button("Lock Plot Element", on_click=lock_variable, args=('locked_plot_element', plot_element_select))
        if st.session_state.locked_plot_element:
            st.write(f"**Plot Element:** {st.session_state.locked_plot_element}")
            st.session_state.storyelements['plot_element'] = st.session_state.locked_plot_element

        theme_select = st.selectbox("Choose the Theme:", options=st.session_state.selected_themes, key='theme_select')
        selected_theme = st.button("Lock Theme", on_click=lock_variable, args=('locked_theme', theme_select))
        if st.session_state.locked_theme:
            st.write(f"**Theme:** {st.session_state.locked_theme}")
            st.session_state.storyelements['theme'] = st.session_state.locked_theme

        magical_object_select = st.selectbox("Choose Magical Objects:", options=st.session_state.selected_magical_objects, key='magical_object_select')
        selected_magicobject = st.button("Lock Magical Object", on_click=lock_variable, args=('locked_magical_object', magical_object_select))
        if st.session_state.locked_magical_object:
            st.write(f"**Magical Object:** {st.session_state.locked_magical_object}")
            st.session_state.storyelements['magical_object'] = st.session_state.locked_magical_object

        tone_select = st.selectbox("Choose the Tone/Mood:", options=st.session_state.selected_tones, key='tone_select')
        selected_tone = st.button("Lock Tone", on_click=lock_variable, args=('locked_tone', tone_select))
        if st.session_state.locked_tone:
            st.write(f"**Tone/Mood:** {st.session_state.locked_tone}")
            st.session_state.storyelements['tone'] = st.session_state.locked_tone

        style_select = st.selectbox("Choose the illustration Style:", options=st.session_state.selected_styles, key='style_select')
        selected_style = st.button("Lock Style", on_click=lock_variable, args=('locked_style', style_select))
        if st.session_state.locked_style:
            st.write(f"**Style:** {st.session_state.locked_style}")
            st.session_state.storyelements['style'] = st.session_state.locked_style
            

def simple_container():
    with stylable_container(
        key="Simple_Container",
        css_styles="""
        {
            box-shadow: 0px 0px 10px #0099FF;
            font-family: 'Arial', sans-serif;
            font-size: 20px;
            transition: background-color 0.3s ease, box-shadow 0.3s ease;
            border: 2px solid c;
            border-radius: 5px;
            background-color: #4E312DD9;
            color: #3FED43;
            width:102%;
            padding: 5px;
            margin: 5px;
        }
        """,
    ):
        uploaded_img = st.file_uploader("Upload a picture of the person/pet you'd like as the main Character of the story", type=['png', 'jpg', 'jpeg', 'gif'])
        
        if uploaded_img is not None:
            st.session_state.uploaded_image = uploaded_img
            st.session_state.uploaded_image_type = uploaded_img.type
            st.session_state.uploaded_image_data = Image.open(uploaded_img)
            st.session_state.uploaded_encoded_image = encode_image(image_input=st.session_state.uploaded_image_data, type="pil")
            st.session_state.uploaded_image_url = get_image_url(encoded_image=st.session_state.uploaded_encoded_image, image_type=st.session_state.uploaded_image_type)
            with st.popover(label="Uploaded Image", use_container_width=True):
                st.image(st.session_state.uploaded_image_data, caption='Uploaded Image.', use_column_width=True)
            st.write("Please verify that this is the correct image. If not, please delete and upload a new image")
        else:
            st.warning("Please upload an image.")

        relation = st.text_input("Relation to the recipient")
        if relation:
            st.session_state.storyelements['relation_to_recipient'] = relation
            st.success(relation)

        name_of_recipient = st.text_input("Insert the name of the recipient here")
        if name_of_recipient:
            st.session_state.storyelements['character_name'] = name_of_recipient
            st.success(name_of_recipient)

        if st.button("Generate New Lists"):
            st.session_state.selected_genres = select_random_elements(genres)
            st.session_state.selected_settings = select_random_elements(settings)
            st.session_state.selected_supporting_characters = select_random_elements(supporting_characters_list)
            st.session_state.selected_plot_elements = select_random_elements(plot_elements_list)
            st.session_state.selected_themes = select_random_elements(themes_list)
            st.session_state.selected_magical_objects = select_random_elements(magical_objects_list)
            st.session_state.selected_tones = select_random_elements(tone_list)
            st.session_state.selected_styles = style_list

        create_story_form()
        getoutline_button = st.button(label="Generate Story Outline")
        

        if getoutline_button:
            output_container = st.container(border=False)
            with output_container:
                with st.spinner("Generating Story..."):
                    asyncio.run(generate_story())
                output_cols = st.columns(5)
                with output_cols[0]:
                    outline_placeholder = st.empty()
                with output_cols[1]:
                    titlesummary_placeholder = st.empty()
                with output_cols[2]:
                    characterdesc_placeholder = st.empty()
                with output_cols[3]:
                    characterimage_placeholder = st.empty()
                with output_cols[4]:
                    narrative_placeholder = st.empty()
            

            with outline_placeholder.container():
                with st.popover(label="Story Outline", use_container_width=True):
                    st.markdown(st.session_state.outline)
                
            with titlesummary_placeholder.container():
                with st.popover(label="Title and Summary", use_container_width=True):
                    st.markdown(st.session_state.titlesummary)
            
            with characterdesc_placeholder.container():
                with st.popover(label="Character Description", use_container_width=True):
                    st.markdown(st.session_state.characterdesc)
                
            with characterimage_placeholder.container():
                with st.popover(label="Character Image", use_container_width=True):
                    st.image(image=st.session_state.characterimageurl)
            
            with narrative_placeholder.container():
                with st.popover(label="Narrative", use_container_width=True):
                    st.markdown(st.session_state.narrative)
                
                    



simple_container()

