import React, {
  useState,
  useCallback,
  memo,
  useEffect,
  useMemo,
} from 'react';
import { Button, IconButton, CircularProgress } from "@material-ui/core";
import PhotoCamera from '@material-ui/icons/PhotoCamera';

import AvatarDefault from '../../assets/image/default.jpeg';

import { uploadPhoto, getInfoFromVkApi } from '../../utils/api';

import styles from './UploadFIle.module.scss';

const serializeField = {
  'first_name': 'Имя',
  'last_name': 'Фамилия',
  'bdate': 'Дата рождения',
  'university_name': 'Университет',
  'faculty_name': 'Факультет',
}

const UploadFile = () => {
  const [base64Photo, setPhoto] = useState(null);
  const [userData, setUserData] = useState(null);
  const [errorInfo, setError] = useState(false);
  const [loader, setLoader] = useState(false);

  const photoHandler = useCallback((event) => {
    const photo = event.target.files[0];

    if (photo) {
      const reader = new FileReader();
      reader.readAsBinaryString(photo);

      reader.onload = function() {
        setPhoto(btoa(reader.result));
      };
      reader.onerror = function() {
        console.log('there are some problems');
      };
    }
  }, []);

  const uploadHandler = async () => {
    setLoader(true);
    const result = await uploadPhoto(base64Photo);

    if (typeof result === 'string') {
      setError(result);
    } else {
      setUserData(result)
    }
  }

  const imagePath = useMemo(() => (
    base64Photo
      ? `data:image/jpeg;base64,${base64Photo}`
      : AvatarDefault
    ), [base64Photo])

  useEffect(() => {
    const getData = async () => {
      const data = await getInfoFromVkApi()
      setUserData(data);

      const user = {}
      if (data) {
        Object.keys(data).map(item => {
          if(serializeField[item]) {
            console.info('item ', item);
            user[item] = data[item];
          }
        })
        setUserData(user);
      }
    }
    // getData();
  },[])

  console.info('userData ', userData);
  return (
    <div className={styles.uploadContainer}>
      <h3 className={styles.mainTitle}>
        Пожалуйста загрузите фото пользователя для идентификации
        финансового
        профиля из открытых источников
      </h3>
      <input
        type="file"
        hidden
        onChange={photoHandler}
        accept="image/*"
        id="file"
      />
      <label
        className={styles.photoLabel}
        htmlFor="file"
      >
        <IconButton
          color="secondary"
          aria-label="upload picture"
          component="span"
        >
          <PhotoCamera />
        </IconButton>
      </label>
      <img
        className={styles.userPhoto}
        src={imagePath}
      />
      {
        base64Photo && (
          <>
            <Button
              variant="contained"
              color="primary"
              className={styles.uploadButton}
              style={{
                marginTop: '50px',
              }}
              onClick={uploadHandler}
            >
              Загрузить фото для поиска данных
            </Button>
          </>
        )
      }
      {
        loader && (
          <div  className={styles.loaderWrapper}>
            <h3>Выполняется поиск</h3>
            <CircularProgress
              style={{
                padding: '50px',
              }}
            />
          </div>
        )
      }

      {
        userData && (
          <div className={styles.fieldWrapper}>
              {Object.keys(userData).map((fieldName, index) => {
                if (serializeField[fieldName]) {
                  return (
                    <div className={styles.fieldNameWrapper}>
                      <p>{serializeField[fieldName]}</p>
                      <p>{userData[fieldName]}</p>
                    </div>
                  )
                }
                return null
              })}
          </div>
        )
      }
    </div>
  )
}

export default memo(UploadFile);
