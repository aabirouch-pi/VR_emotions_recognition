import spacy
from spacy import displacy
import librosa
import streamlit as st



def word_counting(paragraph):
	message = "The number of words you spoke: " + str(len(paragraph.split())) + "words"
	return message

def speed_of_talk(paragraph, duration):
	num_words = len(paragraph.split())
	speed = num_words/duration
	message = "You are speaking with a rate of: " + str(speed) + " word per second"
	return message

def NER(paragraph, nlp_lang):
	nlp = spacy.load(nlp_lang)
	doc = nlp(paragraph)

	for i in range(len(doc)):
		text = doc[i].text
		ent_IOB = doc[i].ent_iob_
		ent_TYPE = doc[i].ent_type_

		if ent_IOB != "O":
			st.write(text, ent_IOB, ent_TYPE)
		else:
			pass

def audio_duration(audio_file):
	duration = librosa.get_duration(filename=audio_file)
	return duration