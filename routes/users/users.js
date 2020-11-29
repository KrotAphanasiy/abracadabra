const express = require('express');

const router = express.Router();

const { wrapRouter, } = require('../../utils');

const userController = require('./users.controller');

router.get('/vk', wrapRouter(userController.getVkUsers));

router.post('/file', wrapRouter(userController.createFileForPython));

router.get('/vk-info', wrapRouter(userController.getMoreInfoAboutVkUser));

router.post('/script', wrapRouter(userController.runPythonScript));

module.exports = router;
