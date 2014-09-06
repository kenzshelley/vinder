// Requires
var fs = require('node-fs');
var express = require('express');
var bodyParser = require('body-parser');
var AWS = require('aws-sdk');
	AWS.config.update({region: 'us-east-1'});
	AWS.config.update({accessKeyId: 'AKIAIM327M75R4YK5VAA', secretAccessKey: '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'});
var s3 = require('s3');
var md5 = require('MD5');
// var client = s3.createClient({
//   maxAsyncS3: 20,     // this is the default
//   s3RetryCount: 3,    // this is the default
//   s3RetryDelay: 1000, // this is the default
//   multipartUploadThreshold: 20971520, // this is the default (20 MB)
//   multipartUploadSize: 15728640, // this is the default (15 MB)
//   s3Options: {
//     accessKeyId: "AKIAIM327M75R4YK5VAA",
//     secretAccessKey: "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",
//     // any other options are passed to new AWS.S3()
//     // See: http://docs.aws.amazon.com/AWSJavaScriptSDK/latest/AWS/Config.html#constructor-property
//   },
// });

// var params = {
//   localFile: "test_recording.wav",

//   s3Params: {
//     Bucket: "audio_from_users",
//     Key: "hash"

//     // other options supported by putObject, except Body and ContentLength.
//     // See: http://docs.aws.amazon.com/AWSJavaScriptSDK/latest/AWS/S3.html#putObject-property
//   },
// };
// var uploader = client.uploadFile(params);
// uploader.on('error', function(err) {
//   console.error("unable to upload:", err.stack);
// });
// uploader.on('progress', function() {
//   console.log("progress", uploader.progressMd5Amount,
//             uploader.progressAmount, uploader.progressTotal);
// });
// uploader.on('end', function() {
//   console.log("done uploading");
//   var params = {Bucket: 'audio_from_users', Key: 'hash'};
//   var s3 = new AWS.S3(); 
//   s3.getSignedUrl('getObject', params, function(err, url) {
//   	return url; 
//   });
//   // var params = {Bucket: 'audio_from_users', Key: 'hash'};
//   // var url = s3.getSignedUrl('getObject', params);
//   // console.log("The URL is", url);
// });

var username = 'santoshm@umich.edu';
var hash = md5(username);
console.log(hash);


var app = express();
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

app.post('/receive_mp3', function(req, res) {

	
});

app.listen(5000);
console.log('Listening on port 5000...');
