#!/usr/local/bin/python

import nltk, nltk.data
import numpy as np

# Load the models 
SENTDET = nltk.data.load('tokenizers/punkt/english.pickle')

def get_features(full_text):
    # Get the feature list.
    
    # Kinds of summary statistics (3)

    # Total number of words
    # Average word length
    # Standard deviation of word length

    # - Various Densities (10)
    # Adjective
    # Noun
    # Verb
    # Articles
    # Conjunction
    # Adverbs
    # Pronouns
    # Prepositions
    # Interjections (like 'uhhhs')

    # - Comparisons (3)
    # Complicated Verbs
    # Superlatives relative to Total
    # Comparatives relative to Total

    all_sent = SENTDET.tokenize(full_text)
    all_sent = [x.replace('.', '') for x in all_sent]

    parse_sent = [nltk.pos_tag(nltk.word_tokenize(x)) for x in all_sent]
    print parse_sent

    parse_words = [item for sublist in parse_sent for item in sublist]

    parse_words = [x for x in parse_words if x[0] != ',']
    # print len(parse_words)
    # print parse_words

    # Compute the first wave of three summary statistics
    tot = float(len(parse_words))
    word_lengths = [len(x[0]) for x in parse_words]
    summary_stat = [len(word_lengths), round(np.mean(word_lengths), 2), round(np.std(word_lengths), 2)]

    # Now compute densities
    important_tags = ['JJ', 'JJR', 'JJS', 
                      'NN', 'NNP', 'NNPS', 'NNS', 
                      'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ',
                      'MD',
                      'DT', 'FW', 'WDT',
                      'LS', 'IN',
                      'RB', 'RBR', 'RBS',
                      'POS', 'PRP', 'PRP$', 'WP', 'WP$',
                      'RP', 'TO',
                      'UH']

    word_types = {}

    # Initialize them as you go 
    for k in important_tags:
        word_types[k] = 0

    # print 'Initialized tags'

    # Now you go through the parsed words and increment when you see things
    for pair in parse_words:
        # print pair
        if pair[1] in word_types.keys():
            # print pair[1]
            word_types[pair[1]] = word_types[pair[1]] + 1

    print word_types

    # We now follow the formulas and compute the pure densities

    adj = (word_types['JJ'] + word_types['JJR'] + word_types['JJS'])/tot
    noun = (word_types['NN'] + word_types['NNP'] +\
            word_types['NNPS'] + word_types['NNS'])/tot
    verb = (word_types['VB'] + word_types['VBD'] + word_types['VBG'] +\
            word_types['VBN'] + word_types['VBP'] + word_types['VBZ'])/tot
    aux = word_types['MD']/tot
    art = (word_types['DT'] + word_types['FW'] + word_types['WDT'])/tot
    conj = (word_types['LS'] + word_types['IN'] * 0.5)/tot
    advb = (word_types['RB'] + word_types['RBR'] + word_types['RBS'])/tot
    pron = (word_types['POS'] + word_types['PRP'] + word_types['PRP$'] +\
            word_types['WP'] + word_types['WP$'])/tot
    prep = (word_types['RP'] + word_types['TO'] + word_types['IN'] * 0.5)/tot
    inter = word_types['UH']/tot

    densities = [adj, noun, verb, aux, art, conj, advb, pron, prep, inter]
    densities = [round(x * 10, 2) for x in densities]

    # Now we compute the ratios

    ratio_vb = (word_types['VBG'] + word_types['VBN'] +\
                word_types['VBP'] + word_types['VBZ'])/\
                (verb * tot + 0.00001)
    ratio_super = (word_types['RBS'] + word_types['JJS'])/(adj + advb + 0.00001) / tot
    ratio_comp = (word_types['RBR'] + word_types['JJR'])/(adj + advb + 0.00001) / tot

    ratios = [ratio_vb, ratio_super, ratio_comp]
    ratios = [round(x, 3) for x in ratios]

    return(summary_stat + densities + ratios)

