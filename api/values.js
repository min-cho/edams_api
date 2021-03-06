var express   = require('express');
var router    = express.Router();
var mongoose  = require('mongoose');
var RAWvalue = require('../models/value');

// Index
router.get('/',
  function(req, res, next){
    var query = {};
    if(req.query.name) query.name = {$regex:req.query.name, $options:'i'};

    RAWvalue.find(query)
    .sort({date: -1})
    .exec(function(err, values){
      if(err) {
        res.status(500);
        res.json({success:false, message:err});
      }
      else {
        res.json({success:true, data:values});
      }
    });
  }
);

// Show
router.get('/:detectionID',
  function(req, res, next){
    RAWvalue.findOne({detectionID:req.params.detectionID})
    .exec(function(err, value){
      if(err) {
        res.status(500);
        res.json({success:false, message:err});
      }
      else if(!value){
        res.json({success:false, message:"RAW DATA not found"});
      }
      else {
        res.json({success:true, data:value});
      }
    });
  }
);

// Create
router.post('/',
  function(req, res, next){
    var newvalue = new RAWvalue(req.body);
    newvalue.save(function(err, value){
      if(err) {
        res.status(500);
        res.json({success:false, message:err});
      }
      else {
        res.json({success:true, data:value});
     }
    });
  }
);

// Destroy
router.delete('/:detectionID',
  function(req, res, next){
    RAWvalue.findOneAndRemove({detectionID:req.params.detectionID})
    .exec(function(err, value){
      if(err) {
        res.status(500);
        res.json({success:false, message:err});
      }
      else if(!value){
        res.json({success:false, message:"RAW DATA not found"});
      }
      else {
        res.json({success:true});
      }
    });
  }
);

module.exports = router;