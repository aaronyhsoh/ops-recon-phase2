import AppWrapper from './AppWrapper'
import Button from './Button'

import styles from './FileUploadApp.module.css'

// in charge of checking if the file dates are the same, and will highlight if not. will only do so
// after all required files are uploaded.
// takes in each fileupload as a children.
// 
export default function FileUploadApp({ title, checkDate, isAllUploaded, children }) {
    return (
        <AppWrapper title={title}>
            <div className={styles.fileUploadApp}>
                {children}
            </div>
            <div className={styles.buttonWrapper}>
                <Button onClick={checkDate} disabled={!isAllUploaded}>对账</Button>
            </div>
        </AppWrapper>
    )
}
