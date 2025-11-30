import styles from './upload-panel.module.scss'
import UploadItem from '../upload-item/UploadItem';


function UploadsPanel({uploads}){

    return(
        <div className={styles['uploads-panel']}>
            <div className={styles['file-info-header']}>
                <p className={styles['file-info-title']}>Файл</p>
                <p className={styles['file-info-title']}>Дата загрузки</p>
                {/* <p className={styles['file-info-title']}>Статистика по файлу</p> */}
                <p className={styles['file-info-title']}>Статус обработки</p>
                <p className={styles['file-info-title']}>Просмотр</p>
            </div>
            <div className={styles['uploads-container']}>{uploads.map(upload => 
            <UploadItem 
                name={upload.filename} 
                uploaded_at={upload.uploaded_at}
                // file_statistics={"upload.file_statistics"}
                status={upload.status}
                upload_id={upload.upload_id}
            />
            )}</div>
            
            
        </div>
    )
}

export default UploadsPanel;