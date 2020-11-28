import React, {
  useState,
  useCallback,
  memo
} from 'react';
import { Button, IconButton } from "@material-ui/core";
import PhotoCamera from '@material-ui/icons/PhotoCamera';

import styles from './UploadFIle.module.scss';

const UploadFile = () => {
  const [base64Photo, setPhoto] = useState(null);

  const photoHandler = useCallback((event) => {
    const photo = event.target.files[0];
    console.info('photo ', photo);

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
      {
        base64Photo && (
          <>
            <img
              className={styles.userPhoto}
              src={`data:image/jpeg;base64,${base64Photo}`}
            />
            <Button
              variant="contained"
              color="primary"
              className={styles.uploadButton}
              style={{
                marginTop: '50px',
              }}
            >
              Загрузить фото для поиска данных
            </Button>
          </>
        )
      }
    </div>
  )
}

export default memo(UploadFile);
