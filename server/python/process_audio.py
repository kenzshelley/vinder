import sys
print sys.path
sys.path.append('/Users/Mackenzie/Documents/2014/vinder')
from firebase import firebase
from language import match


def main(audio_path): 
  print 'running main'
#  features = process_audio(audio_path)
  features = [1,2,3]
  print features


if __name__ == '__main__':
  main(sys.argv[1])
