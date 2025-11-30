import styles from './muted-text.module.scss' 

function MutedText({children}){
    return(
        <div className={styles['muted-text']}>{children}</div>
    )
}

export default MutedText;