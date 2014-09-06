var express = require('express');
var bodyParser = require('body-parser');
var multer = require('multer');
var fs = require('fs');
var util = require('util');

var app = express();
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
app.use(multer({ dest: './uploads'}));

app.get('/', function(req,res){
    res.send('Hello world');
});
app.post('/upload', function(req, res) {
        console.log('POST /upload');
        if (req.files) { 
            console.log(util.inspect(req.files));
            fs.exists(req.files.sound_data.path, function(exists) { 
                if(exists) { 
                    res.send("Got your file!"); 
                } else { 
                    res.send("Didn't get your file"); 
                } 
            }); 
        } else {
            res.send('no files found');
        }
});
app.listen(3000);
console.log('Listening on port 3000...');
