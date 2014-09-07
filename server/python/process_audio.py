import sys
print sys.path
sys.path.append('/Users/Mackenzie/Documents/2014/vinder')
from firebase import firebase
from language import match


def main(user_hash, mp3_url, audio_path): 
  print 'running main'
#  features = process_audio(audio_path)
  features = [1,2,3]
  print "HELO"
  print features
  # Store feature vector in Firebase
  fb = firebase.FirebaseApplication('https://vinder.firebaseio.com', None)
  fb.post('users/', {'anid': {'features': features,
                     'user_hash': user_hash,
                     'mp3_url': mp3_url,
                     'matches': []}})
  match.update_matches(user_hash)


if __name__ == '__main__':
  main(sys.argv[1], sys.argv[2], sys.argv[3])
