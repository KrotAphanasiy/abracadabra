import axios from 'axios';

const { REACT_APP_API_URL } = process.env;

const uploadPhoto = async (photo) => {
  try {
    console.info('photo ', photo);
    const requestData = {
      method: 'POST',
      url: `/api/v1/users/script`,
      data: {
        base64: photo,
      },
    };

    const { data } = await axios(requestData);
    console.info('data ', data);
    return data;

  } catch (error) {
    console.info('error ', error);
    return 'Пользователь не найден'
  }
}

const getInfoFromVkApi = async () => {
  try {
    const requestData = {
      method: 'GET',
      url: `/api/v1/users/vk-info`,
    };

    const { data } = await axios(requestData);
    return data;
  } catch (error) {
    console.info('error ', error);
  }
}
export {
  uploadPhoto,
  getInfoFromVkApi
}
