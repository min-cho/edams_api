var mongoose = require('mongoose');

var FDDSchema = mongoose.Schema({
  detectionID: {
    type: String,
    required: true,
  },
  date: {
    type: String,
    required: true,
  },
  buildingID: {
    type: String,
    required: true,
  },
  facilityID: {
    type: String,
    required: true,
  },
  impact: {
    type: Number,
    required: true,
  },
  reduction: {
    type: Number,
    required: true,
  },
  code: {
    type: String,
    required: true,
  },
  breif: {
    type: String,
    required: true,
  },
  check: {
    type: String,
    required: true,
  }
});

var FDDresult = mongoose.model('result', FDDSchema);
module.exports = FDDresult;
