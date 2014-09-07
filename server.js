// Requires
var fs = require('node-fs');
var express = require('express');
var bodyParser = require('body-parser');
var Firebase = require('firebase');
var PythonShell = require('python-shell');
var multer = require('multer');
var fs = require('fs');
var util = require('util');
var AWS = require('aws-sdk');
	AWS.config.update({region: 'us-east-1'});
	AWS.config.update({accessKeyId: 'AKIAIM327M75R4YK5VAA', secretAccessKey: '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'});
var s3 = require('s3');
var md5 = require('MD5');
 var client = s3.createClient({
   maxAsyncS3: 20,     // this is the default
   s3RetryCount: 3,    // this is the default
   s3RetryDelay: 1000, // this is the default
   multipartUploadThreshold: 20971520, // this is the default (20 MB)
   multipartUploadSize: 15728640, // this is the default (15 MB)
   s3Options: {
     accessKeyId: "AKIAIM327M75R4YK5VAA",
     secretAccessKey: "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",
     // any other options are passed to new AWS.S3()
     // See: http://docs.aws.amazon.com/AWSJavaScriptSDK/latest/AWS/Config.html#constructor-property
   },
 });


var app = express();
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
app.use(multer({ dest: './uploads'}));

app.post('/receive_mp3', function(req, res) {
  // Will be recieved in the request so that we can hash it
  var username = req.body.email_address;
  var hash = String(md5(username));
  console.log(hash);

  // Get the files from the req
  if (req.files) {
    console.log(util.inspect(req.files));
    fs.exists(req.files.sound_data.path, function(exists) {
      if (exists) {
        console.log("Got audio file!");
      } else {
        console.log("Didn't get audio file!");
      }
    });
  } else {
    console.log('no files found!');
  }
  var audio_path = './uploads/' + hash + '.wav';
  fs.rename(req.files.sound_data.path, audio_path);

  var params = {
    localFile: audio_path,

    s3Params: {
      Bucket: "audio_from_users",
      Key: hash 

     // other options supported by putObject, except Body and ContentLength.
     // See: http://docs.aws.amazon.com/AWSJavaScriptSDK/latest/AWS/S3.html#putObject-property
   },
  };
  var uploader = client.uploadFile(params);
  uploader.on('error', function(err) {
    console.error("unable to upload:", err.stack);
  });
  uploader.on('progress', function() {
    console.log("progress", uploader.progressMd5Amount,
             uploader.progressAmount, uploader.progressTotal);
  });

  var URL = '';
  // var url thing might be completely wrong
  uploader.on('end', function() {
  console.log("done uploading");
    var params = {Bucket: 'audio_from_users', Key: 'hash'};
    var s3 = new AWS.S3(); 
    s3.getSignedUrl('getObject', params, function(err, url) {
      URL = url; 
      console.log("just set url");
      console.log(url);
      console.log(URL);
      var new_audio_path = './uploads/' + hash + '.wav';
      var options = {
        mode: 'text',
        args: [new_audio_path]
      };
  
      PythonShell.run('process_audio.py',options, function (err, results) {
        if (err) throw err;
        // results is an array consisting of messages collected during execution
        console.log('Successfully ran python script');
        var temp_m = [1,2,3];
        var unparsed_features = results[results.length-1];
        var features = unparsed_features.split(', ');
        features[0] = features[0].substring(1);
        var last_el_length = features[features.length -1].length;
        features[features.length - 1] = features[features.length - 1].substring(0, last_el_length -1);
        for (var i = 0; i < features.length - 1; ++i) {
          features[i] = parseInt(features[i]); 
        }
        update_matches(features, hash, URL, username);
        
      });
    });
  });
  res.send(hash);
});

app.listen(process.env.PORT || 5000);
console.log('Listening on port 5000...');

function update_matches(features, user_hash, url, username) {
  var users_ref = new Firebase('https://vinder.firebaseio.com/users');
  var new_user_data = {'mp3_url' : url, 
                       'email' : username,
                       'features' : features,
                       'matches' : []};
  users_ref.child(user_hash).set(new_user_data);
  
  users_ref.once('value', function(vals) {
    for (var key in vals.val()) {
      if (key == user_hash) 
        continue; 
      var user = vals.val()[key];
      var cor = match(user['features'], features);
      console.log('cor: ' + cor);
      if (cor > .4) {
        if (!user['matches']) {
          console.log('matches does not exist');
          user['matches'] = [user_hash];
        } else {
          user['matches'].push(user_hash);
        }
        new_user_data['matches'].push(key); 
      }
      users_ref.child(key).set(user);
    }
  users_ref.child(user_hash).set(new_user_data);
    
  }, function(err) {
    console.log('done fucked up');
  });
  console.log("blah blah fuck firebase"); 
}

function match(features_1, features_2) {
  var result = [];
  for (var i = 0; i < features_1.length - 1; ++i) {
    var num1 = features_1[i];
    var num2 = features_2[i];
    var num = 1 - Math.abs(num1 - num2) / Math.abs(num1 + num2 + .0001);
    result.push(num);
  }
  var sum = 0;
  for (var i = 0; i < result.length - 1; ++i) {
    sum += result[i];
  }
  var avg = sum/(result.length - 1);
  return avg;
}






