var express = require('express');
var bodyParser = require('body-parser');
var Firebase = require('firebase');

var app = express();
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

app.post('/recieve_mp3', function(req, res) {
  var url = '';
  var fb = new Firebase('https://vinder.firebaseio.com/');
  var post_user = fb.child('users');
  post_user.push({
    mp3_url: url
  }); 

  res.send('Added mp3 url to firebase.');
});

app.listen(5000);
console.log('Listening on port 3000...');

