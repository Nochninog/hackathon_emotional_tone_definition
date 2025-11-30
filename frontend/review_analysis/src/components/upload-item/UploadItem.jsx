import styles from './upload-item.module.scss'
import MutedText from '../muted-text/MutedText';
import {Link} from "react-router-dom";
import Badge from '../badge/Badge';


function UploadItem({name, uploaded_at, status, upload_id}){
    const truncateFileName = (name, maxLength = 20) => {
        if (name.length <= maxLength) 
            return name;
        return name.substring(0, maxLength) + '...';
    };


    return(
        <div className={styles['upload-item']}>
            <div className={styles['upload-item-column']}>
                <div className={styles['file-column']}>
                    <MutedText>
                        <img src="file.svg" alt="" />{name}
                    </MutedText>
                </div>
            </div>
            <div className={styles['upload-item-column']}>
                <div className={styles['uploaded-at-column']}>
                    <MutedText>
                        {uploaded_at}
                    </MutedText>
                </div>
            </div>
           
            <div className={styles['upload-item-column']}>
                <div className={styles['status-column']}>
                    <Badge 
                    status={status}
                ></Badge>
                </div>
            </div>
            <div className={styles['upload-item-column']}>
                <div className={styles['link-column']}>
                    <Link className={styles['link']} to={`/reviews-analysis/${upload_id}`}>
                    <MutedText>
                        <img src="eye.svg" alt="" />
                        Посмотреть
                    </MutedText>
                </Link>
                </div>
            </div>    
        </div>
    );
}

export default UploadItem;