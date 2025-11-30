import styles from "../assets/ReviewsAnalysis.module.scss";
import { useParams} from "react-router-dom";
import UploadService from "../API/UploadService";
import { useState, useEffect } from "react";
import Badge from "../components/badge/Badge";
import SourcePanel from "../components/source-panel/SourcePanel";
import PieChart from "../components/chart/PieChart";

function ReviewAnalysis(){
    const {id} = useParams();
    const [upload, setUpload] = useState(null);
    const [tones, setTones] = useState(null);
    const [progress, setProgress] = useState(null);
    const [sources, setSources] = useState(null);

    async function fetchData() {
            const data = await UploadService.get_file_by_id(id);
            setUpload(data);
            
            const tones = await UploadService.get_tones(id);
            setTones(tones);

            const sources = await UploadService.get_sources(id);
            setSources(sources);

            const progress = await UploadService.get_progress(id);
            setProgress(progress);
        }

    useEffect(() => {
        fetchData();
    }, [id]);


    return(
        <main>
            <div className={styles['header-container']}>
                <h1>АНАЛИЗАТОР ТОНАЛЬНОСТИ ОТЗЫВОВ</h1>
            </div>
            <div className={styles['chart-info-container']}>
                <div className={styles['info-container']}>
                    {upload && 
                    <div className={styles['filename']}>{upload[0].filename} </div>}
                    {upload && 
                    <div className={styles['uploaded-at']}>{upload[0].uploaded_at} </div>}
                    {upload && 
                    <Badge big={true} status={upload[0].status}></Badge>}
                    <div className={styles['sources-container']}>
                        <h2>Источники</h2>
                        <SourcePanel sources={sources}></SourcePanel>
                    </div>
                </div >
                <div className={styles['chart-container']}>
                   {tones && <PieChart positive={tones.positive} negative={tones.negative} neutral={tones.neutral} title="Распределение тональности отзывов">
                    </PieChart>}
                </div>
                
                
            </div>
        </main>
    );
}

export default ReviewAnalysis;