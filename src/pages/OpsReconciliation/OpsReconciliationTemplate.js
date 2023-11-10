import FileUploadApp from "../../components/FileUploadApp"
import AppWrapper from "../../components/AppWrapper"
import CsvViewer from "../../components/CsvViewer/CsvViewer"
import FileUpload from "../../components/FileUpload/FileUpload"

import ConfirmModal from "../../components/Modals/ConfirmModal"
import { useEffect, useState } from 'react'
import ErrorModal from "../../components/Modals/ErrorModal"

export default function OpsReconciliationTemplate({ secondaryTitle="结果显示", settings }) {
    const [uploadedFiles, setUploadedFiles] = useState([]);
    const [dataframes, setDataFrames] = useState([]);
    const [cFile, setCfile]=useState(null);
    const [dates, setDates] = useState(Array(settings.fileUploadSettings.length).fill("文件日期"))
    const [passwords, setPasswords] = useState(Array(settings.fileUploadSettings.length).fill(null))
    const [show, setShow] = useState(false)
    const [showErrorMsg, setShowErrorMsg] = useState(false)
    const [errorMsg, setErrorMsg] = useState('')

    const currentDate = new Date();
    const year = currentDate.getFullYear();
    const month = (currentDate.getMonth() + 1).toString().padStart(2, "0");
    const day = currentDate.getDate().toString().padStart(2, "0");
    
    const formattedDate = `${year}-${month}-${day}`;

    const setDate = index => date => {
        const tmpDates = [...dates]
        tmpDates[index] = date
        setDates(tmpDates)
    }

    const setPassword = index => password => {
        const tmpPasswords = [...passwords]
        tmpPasswords[index] = password
        setPasswords(tmpPasswords)
    }


    // temp
    useEffect(() => {
        setUploadedFiles(Array(settings.fileUploadSettings.length).fill(null))
        setDataFrames(Array(settings.fileUploadSettings.length).fill(null))
    }, [settings])

    const _setUploadedFile = (idx) => (newFile) => {
        setUploadedFiles(prev => {
            const updated = [...prev]
            updated[idx] = newFile
            return updated
        })
    }

    const _setDataFrames = (idx) => (newFile) => {
        setDataFrames(prev => {
            const updated = [...prev]
            updated[idx] = newFile
            return updated
        })
    }

    const isAllUploaded = uploadedFiles.every(file => file)

    function checkDate(){
        console.log(formattedDate)
        setShow(!dates.every((item) => item === dates[0]))
        const confirmVar = dates.every((item) => item === dates[0]);
        if(confirmVar){
            PostAPI()
        }
    }

    const getFilesWithWrongDate = () => {
        let temp = ""
        dates.forEach((date, index) => {
            if(date !== formattedDate){
                temp+=settings.fileUploadSettings[index].title + ", "
            }
        });

        if (temp.endsWith(", ")) {
            temp = temp.slice(0, -2); // Remove the last two characters (comma and space)
        }

        return temp
    }

    async function PostAPI() {
        const formData = new FormData();
        formData.append("passwords", JSON.stringify(passwords))
        for (let i = 0; i < uploadedFiles.length; i++) {
            formData.append(i, uploadedFiles[i])
        }
        formData.append("dataframes", JSON.stringify(dataframes))
        console.log(dataframes)
        try {
            setCfile(null);
      
            const response = await fetch("http://127.0.0.1:5000" + settings.apiReconcileRoute, {
                method: "POST",
                body: formData,
            })
            const result = await response.json()
            console.log(result)
      
            if (result.cfile) {
                setCfile(result.cfile)
            } else {
                setShowErrorMsg(true)
                setErrorMsg(result.message)
            }
        } catch (error) {
            console.error("Error:", error)
        }
    }

    return (
        <div>
            <ConfirmModal show={show} PostAPI={PostAPI} setShow={setShow} filesWithWrongDate={getFilesWithWrongDate()} />
            <ErrorModal show={showErrorMsg} setShow={setShowErrorMsg} message={errorMsg} />
            <FileUploadApp title={settings.title} checkDate={checkDate} isAllUploaded={isAllUploaded}>
                { settings.fileUploadSettings.map((obj, idx) => (
                    <FileUpload key={idx} title={obj.title} acceptedFileType={obj.acceptedFileType} uploadedFile={uploadedFiles[idx] } setUploadedFile={_setUploadedFile(idx)} setDataFrames={_setDataFrames(idx)} date={dates[idx]} setDate={setDate(idx)} setPassword={setPassword(idx)} formattedDate={formattedDate} disabled={obj.title!=='Ledger Raw Data' && (settings.title === '上传 Bond Custody (Inter.) 对账文件' && !uploadedFiles[0])}/>
                ))}
            </FileUploadApp>
            <AppWrapper title={secondaryTitle}>
                <CsvViewer cFile={cFile}/>
            </AppWrapper>
        </div>
    )
}