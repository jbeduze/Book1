import streamlit as st
from openai import OpenAI
import random
from PIL import Image
import base64
from streamlit_extras.stylable_container import stylable_container
from clsSessionState import SessionState
import aiworking

# Access OpenAI API key from secrets
# openai.api_key = st.secrets["openai"]["openai_api_key"]

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

        setting_select = st.selectbox("Choose the Setting:", options=st.session_state.selected_settings, key='setting_select')
        selected_setting = st.button("Lock Setting", on_click=lock_variable, args=('locked_setting', setting_select))
        if st.session_state.locked_setting:
            st.write(f"**Setting:** {st.session_state.locked_setting}")

        supporting_character_select = st.selectbox("Choose Supporting Character(s):", options=st.session_state.selected_supporting_characters, key='supporting_character_select')
        selected_supporting_character = st.button("Lock Supporting Character", on_click=lock_variable, args=('locked_supporting_character', supporting_character_select))
        if st.session_state.locked_supporting_character:
            st.write(f"**Supporting Character:** {st.session_state.locked_supporting_character}")

        plot_element_select = st.selectbox("Choose Plot Elements:", options=st.session_state.selected_plot_elements, key='plot_element_select')
        selected_plot_element = st.button("Lock Plot Element", on_click=lock_variable, args=('locked_plot_element', plot_element_select))
        if st.session_state.locked_plot_element:
            st.write(f"**Plot Element:** {st.session_state.locked_plot_element}")

        theme_select = st.selectbox("Choose the Theme:", options=st.session_state.selected_themes, key='theme_select')
        selected_theme = st.button("Lock Theme", on_click=lock_variable, args=('locked_theme', theme_select))
        if st.session_state.locked_theme:
            st.write(f"**Theme:** {st.session_state.locked_theme}")

        magical_object_select = st.selectbox("Choose Magical Objects:", options=st.session_state.selected_magical_objects, key='magical_object_select')
        selected_magicobject = st.button("Lock Magical Object", on_click=lock_variable, args=('locked_magical_object', magical_object_select))
        if st.session_state.locked_magical_object:
            st.write(f"**Magical Object:** {st.session_state.locked_magical_object}")

        tone_select = st.selectbox("Choose the Tone/Mood:", options=st.session_state.selected_tones, key='tone_select')
        selected_tone = st.button("Lock Tone", on_click=lock_variable, args=('locked_tone', tone_select))
        if st.session_state.locked_tone:
            st.write(f"**Tone/Mood:** {st.session_state.locked_tone}")

        style_select = st.selectbox("Choose the illustration Style:", options=st.session_state.selected_styles, key='style_select')
        selected_style = st.button("Lock Style", on_click=lock_variable, args=('locked_style', style_select))
        if st.session_state.locked_style:
            st.write(f"**Style:** {st.session_state.locked_style}")
            
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
            st.session_state.uploaded_image_file = uploaded_img
            uploaded_image_type = uploaded_img.type
            st.session_state.uploaded_image_type = uploaded_image_type
            image = Image.open(uploaded_img)
            st.session_state.uploaded_image = image
            st.image(image, caption='Uploaded Image.', use_column_width=True)
            st.write("Please verify that this is the correct image. If not, please delete and upload a new image")
        else:
            st.warning("Please upload an image.")

        relation = st.text_input("Relation to the recipient")
        if relation:
            st.session_state.relation = relation
            st.success(relation)

        name_of_recipient = st.text_input("Insert the name of the recipient here")
        if name_of_recipient:
            st.session_state.recipient_name = name_of_recipient
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
        outline_placeholder = st.empty()
        description_placeholder = st.empty()
        if getoutline_button:
            prompt1 = prompt1_template.format(genre=st.session_state.locked_genre, setting=st.session_state.locked_setting, supporting_character=st.session_state.locked_supporting_character, plot_element=st.session_state.locked_plot_element, theme=st.session_state.locked_theme, magical_object=st.session_state.locked_magical_object, tone=st.session_state.locked_tone, style=st.session_state.locked_style, recipient_name=st.session_state.recipient_name, relation=st.session_state.relation, main_character_description=st.session_state.main_character_description)
            outline = aiworking.generate_story_outline(prompt1)
            description = aiworking.generate_character_description()
            with outline_placeholder.container():
                st.markdown("**OUTLINE**")
                cols = st.columns(5)
                counter = 0
                for key, value in outline.items():
                    with cols[counter]:
                        with st.container(height=200):
                            with st.popover(label=key, use_container_width=True):
                                st.markdown(value)
                    counter = counter + 1
            with description_placeholder.container():
                st.markdown("**CHARACTER DESCRIPTION**")
                st.divider()
                st.markdown(description['character_description'])
            
                    



simple_container()



#         if st.button("Generate Story Outline"):
#             elements = {
#                 "theme": st.session_state.locked_theme,
#                 "environment": st.session_state.locked_setting,
#                 "main_character": name_of_recipient,
#                 "supporting_characters": st.session_state.locked_supporting_character,
#                 "plot_elements": st.session_state.locked_plot_element,
#                 "tone": st.session_state.locked_tone,
#             }
#             outline = generate_story_outline(elements)
#             st.header("Generated Story Outline")
#             st.write(outline)

# # Function to generate story outline using OpenAI API
# def generate_story_outline(elements):
#     prompt = (
#         f"Create a story with the following elements:\n"
#         f"Theme: {elements['theme']}\n"
#         f"Environment: {elements['environment']}\n"
#         f"Main Character: {elements['main_character']}\n"
#         f"Supporting Characters: {elements['supporting_characters']}\n"
#         f"Plot Elements: {elements['plot_elements']}\n"
#         f"Tone/Mood: {elements['tone']}\n\n"
#         "Story Outline:"
#     )

#     response = openai.Completion.create(
#         engine="text-davinci-003",
#         prompt=prompt,
#         max_tokens=500
#     )

#     return response.choices[0].text.strip()