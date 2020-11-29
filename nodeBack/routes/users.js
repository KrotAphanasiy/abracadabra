var express = require('express');
var router = express.Router();

/* GET users listing. */
router.get('/python-script', function(req, res, next) {


  console.log(123213);
  res.send('respond with a resource');
});

module.exports = router;
