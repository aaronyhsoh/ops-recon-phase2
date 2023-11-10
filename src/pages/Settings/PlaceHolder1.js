import { useState } from "react";

import styles from './PlaceHolder.module.css'
import Button from "../../components/Button";

export default function PlaceHolder1() {

    const [code, setCode] = useState('');
    const [number, setNumber] = useState('');    
    const [updated, setUpdated] = useState(false)

    const handleCodeChange = (event) => {
        setCode(event.target.value);
    };
    
    const handleNumberChange = (event) => {
        setNumber(event.target.value);
    };
  

    async function UploadValue(){
        const formData = new FormData();
        formData.append('Code', code);
        formData.append("Number", number);
        try {
            const response = await fetch("http://127.0.0.1:5000/placeholder1", {
                method: "POST",
                body: formData,
            })
            const result = await response.json()
            if(result.status==="updated"){
                showUpdateTimer();
                setCode('');
                setNumber('');
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
                        Code
                    </div>
                    <input className={styles.long} type="text" value={code} id="Code" onChange={handleCodeChange} autoComplete="off" />
                </div>
                <div className={styles.marginRight}>
                    <div className={styles.inputTitle}>
                        Number
                    </div>
                    <input className={styles.long} type="text" value={number} id="Number" onChange={handleNumberChange} autoComplete="off" />
                </div>
               <Button disabled={!code || !number} onClick={UploadValue}>
                    更新
                </Button>
            </div>
            {updated && <div className={styles.updated}>Updated!</div>}
        </>
    )
}
