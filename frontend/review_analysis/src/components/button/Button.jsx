import { useState } from 'react';
import styles from './button.module.scss'

function Button({children, onClick}){

    return(
        <button className={styles["main-button"]} onClick={onClick}>
            {children}
        </button>
    );
}

export default Button;