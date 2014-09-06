from flask import Flask
from firebase import firebase
app = Flask(__name__)

@app.route("/")
def main(): 
  print "yo"
  firebase = firebase.FirebaseApplication('https://vinder.firebaseio.com', None)
  print "hi"
  result = firebase.get('/Test', None)
  return result
#  return "Nothing"

if __name__ == "__main__":
  app.run()
