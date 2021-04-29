import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
import base64
import pandas as pd
import spacy
import pyaudio
import wave
from spacytextblob.spacytextblob import SpacyTextBlob


########################################################################################################################################
########################################################################################################################################
def record(duration, chunks_folder):
    filename = chunks_folder + "recorded.wav"
    

    with st.spinner("Recording..."):
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 2
        RATE = 44100
        RECORD_SECONDS = duration*60
        
        p = pyaudio.PyAudio()
        
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
        
        frames = []
        
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)
        
        st.write("* done recording")
        
        stream.stop_stream()
        stream.close()
        wf = wave.open(filename, "wb")
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b"".join(frames))
        wf.close()
    
########################################################################################################################################
########################################################################################################################################

