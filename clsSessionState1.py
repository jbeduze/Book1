import streamlit as st
import random
import json
from clsStoryBook1 import StoryBook  # Assuming your StoryBook class is in a file named storybook.py

class SessionStateUtilities:
    @staticmethod
    def select_random_elements(options, count=10):
        elements = random.sample(options, min(count, len(options)))
        if "surprise me" not in elements:
            elements.append("surprise me")
        return elements

class SessionState:
    def __init__(self):
        self.initial_state = dict(st.secrets.sessionstate)
        self.set()
        self.initialize()
    
    def set(self):
        self._set_lists()
        self._set_initial_attributes()

    def _set_lists(self):
        self.genres = st.secrets["genres"]["options"]
        self.settings = st.secrets["settings"]["options"]
        self.supporting_characters_list = st.secrets["supporting_characters"]["options"]
        self.plot_elements_list = st.secrets["plot_elements"]["options"]
        self.themes_list = st.secrets["themes"]["options"]
        self.magical_objects_list = st.secrets["magical_objects"]["options"]
        self.tone_list = st.secrets["tone"]["options"]
        self.style_list = st.secrets["styles"]["options"]

    def _set_initial_attributes(self):
        self.initial_state["selected_genres"] = SessionStateUtilities.select_random_elements(self.genres, 10)
        self.initial_state["selected_settings"] = SessionStateUtilities.select_random_elements(self.settings, 10)
        self.initial_state["selected_supporting_characters"] = SessionStateUtilities.select_random_elements(self.supporting_characters_list, 10)
        self.initial_state["selected_plot_elements"] = SessionStateUtilities.select_random_elements(self.plot_elements_list, 10)
        self.initial_state["selected_themes"] = SessionStateUtilities.select_random_elements(self.themes_list, 10)
        self.initial_state["selected_magical_objects"] = SessionStateUtilities.select_random_elements(self.magical_objects_list, 10)
        self.initial_state["selected_tones"] = SessionStateUtilities.select_random_elements(self.tone_list, 10)
        self.initial_state["selected_styles"] = self.style_list
        self.initial_state["storybook"] = StoryBook.get_instance()  # Initialize with StoryBook instance
        self.initial_state["mb"] = dict(st.secrets.mb)
        self.initial_state["storyelements"] = dict(st.secrets.storyelements)

    def initialize(self):
        for key, value in self.initial_state.items():
            if key not in st.session_state:
                st.session_state[key] = value

    @classmethod
    def get(cls):
        if 'session_state_instance' not in st.session_state:
            st.session_state.session_state_instance = cls()
        return st.session_state.session_state_instance
         
    def update(self, **kwargs):
        for key, value in kwargs.items():
            st.session_state[key] = value
    
    def get_value(self, key):
        return st.session_state.get(key, None)

    def set_file_content(self, key, filepath, is_json: bool=False):
        try:
            with open(file=filepath, mode="r") as file:
                if not is_json:
                    content = file.read()
                else:
                    content = json.load(file)
            st.session_state[key] = content
        except FileNotFoundError:
            st.session_state[key] = "File Not Found"