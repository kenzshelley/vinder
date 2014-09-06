from firebase import firebase
import sys

def main(text, user_id): 
  print 'running main'
  # Convert process text file 
#  features = process_text(text)
  features = [1,2,3]

  # Store feature vector in Firebase
  fb = firebase.FirebaseApplication('https://vinder.firebaseio.com', None)
  fb.post('users/',  features)


if __name__ == '__main__':
  main(sys.argv[1], sys.argv[2])
