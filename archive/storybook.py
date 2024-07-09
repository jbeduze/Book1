import streamlit as st
from openai import OpenAI
import time
import json
from typing import Literal
import base64


# 0. Setup
client = OpenAI(api_key=st.secrets.openai.apikey)
assistantid = st.secrets.openai.assistantid
threadid = client.beta.threads.create().id
st.session_state.threadid = threadid
prompt1_template = st.secrets.prompts.prompt1
prompt2_template = st.secrets.prompts.prompt2
prompt3_template = st.secrets.prompts.prompt3
prompt4_template = st.secrets.prompts.prompt4
jsonformat = {"type": "json_object"}


# Open the file and load the JSON data
with open("working/inputs.json", "r") as file:
    data = json.load(file)

# Print the loaded JSON data
print(data)
###### STORYBOOK ##############
# 1. Inputs


# 2. Create Outline (5 point outline)


# 3. Create Concept (title, summary paragraph, reading level)


#### STOPPING POINT - PRESENT SUMMARY PARAGRAPH TO USER

# 4. 

