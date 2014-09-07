#!/usr/local/bin/python

import speech_recognition as sr
import sys
import os
import nltk
# import multiprocessing as mp
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool
from wave_cut import cut_wave
from nltk_features import get_features 
from nltk.corpus import stopwords

trial_keys = ['AIzaSyCzfSslLEsPH5VNMsoywLTmooC2od2IZoc',
              'AIzaSyDUY3b_BdCeGcRJPck6Hf1m1sy21-6LFxA',
              'AIzaSyD-53-pSVtSMoD7kNjX2wopSnIAAH87108',
              'AIzaSyBH4N84Gw04sZlvqc8QAw5QdRGcscn8Sks',
              'AIzaSyDeHXQ3GA-RFcFbobQv0GS53EhG1C-yMLk']

nltk.data.path.append('./nltk_data/')

def audio_convert(filename):
    # This combines the cutting and the conversions

    cut_files = {}
    text = {}
    
    error_file = open('error.txt', 'w')
    error_file.write(filename)
    for speed in ['slow', 'fast']:
        if speed == 'slow':
            cut_files[speed] = cut_wave(filename, 0.70)
        else:
            cut_files[speed] = cut_wave(filename, 0.85) 
        # assert(False)
        pool = ThreadPool(processes = len(cut_files[speed]))
        text[speed] = pool.map(chunk_convert, cut_files[speed])
        pool.close()
        # text[speed] = [chunk_convert(x) for x in cut_files[speed]]
        print "Closed a pool"
        # Clear out the temporary files created
        for x in cut_files[speed]:
            os.remove(x)

    text = text['slow'] + text['fast']
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
        except KeyError:
            print "API Error"
            got_transcription = False
            api_key = api_key + 1
        except LookupError:
            print('Could not understand audio')

        if translate_success:
            print translate
            return translate

    return ''

def audio_parse(filename):
    text_list = audio_convert(filename)
    if(len(text_list) == 0):
        return([None] * 16) 
    full_text =  ' ' + ' '.join(text_list) + ' '
    full_parse = get_features(full_text)
    full_text.lower()

    # print full_parse
    # print full_text

    # print stopwords.words('english')

    # Remove stopwords when recording the text
    for w in stopwords.words('english') + ['like']:
        full_text = full_text.replace(' ' + w + ' ', ' ')

    # print full_text
    full_parse.append(full_text.strip())
    return full_parse

# x = audio_parse('audio/guitar.wav')
# print(x)
