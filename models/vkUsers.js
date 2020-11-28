const mongoose = require('mongoose');

const { Schema, } = mongoose;

const VkUserSchema = new Schema({
  vkId: {
    type: String,
    // unique: true,
    // lowercase: true,
    trim: true,
  },
  avatar: {
    type: String,
  },
}, {
  versionKey: false,
});

const VkUser = mongoose.model('vkUsers', VkUserSchema);

module.exports = VkUser;
