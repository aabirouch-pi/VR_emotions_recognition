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
st.write("**Sentiment Analysis Based on Voice Recognition:**")

# Enter Infos:
first_name = st.text_area("Enter your First_Name")
second_name = st.text_area("Enter your Second_Name")
location = st.text_area("Enter your Country Name")

# Duration Sidebar
st.sidebar.title("Duration")
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
    get_large_audio_transcription(recoded_file, chunks_folder)