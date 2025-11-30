import { useState, useEffect, useRef} from "react";
import styles from "../assets/MainPage.module.scss";
import '../assets/global.scss'
import Button from "../components/button/Button";
import UploadModal from "../components/upload-modal/UploadModal";
import Input from "../components/input/Input";
import UploadsPanel from "../components/uploads-panel/UploadsPanel";
import UploadService from "../API/UploadService";

export default function MainPage() {

  const [isModalActive, setIsModalActive] = useState(false);
  const [search, setSearch] = useState("");

  const [uploads, setUploads] = useState([])
  async function loadUploads() {
          try {
              const data = await UploadService.get_all_files(search);
              setUploads(data); 
          } catch (error) {
              console.error("Ошибка при загрузке файлов:", error);
          }
      }

  useEffect(() => {
      loadUploads();
  }, [isModalActive, search]);

  const intervalRef = useRef();
  useEffect(() => {
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
    }
    intervalRef.current = setInterval(() => loadUploads(), 1000);
  }, []);

  return (
    <main>
      <div className={styles['header-container']}>
        <Link to="/"><h1>АНАЛИЗАТОР ТОНАЛЬНОСТИ ОТЗЫВОВ</h1></Link>
      </div>

      <div className={styles['upload-status-container']}>
        <div className={styles['upload-container']}>
            <div className={styles['search']}><Input onChange={(e) => setSearch(e.target.value)}/></div>
            <Button onClick={() => setIsModalActive(true)}>Загрузить данные</Button>
            
        </div>

        <div className={styles['status-panel-container']}>
            <UploadsPanel uploads={uploads}>
                
            </UploadsPanel>        
        </div>
      </div>

      {isModalActive &&
        <UploadModal setIsModalActive={setIsModalActive} >
          
        </UploadModal>
      }

      
    </main>
  );
}
