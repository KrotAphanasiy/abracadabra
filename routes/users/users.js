const express = require('express');

const router = express.Router();

const { wrapRouter, } = require('../../utils');

const userController = require('./users.controller');

router.get('/vk', wrapRouter(userController.getVkUsers));

router.post('/file', wrapRouter(userController.createFileForPython));

router.post('/vk-info', wrapRouter(userController.getMoreInfoAboutVkUser));

module.exports = router;
