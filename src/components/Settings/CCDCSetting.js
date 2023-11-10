import { useState } from "react";

import styles from './CCDCSetting.module.css'
import Button from "../Button";

export default function CCDCSetting() {

    const [IBCode, setIBCode] = useState('');
    const [ISIN, setISIN] = useState('');    
    const [updated, setUpdated] = useState(false)

    const handleIBCodeChange = (event) => {
        setIBCode(event.target.value);
    };
    
    const handleISINChange = (event) => {
        setISIN(event.target.value);
    };
  

    async function UploadValue(){
        const formData = new FormData();
        formData.append('IBCode', IBCode);
        formData.append("ISIN", ISIN);
        try {
            const response = await fetch("http://127.0.0.1:5000/system_Settings", {
                method: "POST",
                body: formData,
            })
            const result = await response.json()
            if(result.status==="updated"){
                showUpdateTimer();
                setIBCode('');
                setISIN('');
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
            <div className={styles.flex}>
                <div className={styles.marginRight}>
                    <div className={styles.inputTitle}>
                        IB Code
                    </div>
                    <input className={styles.long} type="text" value={IBCode} id="IBCode" onChange={handleIBCodeChange} autoComplete="off" />
                </div>
                <div className={styles.marginRight}>
                    <div className={styles.inputTitle}>
                        ISIN
                    </div>
                    <input className={styles.long} type="text" value={ISIN} id="ISIN" onChange={handleISINChange} autoComplete="off" />
                </div>
               <Button disabled={!IBCode || !ISIN} onClick={UploadValue}>
                    更新
                </Button>
            </div>
            {updated && <div className={styles.updated}>Updated!</div>}
        </>
    )
}
