var express = require('express');
var bodyParser = require('body-parser');
var $ = require('jquery'),
    XMLHttpRequest = require()

var app = express();
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

app.post('/recieve_mp3', function(req, res) {
    console.log("Hello");
    res.send("test");
});

app.listen(5000);
console.log('Listening on port 3000...');
