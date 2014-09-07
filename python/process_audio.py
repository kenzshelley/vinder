import sys
import os
print sys.path
print os.path.dirname(os.path.abspath(__file__))
sys.path.append('/app/vinder/')
from firebase import firebase
#from language import audio_parse
from language.audio_parse import *

def main(audio_path): 
  print audio_path
  features = audio_parse(audio_path)
  print features

if __name__ == '__main__':
  main(sys.argv[1])
