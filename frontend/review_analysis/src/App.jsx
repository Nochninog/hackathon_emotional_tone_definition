import { useState } from 'react'
import styles from "./assets/App.module.scss";
import './assets/global.scss'

function App() {
  return (
    <>
      <main>
        <div className={styles['header-container']}>
          <h1>АНАЛИЗАТОР ТОНАЛЬНОСТИ ОТЗЫВОВ</h1>
        </div>
        <div className={styles['upload-status-container']}>
          <div className={styles['upload-container']}>
              <input type="Введите название файла" />
              <button>Загрузить данные</button>
          </div>
          <div className={styles['status-panel-container']}>

          </div>
        </div>
        
      </main>
     
    </>
  )
}

export default App
