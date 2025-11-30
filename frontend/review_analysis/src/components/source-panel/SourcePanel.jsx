import styles from './source-panel.module.scss'
import SourceItem from '../source_item/SourceItem';

function SourcePanel(){
    return(
        <div className={styles['source-panel']}>
            <SourceItem>perekryastok</SourceItem>
            <SourceItem>perek</SourceItem>
            <SourceItem>pekryastok</SourceItem>
            <SourceItem>perekryastok</SourceItem>
            <SourceItem>perekryastok</SourceItem>
            <SourceItem>peok</SourceItem>
            <SourceItem>perekryastok</SourceItem>
            <SourceItem>perryastok</SourceItem>
            <SourceItem>perek</SourceItem>
            <SourceItem>peyastok</SourceItem>
        </div>
    );
}

export default SourcePanel;