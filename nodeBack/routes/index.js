const express = require('express');
const { spawn } = require('child_process')
const fs = require('fs')

const execSync = require('child_process').execSync;


var router = express.Router();

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

/* GET home page. */
router.post('/python-script', async (req, res, next) => {
  const { base64 } = req.body
  const data = { photo: base64 }

  await fs.writeFile('arg.json', JSON.stringify(data), (err) => {
    if (err) throw err;
    console.log('Data written to file');
  });
  console.log(base64);
  //const python = spawn('python', ['../findFace.py']);
  code = execSync('python ../findFace.py');
  // collect data from script
  // python.stdout.on('data', async (data) => {
  //   console.log('Pipe data from python script ...');
  //   console.info('data.toString() ', data.toString());
  //   await sleep(50000);
  // });
  // // in close event we are sure that stream from child process is closed
  // python.on('close', (code) => {
  //   console.log('child process close a ll stdio with code', code);
  //   // send data to browser
  // });
  //
  //
  // res.send('ok').status(200);
});

module.exports = router;
