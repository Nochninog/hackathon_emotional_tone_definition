import { useState } from "react";
import styles from "../assets/MainPage.module.scss";
import '../assets/global.scss'
import Button from "../components/button/Button";
import UploadModal from "../components/upload-modal/UploadModal";
import Input from "../components/input/input";
import UploadsPanel from "../components/uploads-panel/UploadsPanel";

export default function MainPage() {

  const [isModalActive, setIsModalActive] = useState(false);


  return (
    <main>
      <div className={styles['header-container']}>
        <h1>АНАЛИЗАТОР ТОНАЛЬНОСТИ ОТЗЫВОВ</h1>
      </div>

      <div className={styles['upload-status-container']}>
        <div className={styles['upload-container']}>
            <div className={styles['search']}><Input/></div>
            <Button onClick={() => setIsModalActive(true)}>Загрузить данные</Button>
            
        </div>

        <div className={styles['status-panel-container']}>
            <UploadsPanel>
                
            </UploadsPanel>        
        </div>
      </div>

      {isModalActive &&
        <UploadModal setIsModalActive={setIsModalActive}>
          
        </UploadModal>
      }

      
    </main>
  );
}
