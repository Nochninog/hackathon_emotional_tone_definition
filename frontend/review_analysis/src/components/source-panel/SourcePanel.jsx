import styles from './source-panel.module.scss'
import SourceItem from '../source_item/SourceItem';

function SourcePanel({sources}){
    return(
        <div className={styles['source-panel']}>
            {sources && sources.map(source => 
                <SourceItem>{source}</SourceItem>
            )}
        </div>
    );
}

export default SourcePanel;