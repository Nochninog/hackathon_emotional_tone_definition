import styles from './upload-panel.module.scss'
import UploadItem from '../upload-item/UploadItem';
import { useState } from 'react';

function UploadsPanel(){
    const [uploads, setUploads] = useState([{
        file_name: "Анапа",
         uploaded_at: "2025-10-10 11:00",
        file_statistics:"256 fekkejfkf",
        status: "rgrgr",
        upload_id: 1,
    }])

    return(
        <div className={styles['uploads-panel']}>
            <div className={styles['file-info-header']}>
                <p className={styles['file-info-title']}>Файл</p>
                <p className={styles['file-info-title']}>Дата загрузки</p>
                <p className={styles['file-info-title']}>Статистика по файлу</p>
                <p className={styles['file-info-title']}>Статус обработки</p>
                <p className={styles['file-info-title']}>Просмотр</p>
            </div>
            {uploads.map(upload => 
            <UploadItem 
                name={upload.file_name} 
                uploaded_at={upload.uploaded_at}
                file_statistics={upload.file_statistics}
                status={upload.status}
                upload_id={upload.upload_id}
            />
            )}
            
        </div>
    )
}

export default UploadsPanel;