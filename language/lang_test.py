#!/usr/local/bin/python

from nltk_features import get_features 
import sys

# When running it stepwise I will just type in a few example sentences.

print sys.argv
test_text = sys.argv[1]
test_features = get_features(test_text)
print(test_features)
