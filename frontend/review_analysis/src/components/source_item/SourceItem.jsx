import styles from './source-item.module.scss'

function SourceItem({children}){
    return(
        <div className={styles['source-item']}>
           {children}</div>
    );
}

export default SourceItem;