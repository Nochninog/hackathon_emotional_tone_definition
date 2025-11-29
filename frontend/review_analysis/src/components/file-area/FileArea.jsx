import { useState, useRef, useId } from 'react';
import styles from './file-area.module.scss'


function FileArea({children, onFileSelect}){

    const [fileName, setFileName] = useState(null);
    const fileInputRef = useRef(null);

    const handleFileChange = (e) => {
        const file = e.target.files[0];
        if (file){
            onFileSelect(file);
            setFileName(file.name)
        }
    }

    const handleButtonClick = (e) => {
        e.preventDefault();
        e.stopPropagation();
        setFileName(null);
        onFileSelect(null); 

        if (fileInputRef.current) {
            fileInputRef.current.value = "";
        }
    };

    const truncateFileName = (name, maxLength = 20) => {
        if (name.length <= maxLength) 
            return name;
        return name.substring(0, maxLength) + '...';
    };

    let inputId = useId();

    return(
        fileName ? 
        <div className={styles['file-area']}>
            <img className={styles['file-area-img']} src="../../public/input_file.svg" alt="" />
            
                <div className={styles['file-name-container']}>
                    {truncateFileName(fileName)}
                    <button className={styles['file-name-button']} onClick={handleButtonClick}>
                        <img src="../../public/close.svg" height={20} alt="" />
                    </button>
                </div>
        
            <input 
                type="file" 
                className={styles['file-input']}
                onChange={handleFileChange}
                ref={fileInputRef}
                id={inputId}
            />
            
        </div>
        :
        <label className={styles['file-area']}>
            <img className={styles['file-area-img']} src="../../public/input_file.svg" alt="" />
            
                <h3>{children}</h3>
        
            <input 
                type="file" 
                className={styles['file-input']}
                onChange={handleFileChange}
                ref={fileInputRef}
                id={inputId}
            />
            
        </label>
    );
}

export default FileArea;
