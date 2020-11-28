'use strict';

const mongoose = require('mongoose');

// Определяем схему


const NewsModel = new mongoose.Schema({
  userId: {
    required: true,
    type: String
  },
  nameArticle: {
    required: true,
    type: String,
  },
  textArticle: {
    required: true,
    type: String,
  },
  tagsArticle: {
    required: true,
    type: String,
  },
  userName: {
    required: true,
    type: String,
  },
  avatar: {
    required: true,
    type: String,
  }
},{
  versionKey: false
});

module.exports = mongoose.model('News', NewsModel);
