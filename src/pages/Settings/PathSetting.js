import { useContext, useState } from "react";
import AppWrapper from "../../components/AppWrapper";
import styles from './PathSetting.module.css'
import { AppContext } from "../../contexts/AppContext";
import Button from "../../components/Button";
import ErrorModal from "../../components/Modals/ErrorModal";

export default function PathSetting() {
    return (
        <>
            <AppWrapper title='Path Setting' titleAlign='left'>
                <PathSettingContent />
            </AppWrapper>
        </>
    )
}

function PathSettingContent() {
    const { folderPath, setFolderPath } = useContext(AppContext)
    const [updated, setUpdated] = useState(false)
    const [showErrorMsg, setShowErrorMsg] = useState(false)
    const [errorMsg, setErrorMsg] = useState('')

    async function handleClick(){
        const formData = new FormData();
        formData.append('folderPath', folderPath);
        try {
            const response = await fetch("http://127.0.0.1:5000/path_Settings", {
                method: "POST",
                body: formData,
            })
            const result = await response.json()
            if(result.status==="updated"){
                showUpdateTimer();
                setFolderPath('')
            } else {
                setShowErrorMsg(true)
                setErrorMsg(result.error)
            }
        } catch (error) {
            console.error("Error:", error)
        }
    };

    const showUpdateTimer= () => {
        setUpdated(true)
        setTimeout(() => setUpdated(false), 2000)
    }

    return (
        <>
            <ErrorModal show={showErrorMsg} setShow={setShowErrorMsg} message={errorMsg} />
            <div className={styles.container}>
                <div className={styles.flex}>
                    <div className={styles.marginRight}>
                        <div className={styles.inputTitle}>
                            Folder Path
                        </div>
                        <input className={styles.long} type="text" value={folderPath} onChange={e => setFolderPath(e.target.value)} autoComplete="off" />
                    </div>
                    <Button disabled={!folderPath} onClick={handleClick}>
                        Set
                    </Button>
                </div>
                <small className={styles.note}>Note: Copy and paste the absolute file path of your folder here.</small>
                {updated && <div className={styles.updated}>Updated!</div>}
            </div>
        </>
    )
}