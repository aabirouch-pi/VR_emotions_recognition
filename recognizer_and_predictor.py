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
# Audio Chuncking:
import speech_recognition as sr 
import os 
from pydub import AudioSegment
from pydub.silence import split_on_silence
from insights import word_counting, speed_of_talk, NER


# create a speech recognition object
r = sr.Recognizer()

# a function that splits the audio file into chunks
# and applies speech recognition
def get_large_audio_transcription(path, chunks_folder, lang, duration, nlp_lang):
    st.write("Predictions started")
    """
    Splitting the large audio file into chunks
    and apply speech recognition on each of these chunks
    """
    # open the audio file using pydub
    sound = AudioSegment.from_wav(path)  
    # split audio sound where silence is 700 miliseconds or more and get chunks
    chunks = split_on_silence(sound,
        # experiment with this value for your target audio file
        min_silence_len = 500,
        # adjust this per requirement
        silence_thresh = sound.dBFS-14,
        # keep the silence for 1 second, adjustable as well
        keep_silence=1000)


    folder_name = chunks_folder
    # create a directory to store the audio chunks
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""
    sheet_file = pd.DataFrame(columns=["Chunck_Name", "Text", "Polarity"])
    stat = [0,# Positive value
            0,# Inddiff value
            0]# Negative value
    # process each chunk 
    for i, audio_chunk in enumerate(chunks, start=1):
        # export audio chunk and save it in
        # the `folder_name` directory.
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        # recognize the chunk
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            # try converting it to text
            try:
                text = r.recognize_google(audio_listened, language=lang)
            except sr.UnknownValueError as e:
                st.write("Error:", str(e))
            else:
                text = f"{text.capitalize()}. "
                st.write(f"**chunk{i}.wav**", ":")
                # sheet_file["Chunck_Name"][i-1] = f"chunk{i}.wav"

                st.write("**What you said is: **", text)
                # sheet_file["Text"][i-1] = str(text)

                nlp = spacy.load(nlp_lang)
                nlp.add_pipe('spacytextblob')
                doc = nlp(text)
                impression = doc._.polarity
                if impression >0.5:
                    st.write("**The Impression is: **", "Positive" )
                    sheet_file = sheet_file.append({'Chunck_Name' : f"chunk{i}.wav", 'Text' : text, 'Polarity' : "Positive"}, ignore_index = True)
                    stat[0] = stat[0] + 1

                if impression  >=0.4 and impression<= 0.5:
                    st.write("**The Impression is: **", "Indifferent" )
                    sheet_file = sheet_file.append({'Chunck_Name' : f"chunk{i}.wav", 'Text' : text, 'Polarity' : "Indifferent"}, ignore_index = True)
                    stat[1] = stat[1] + 1

                else:
                    st.write("**The Impression is: **", "Negative" )
                    sheet_file = sheet_file.append({'Chunck_Name' : f"chunk{i}.wav", 'Text' : text, 'Polarity' : "Negative"}, ignore_index = True)
                    stat[2] = stat[2] + 1




                whole_text += text
    sheet_file.to_csv(chunks_folder + "results.csv")
    stat_percent = [imp_stat / sum(stat) for imp_stat in stat]
    st.write("**The result of the whole record**")
    # Emotions
    st.write("**You've been **", stat_percent[0]*100, " % Positive")
    st.write("**You've been **", stat_percent[1]*100, " % Neutral")
    st.write("**You've been **", stat_percent[2]*100, " % Negative")
    # Word Counting
    st.write(word_counting(whole_text))
    # # Speed of Talk
    st.write(speed_of_talk(whole_text, duration))
    if lang not in ["fr-FR", "en-US", "it-IT"]:
        st.write(NER(whole_text, nlp_lang))

    # return the text for all chunks detected
    # return NER(whole_text)