const VkUsers = require('../../models/vkUsers');

module.exports = {
  saveVkUsers(arrayUsers) {
    return VkUsers.insertMany(arrayUsers, (err, users) => {
      if (err) {
        console.info('vkUsers error ', err);
        return null;
      }

      return users;
    });
  },
  getAllUsers() {
    return VkUsers.find({}, {
      _id: 0,
      vkId: 1,
      avatar: 1,
    });
  },
};
