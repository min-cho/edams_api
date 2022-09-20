var mongoose = require('mongoose');

var ValueSchema = mongoose.Schema({
  detectionID: {type: String, required: true},
  var_names: [],
  var_data: [{
    time:{type:String}, 
    v1:{type:Number}, 
    v2:{type:Number}, 
    v3:{type:Number}, 
    v4:{type:Number}
  }]
  });

var RAWvalue = mongoose.model('value', ValueSchema);
module.exports = RAWvalue;
