from firebase import firebase
import sys

def main(user_hash, mp3_url, audio_path): 
  print 'running main'
#  features = process_audio(audio_path)
  features = [1,2,3]

  # Store feature vector in Firebase
  fb = firebase.FirebaseApplication('https://vinder.firebaseio.com', None)
  fb.post('users/',  {'features': features,
                     'user_hash': user_hash,
                     'mp3_url': mp3_url})


if __name__ == '__main__':
  main(sys.argv[1], sys.argv[2], sys.argv[3])
