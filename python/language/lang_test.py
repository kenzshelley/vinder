#!/usr/local/bin/python

from nltk_features import get_features 
import sys

# When running it stepwise I will just type in a few example sentences.

print sys.argv
filename = sys.argv[1]
story = file(filename, 'r')
story_text = story.read()
story.close()

test_features = get_features(story_text)
print(test_features)
