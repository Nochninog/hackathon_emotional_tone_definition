import styles from './badge.module.scss'

function Badge({status, big=false}){
    const data_badge = {"processing": ["В работе", "#542DFF",  "#542DFF"], "done": ["Готово","#41CA02", "#39B202"], "error":["Ошибка", "#D32044", "#E12A43"]}

    const [text, bgColorHex, textColor] = data_badge[status];
    return(
        <div 
        className={styles['badge'] + " " + (big ? styles['big'] : "")} 

        style={{
            backgroundColor: hexToRgba(bgColorHex, 0.33),
            color: textColor
        }}>
        {text}
        </div>
    );
}

function hexToRgba(hex, alpha) {
    const r = parseInt(hex.slice(1, 3), 16);
    const g = parseInt(hex.slice(3, 5), 16);
    const b = parseInt(hex.slice(5, 7), 16);
    return `rgba(${r}, ${g}, ${b}, ${alpha})`;
}

export default Badge;