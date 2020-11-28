const axios = require('axios');
const fs = require('fs');

const { responseGenerator, } = require('../../utils/index');

const query = require('./users.query');

const { ACCESS_TOKEN_VK, } = process.env;

const url = 'https://api.vk.com/method/users.search'
  + '?age_from=18'
  + '&fields=photo_400_orig'
  + '&has_photo=1&count=300'
  + '&offset=0'
  + `&access_token=${ACCESS_TOKEN_VK}&v=5.126`;

const optionsVkApi = {
  method: 'POST',
  url,
};

module.exports = {

  async getVkUsers(req, res, next) {
    // const {
    //   id,
    // } = req.user;
    // const data = await query.getUser(id, req.user.roleId);

    req.setTimeout(500000);

    const { data: { response: { items, }, }, } = await axios(optionsVkApi);

    console.info('items ', items.length);

    try {
      const vkUsers = await Promise.all(
        items.map(async ({ id = '', photo_400_orig = '', }, index) => {
          console.info('index Response ', index);

          if (photo_400_orig) {
            const image = await axios({
              method: 'GET',
              url: photo_400_orig,
              responseType: 'arraybuffer',
            });

            const returnedBase64 = Buffer.from(image.data).toString('base64');

            return { vkId: id, avatar: returnedBase64, };
          }
          return { vkId: id, avatar: photo_400_orig, };
        })
      );

      const result = await query.saveVkUsers(vkUsers);

      responseGenerator(res, 200, result);
    }
    catch (e) {
      console.info('e ', e);
    }
  },

  async createFileForPython(req, res, next) {
    req.setTimeout(500000);

    const vkUsers = await query.getAllUsers();

    console.info('vkUsers ', vkUsers.length);

    const data = JSON.stringify(vkUsers);
    await fs.writeFile('vkUsers.json', data, (err) => {
      if (err) throw err;
      console.log('Data written to file');
    });

    responseGenerator(res, 200, 'ok');
  },

  async getMoreInfoAboutVkUser(req, res, next) {

    const vkUsers = await query.getAllUsers();

    console.info('vkUsers ', vkUsers.length);

    fs.readFile('IdVK.json', (err, data) => {
      if (err) throw err;
      const id = JSON.parse(data);
      console.log('id', id);
    });

    responseGenerator(res, 200, 'ok');
  },
};
