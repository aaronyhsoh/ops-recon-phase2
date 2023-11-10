import styles from './AppWrapper.module.css'

export default function AppWrapper({ title, titleAlign='center', children }) {
    return (
        <div className={styles.appWrapper}>
            <div className={`${styles.title} ${titleAlign === 'center' ? styles.titlecenter : titleAlign === 'left' ? styles.titleleft : ''}`}>
                {title}
            </div>
            {children}
        </div>
    )
}
