var express = require('express');
var bodyParser = require('body-parser');
var Firebase = require('firebase');
var PythonShell = require('python-shell');
var multer = require('multer');
var fs = require('fs');
var util = require('util');

var app = express();
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
app.use(multer({ dest: './uploads'}));

app.post('/recieve_mp3', function(req, res) {
  var url = '';
  var fb = new Firebase('https://vinder.firebaseio.com/');
  var post_user = fb.child('users');
  var user_ref_path = post_user.push({
    mp3_url: url
  }); 

  var audio = 5;

  var text = req.body.
  var options = {
    mode: 'text',
    args: [audio, 'user_id']
  };
  
  PythonShell.run('process_audio.py',options, function (err) {
    if (err) throw err;
    // results is an array consisting of messages collected during execution
    console.log('Successfully ran python script');
  });
  
  console.log(user_ref_path.path['o'][1]);
  res.send(user_ref_path.path['o'][1]);
});



app.listen(5000);
console.log('Listening on port 5000...');

