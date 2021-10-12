var express   = require('express');
var router    = express.Router();
var mongoose  = require('mongoose');
var FDDresult = require('../models/result');

// Index
router.get('/',
  function(req, res, next){
    var query = {};
    if(req.query.name) query.name = {$regex:req.query.name, $options:'i'};

    FDDresult.find(query)
    .sort({date: -1})
    .exec(function(err, results){
      if(err) {
        res.status(500);
        res.json({success:false, message:err});
      }
      else {
        res.json({success:true, data:results});
      }
    });
  }
);

// Show
router.get('/:id',
  function(req, res, next){
    FDDresult.findOne({id:req.params.id})
    .exec(function(err, result){
      if(err) {
        res.status(500);
        res.json({success:false, message:err});
      }
      else if(!result){
        res.json({success:false, message:"FDD result not found"});
      }
      else {
        res.json({success:true, data:result});
      }
    });
  }
);

// Create
router.post('/',
  function(req, res, next){
    var newFDD = new FDDresult(req.body);
    newFDD.save(function(err, result){
      if(err) {
        res.status(500);
        res.json({success:false, message:err});
      }
      else {
        res.json({success:true, data:result});
     }
    });
  }
);

// Update
router.put('/:id',
  function(req, res, next){
    FDDresult.findOneAndUpdate({id:req.params.id}, req.body)
    .exec(function(err, result){
      if(err) {
        res.status(500);
        res.json({success:false, message:err});
      }
      else if(!result){
        res.json({success:false, message:"FDD result not found"});
      }
      else {
        res.json({success:true});
      }
    });
  }
);

// Destroy
router.delete('/:id',
  function(req, res, next){
    FDDresult.findOneAndRemove({id:req.params.id})
    .exec(function(err, result){
      if(err) {
        res.status(500);
        res.json({success:false, message:err});
      }
      else if(!result){
        res.json({success:false, message:"FDD result not found"});
      }
      else {
        res.json({success:true});
      }
    });
  }
);

module.exports = router;