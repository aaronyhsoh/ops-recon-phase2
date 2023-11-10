import { useState } from 'react';
import CsvViewer from "../../components/CsvViewer/CsvViewer"
import TableSelector from "../../components/CsvViewer/TableSelector";
import Calender from "../../components/Calender";
import Button from "../../components/Button";
import styles from './ReconcileAll.module.css'
import AppWrapper from '../../components/AppWrapper';
import ErrorModal from "../../components/Modals/ErrorModal"

const titles = [
    "Bond Custody (Inter.)",
    "Bond Custody (Client)",
    "Margin Account",
    "Mutual Fund",
]

export default function ReconcileAll({ secondaryTitle="结果显示" }) {
    const currentDate = new Date();
    const year = currentDate.getFullYear();
    const month = (currentDate.getMonth() + 1).toString().padStart(2, "0");
    const day = currentDate.getDate().toString().padStart(2, "0");
    const formattedDate = `${year}-${month}-${day}`;
    
    const [calDate, setCalDate] = useState(formattedDate)
    const [cFile, setCfile] = useState([]) //contains a list of CSVs, length is expected to be # of tables
    const [selected, setSelected] = useState(0) //by default show the first dataframe
    const [showErrorMsg1, setShowErrorMsg1] = useState(false)
    const [errorMsg1, setErrorMsg1] = useState('')
    const [showErrorMsg2, setShowErrorMsg2] = useState(false)
    const [errorMsg2, setErrorMsg2] = useState('')
    
    async function ReconcileAll() {
        try {
      
            const response = await fetch("http://127.0.0.1:5000/all", {
                method: "GET",
            })
            const result = await response.json()
            console.log(result)
      
            if (result.status === "Succeeded") {
                console.log("Succeeded")

                if (result.cfile.length === titles.length) {
                    setCfile(result.cfile)
                } else {
                    throw new Error('Non-matching cfile length')
                }
            } else {
                 setShowErrorMsg1(true)
                 setErrorMsg1(result.message)
            }
        } catch (error) {
            console.error("Error:", error)
        }
    }

    async function GetHistory() {
        const formData = new FormData();
        formData.append("date", JSON.stringify(calDate))
        try {
      
            const response = await fetch("http://127.0.0.1:5000/history", {
                method: "POST",
                body: formData
            })
            const result = await response.json()
            console.log(result)
            if (result.status === "Succeeded") {
                console.log("Succeeded")

                if (result.cfile.length === titles.length) {
                    setCfile(result.cfile)
                } else {
                    throw new Error('Non-matching cfile length')
                }
            } else {
                setShowErrorMsg2(true)
                setErrorMsg2(result.message)
            }
        } catch (error) {
            console.error("Error:", error)
        }
    }
    
    return (
        <div>
            <ErrorModal show={showErrorMsg1} setShow={setShowErrorMsg1} message={errorMsg1} />
            <ErrorModal show={showErrorMsg2} setShow={setShowErrorMsg2} message={errorMsg2} />
            <AppWrapper>
                <div>
                    <div className={styles.controlsContainer}>
                        <Button onClick={ReconcileAll}>对账</Button>
                        <div className={styles.calendarContainer}>
                            <div>Retrieve history by date:</div>
                            <Calender calDate={calDate} setCalDate={setCalDate} ReconcileAll={GetHistory}/>
                        </div>
                    </div>
                </div>
            </AppWrapper>
            <AppWrapper title={secondaryTitle}>
                <CsvViewer cFile={cFile[selected]}/>
                {cFile.length > 0 && 
                    <TableSelector titles={titles} selected={selected} setSelected={setSelected}/>
                }
            </AppWrapper>
        </div>

    )
}