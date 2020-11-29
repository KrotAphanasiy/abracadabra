var express = require('express');
const { spawn } = require('child_process')

var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  const python = spawn('python', ['../findFace.py']);
  // collect data from script
  python.stdout.on('data', (data) => {
    console.log('Pipe data from python script ...');
    console.info('data.toString() ', data.toString());
  });
  // in close event we are sure that stream from child process is closed
  python.on('close', (code) => {
    console.log('child process close a ll stdio with code', code);
    // send data to browser
  });


  res.render('index', { title: 'Express' });
});

module.exports = router;