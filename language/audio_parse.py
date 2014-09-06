#!/usr/local/bin/python

import speech_recognition as sr
import sys
import os
from wave_cut import cut_wave
from nltk_features import get_features 

trial_keys = ['AIzaSyCzfSslLEsPH5VNMsoywLTmooC2od2IZoc',
              'AIzaSyDUY3b_BdCeGcRJPck6Hf1m1sy21-6LFxA']

def audio_convert(filename):
	# This combines the cutting and the conversions
	cut_files = cut_wave(filename)
	text = [chunk_convert(x) for x in cut_files]

	# Clear out the temporary files created
	for x in cut_files:
		os.remove(x)

	text = [x for x in text if len(x) > 0]
	return(text)


def chunk_convert(filename):
	# This converts the small chunk

	got_transcription = False
	api_key = 0

	while (not got_transcription) and api_key < len(trial_keys):
	    got_transcription = True
	    translate_success = False    
	    try:
	        print "Using api key " + str(api_key)
	        r = sr.Recognizer(key = trial_keys[api_key])
	        r.pause_threshold = 2
	        r.energy_threshold = 100
	        with sr.WavFile(filename) as source:
	            audio = r.record(source, duration = None)
	            translate = r.recognize(audio)

	        translate_success = True
	        # recognize speech using Google Speech Recognition
	    except KeyError:                                    # API key hit the limit
	        got_transcription = False
	        api_key = api_key + 1
	    except LookupError:                                 # speech is unintelligible
	        print('Could not understand audio')

	    if translate_success:
	    	print translate
	    	return translate
	    else:
	    	return ''


def audio_parse(filename):
	text_list = audio_convert(filename)
	if(len(text_list) == 0):
		return([None] * 15)	
	full_text = ' '.join(text_list)
	full_parse = get_features(full_text)
	return full_parse

x = audio_parse('audio/final_rap.wav')
print(x)