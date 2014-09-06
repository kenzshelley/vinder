#!/usr/local/bin/python

import speech_recognition as sr
import sys

trial_keys = ['AIzaSyCzfSslLEsPH5VNMsoywLTmooC2od2IZoc']

got_transcription = False
api_key = 0

while (not got_transcription) and api_key < len(trial_keys):
    got_transcription = True
    translate_success = False    
    try:
        r = sr.Recognizer(key = trial_keys[api_key])
        r.pause_threshold = 1.5
        r.energy_threshold = 50
        with sr.WavFile(sys.argv[1]) as source:
            audio = r.record(source, duration = None)
            translate = r.recognize(audio, True)

        translate_success = True
        # recognize speech using Google Speech Recognition
    except KeyError:                                    # API key hit the limit
        got_transcription = false
        api_key = api_key + 1
    except LookupError:                                 # speech is unintelligible
        print('Could not understand audio')

    if translate_success:
        print('Transcriptions:')
        for prediction in translate:
            print(prediction['text'] + ' (' + str(round(prediction['confidence'] * 100)) + ') ')
