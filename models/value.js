var mongoose = require('mongoose');

var FDDSchema = mongoose.Schema({
  detectionID: {
    type: String,
    required: true,
  },
  time: {
    type: Date,
    required: true,
  },
  data: {
    type: Array,
    required: true,
  }
});

var FDDresult = mongoose.model('result', FDDSchema);
module.exports = FDDresult;