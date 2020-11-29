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

    const {
      data: {
        response: {
          items,
        },
      },
    } = await axios(optionsVkApi);

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

      await query.saveVkUsers(vkUsers);

      responseGenerator(res, 200, 'ok');
    }
    catch (e) {
      console.info('e ', e);
    }
  },

  async createFileForPython(req, res, next) {
    req.setTimeout(500000);

    const vkUsers = await query.getAllUsers();

    const data = JSON.stringify(vkUsers);
    await fs.writeFile('vkUsers.json', data, (err) => {
      if (err) throw err;
      console.log('Data written to file');
    });

    responseGenerator(res, 200, 'ok');
  },

  async getMoreInfoAboutVkUser(req, res, next) {
    fs.readFile('IdVK.json', async (err, data) => {
      if (err) throw err;
      const { vkId = '', } = JSON.parse(data);
      console.info('vkData ', vkId);

      if (!vkId) responseGenerator(res, 404, 'User not found');

      const optionVkSearch = {
        url: 'https://api.vk.com/method/users.get?'
          + `user_ids=${vkId}`
          + '&fields=education,bdate,career,city'
          + `&access_token=${ACCESS_TOKEN_VK}&v=5.126`,

      };
      const {
        data: {
          response = [],
        },
      } = await axios(optionVkSearch);

      responseGenerator(res, 200, response[0]);
    });
  },

  async runPythonScript(req, res, next) {
    try {
      console.info('123 ', req.body.base64);

      const { base64 = '', } = req.body;

      const optionPythonRequest = {
        method: 'POST',
        url: 'http://192.168.43.17:3002/python-script',
        data: {
          base64,
        },

      };
      const { data = false, } = await axios(optionPythonRequest);
      console.info('data', data);

      if (!data) responseGenerator(res, 404, 'Пользователь не найден');

      // const optionVkSearch = {
      //   url: 'https://api.vk.com/method/users.get?'
      //     + `user_ids=${1}`
      //     + '&fields=education,bdate,career,city'
      //     + `&access_token=${ACCESS_TOKEN_VK}&v=5.126`,
      //
      // };
      // const {
      //   data: {
      //     response = [],
      //   },
      // } = await axios(optionVkSearch);
      //
      // responseGenerator(res, 200, response[0]);
      //
      //
      // console.info('data ', data);

      // const python = spawn('python', ['./python/findFace.py']);
      // // collect data from script
      // python.stdout.on('data', (data) => {
      //   console.log('Pipe data from python script ...');
      //   console.info('data.toString() ', data.toString());
      // });
      // // in close event we are sure that stream from child process is closed
      // python.on('close', (code) => {
      //   console.log(`child process close all stdio with code ${code}`);
      //   // send data to browser
      // });

      // responseGenerator(res, 200, 'ok');
    }
    catch (e) {
      console.info('error ', e);
    }
  },
};
