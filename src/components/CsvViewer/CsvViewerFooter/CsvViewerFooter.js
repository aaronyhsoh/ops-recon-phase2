import Button from '../../Button'
import styles from './CsvViewerFooter.module.css'

export default function CsvViewerFooter({ resetData, downloadData }) {
    return (
        <div className={styles.viewerfooter}>
            <Button onClick={resetData}>恢复</Button>
            <Button onClick={downloadData}>下载</Button>
        </div>
    )
}
