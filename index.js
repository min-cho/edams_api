var express    = require('express');
var app        = express();
var path       = require('path');
var mongoose   = require('mongoose');
var bodyParser = require('body-parser');
const PORT = process.env.PORT || 5000;

// Database
mongoose.Promise = global.Promise;
mongoose.connect('mongodb+srv://admin_mrplan:mrplan@cluster0.8geiv.mongodb.net/Cluster0?retryWrites=true&w=majority');
var db = mongoose.connection;

db.once('open', function () {
   console.log('DB connected!');
});
db.on('error', function (err) {
  console.log('DB ERROR:', err);
});


// Middlewares
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: true}));
app.use(function (req, res, next) {
  res.header('Access-Control-Allow-Origin', '*');
  res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE');
  res.header('Access-Control-Allow-Headers', 'content-type');
  next();
});

// API
app.use('/api/results', require('./api/results'));
app.use('/api/values', require('./api/values'));

// Heroku Setting
app.get('/', function(req, res){
  res.send('Welcome to [EDAM-S] provided by [MRPLAN]. You can use the REST API through this domain');
});

// Port setting
//var port = 3000;
//app.listen(port, function(){
//  console.log('server on! http://localhost:'+port);
//});