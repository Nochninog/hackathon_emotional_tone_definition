import styles from './upload-modal.module.scss'
import FileArea from '../file-area/FileArea';
import Button from '../button/Button';
import { use, useState } from 'react';
import UploadService from '../../API/UploadService';



function UploadModal({setIsModalActive}){
    const [dataFile, setDataFile] = useState(null);
    const [hasValidation, setHasValidation] = useState(false);



    const handleUpload = async () => {
        const formData = new FormData();
        if (dataFile) 
            formData.append("upload_file", dataFile);
        
        formData.append("has_validation", hasValidation)
       
        const result = await UploadService.create_upload(formData)
    };


    return(
        <div className={styles['upload-modal-container']}> 
            <div className={styles['upload-modal']}>
                <div className={styles['modal-header']}>
                    <h2> Загрузите данные для анализа</h2>
                    <button className={styles['button-close']} onClick={() => setIsModalActive(false)}>
                        <img src="close.svg" alt="" />
                    </button>
                </div>

                <div className={styles['file-area-container']}>
                    <FileArea onFileSelect={setDataFile}>Загрузить данные</FileArea>
                    <label className={styles['checkbox-label']}>
                        <input type="checkbox" onChange={() => setHasValidation(true)}/>
                        Данные содержат валидацию
                    </label>
                    <Button onClick={() =>{handleUpload(); setIsModalActive(false); }}>Загрузить</Button>
                </div>
               
                
            </div>
        </div>
       
    );
}

export default UploadModal;
