import sys
print sys.path
sys.path.append('/Users/Mackenzie/Documents/2014/vinder')
from firebase import firebase
#from language import audio_parse
from language.audio_parse import *

def main(audio_path): 
  print audio_path
  features = audio_parse(audio_path)
  print features

if __name__ == '__main__':
  main(sys.argv[1])