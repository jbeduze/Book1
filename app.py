import streamlit as st
import openai
import random
from PIL import Image
import base64
from streamlit_extras.stylable_container import stylable_container

# Access OpenAI API key from secrets
# openai.api_key = st.secrets["openai"]["openai_api_key"]

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
            image = Image.open(uploaded_img)
            st.image(image, caption='Uploaded Image.', use_column_width=True)
            st.write("Please verify that this is the correct image. If not, please delete and upload a new image")
        else:
            st.warning("Please upload an image.")

        relation = st.text_input("Relation to the recipient")
        if relation:
            st.success(relation)

        name_of_recipient = st.text_input("Insert the name of the recipient here")
        if name_of_recipient:
            st.success(name_of_recipient)

        def select_random_elements(options, count=10):
            elements = random.sample(options, min(count, len(options)))
            if "surprise me" not in elements:
                elements.append("surprise me")
            return elements

        genres = st.secrets["genres"]["options"]
        settings = st.secrets["settings"]["options"]
        supporting_characters_list = st.secrets["supporting_characters"]["options"]
        plot_elements_list = st.secrets["plot_elements"]["options"]
        themes_list = st.secrets["themes"]["options"]
        magical_objects_list = st.secrets["magical_objects"]["options"]
        tone_list = st.secrets["tone"]["options"]
        style_list = st.secrets["styles"]["options"]

        def initialize_session_state():
            if 'locked_genre' not in st.session_state:
                st.session_state.locked_genre = None
            if 'locked_setting' not in st.session_state:
                st.session_state.locked_setting = None
            if 'locked_supporting_character' not in st.session_state:
                st.session_state.locked_supporting_character = None
            if 'locked_plot_element' not in st.session_state:
                st.session_state.locked_plot_element = None
            if 'locked_theme' not in st.session_state:
                st.session_state.locked_theme = None
            if 'locked_magical_object' not in st.session_state:
                st.session_state.locked_magical_object = None
            if 'locked_tone' not in st.session_state:
                st.session_state.locked_tone = None
            if 'locked_style' not in st.session_state:
                st.session_state.locked_style = None

            if 'selected_genres' not in st.session_state:
                st.session_state.selected_genres = select_random_elements(genres)
            if 'selected_settings' not in st.session_state:
                st.session_state.selected_settings = select_random_elements(settings)
            if 'selected_supporting_characters' not in st.session_state:
                st.session_state.selected_supporting_characters = select_random_elements(supporting_characters_list)
            if 'selected_plot_elements' not in st.session_state:
                st.session_state.selected_plot_elements = select_random_elements(plot_elements_list)
            if 'selected_themes' not in st.session_state:
                st.session_state.selected_themes = select_random_elements(themes_list)
            if 'selected_magical_objects' not in st.session_state:
                st.session_state.selected_magical_objects = select_random_elements(magical_objects_list)
            if 'selected_tones' not in st.session_state:
                st.session_state.selected_tones = select_random_elements(tone_list)
            if 'selected_styles' not in st.session_state:
                st.session_state.selected_styles = style_list

        initialize_session_state()

        if st.button("Generate New Lists"):
            st.session_state.selected_genres = select_random_elements(genres)
            st.session_state.selected_settings = select_random_elements(settings)
            st.session_state.selected_supporting_characters = select_random_elements(supporting_characters_list)
            st.session_state.selected_plot_elements = select_random_elements(plot_elements_list)
            st.session_state.selected_themes = select_random_elements(themes_list)
            st.session_state.selected_magical_objects = select_random_elements(magical_objects_list)
            st.session_state.selected_tones = select_random_elements(tone_list)
            st.session_state.selected_styles = style_list

        def create_story_form():
            with st.expander("Choose Story Elements"):
                if not st.session_state.locked_genre:
                    st.session_state.selected_genre = st.selectbox("Choose the Genre:", options=st.session_state.selected_genres, key='genre_select')
                    if st.button("Lock Genre"):
                        st.session_state.locked_genre = st.session_state.selected_genre
                else:
                    st.write(f"**Genre:** {st.session_state.locked_genre}")

                if not st.session_state.locked_setting:
                    st.session_state.selected_setting = st.selectbox("Choose the Setting:", options=st.session_state.selected_settings, key='setting_select')
                    if st.button("Lock Setting"):
                        st.session_state.locked_setting = st.session_state.selected_setting
                else:
                    st.write(f"**Setting:** {st.session_state.locked_setting}")

                if not st.session_state.locked_supporting_character:
                    st.session_state.selected_supporting_character = st.selectbox("Choose Supporting Character(s):", options=st.session_state.selected_supporting_characters, key='supporting_character_select')
                    if st.button("Lock Supporting Character"):
                        st.session_state.locked_supporting_character = st.session_state.selected_supporting_character
                else:
                    st.write(f"**Supporting Character:** {st.session_state.locked_supporting_character}")

                if not st.session_state.locked_plot_element:
                    st.session_state.selected_plot_element = st.selectbox("Choose Plot Elements:", options=st.session_state.selected_plot_elements, key='plot_element_select')
                    if st.button("Lock Plot Element"):
                        st.session_state.locked_plot_element = st.session_state.selected_plot_element
                else:
                    st.write(f"**Plot Element:** {st.session_state.locked_plot_element}")

                if not st.session_state.locked_theme:
                    st.session_state.selected_theme = st.selectbox("Choose the Theme:", options=st.session_state.selected_themes, key='theme_select')
                    if st.button("Lock Theme"):
                        st.session_state.locked_theme = st.session_state.selected_theme
                else:
                    st.write(f"**Theme:** {st.session_state.locked_theme}")

                if not st.session_state.locked_magical_object:
                    st.session_state.selected_magical_object = st.selectbox("Choose Magical Objects:", options=st.session_state.selected_magical_objects, key='magical_object_select')
                    if st.button("Lock Magical Object"):
                        st.session_state.locked_magical_object = st.session_state.selected_magical_object
                else:
                    st.write(f"**Magical Object:** {st.session_state.locked_magical_object}")

                if not st.session_state.locked_tone:
                    st.session_state.selected_tone = st.selectbox("Choose the Tone/Mood:", options=st.session_state.selected_tones, key='tone_select')
                    if st.button("Lock Tone"):
                        st.session_state.locked_tone = st.session_state.selected_tone
                else:
                    st.write(f"**Tone/Mood:** {st.session_state.locked_tone}")
                
                if not st.session_state.locked_style:
                    st.session_state.selected_style = st.selectbox("Choose the illustration Style:", options=st.session_state.selected_styles, key='style_select')
                    if st.button("Lock Style"):
                        st.session_state.locked_style = st.session_state.selected_style
                else:
                    st.write(f"**Style:** {st.session_state.locked_style}")

        create_story_form()

        

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

simple_container()
