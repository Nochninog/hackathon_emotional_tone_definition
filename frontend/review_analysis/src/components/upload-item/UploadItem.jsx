import styles from './upload-item.module.scss'
import MutedText from '../muted-text/MutedText';
import {Link} from "react-router-dom";
import Badge from '../badge/Badge';


function UploadItem({name, uploaded_at, file_statistics, status, upload_id}){
    return(
        <div className={styles['upload-item']}>
            <div className={styles['upload-item-column']}>
                <MutedText>
                    <img src="../../public/file.svg" alt="" />{name}
                </MutedText>
            </div>
            <div className={styles['upload-item-column']}>
                <MutedText>
                    {uploaded_at}
                </MutedText>
            </div>
            <div className={styles['upload-item-column']}>
                <MutedText>
                {file_statistics}
                </MutedText>
            </div>
            <div className={styles['upload-item-column']}>
                {status}
            </div>
            <div className={styles['upload-item-column']}>
                <Link className={styles['link']} to="/reviews-analysis">
                    <MutedText>
                        <img src="../../public/eye.svg" alt="" />
                        {upload_id}
                    </MutedText>
                </Link>
            </div>    
        </div>
    );
}

export default UploadItem;