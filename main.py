import streamlit as st
# from bokeh.models.widgets import Button
# from bokeh.models import CustomJS
# from streamlit_bokeh_events import streamlit_bokeh_events
import base64
import pandas as pd
import spacy
# import pyaudio
import wave
import os
from spacytextblob.spacytextblob import SpacyTextBlob
from recorder import record
from recognizer_and_predictor import get_large_audio_transcription





# from auto_foldering import auto_foldering

# @st.cache(allow_output_mutation=True)
st.title("Sentiment Analysis using SR:")

st.write("**1- First, Enter your informations:**")
# Enter Infos:
first_name = st.text_area("Enter your First_Name")
second_name = st.text_area("Enter your Second_Name")
location = st.text_area("Enter your Country Name")

# Select Language
languages = ["ar-MA", "fr-FR", "en-US", "he", "it-IT"]
st.write("**2- Select your language:**")
language = st.radio('', languages)

# Duration Sidebar
st.sidebar.title("Duration")
st.write("**3- Choose either to RECORD or UPLOAD your speech:**")
duration = st.sidebar.slider("Recording duration (by min)", 0, 30, 1)

# start
if st.button("Start Recording"):
    root = "./results/"
    chunks_folder = root + first_name + "_" + second_name + "_" + location +"/"
    recoded_file = chunks_folder + "recorded.wav"
    os.mkdir(chunks_folder)

    # Start recording:
    record(duration, chunks_folder)

    # Start prediction:
    get_large_audio_transcription(recoded_file, chunks_folder, language)

file_bytes = st.file_uploader("Upload a file", type=("wav"))
if st.button("Process Uploaded File"):
    root = "./results/"
    chunks_folder = root + first_name + "_" + second_name + "_" + location +"/"
    recoded_file = file_bytes
    os.mkdir(chunks_folder)


    # Start prediction:
    get_large_audio_transcription(recoded_file, chunks_folder, language)