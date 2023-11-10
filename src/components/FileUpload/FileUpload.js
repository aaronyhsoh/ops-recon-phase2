import { useEffect, useRef, useState} from 'react';
import { pdfjs } from 'react-pdf';
import ExcelJS from 'exceljs';

import { ReactComponent as FileUploadIcon} from "../../assets/FileUpload/FileUploadIcon.svg";
import { ReactComponent as DeleteButtonIcon} from "../../assets/FileUpload/DeleteButtonIcon.svg";

import PdfIcon from "../../assets/FileUpload/PdfIcon.png";
import WordIcon from "../../assets/FileUpload/WordIcon.png";
import ImageIcon from "../../assets/FileUpload/ImageIcon.png";
import XlsIcon from "../../assets/FileUpload/XlsIcon.png";
import BlankIcon from "../../assets/FileUpload/BlankIcon.png";

import PasswordModal from "../../components/Modals/PasswordModal";
import ErrorModal from "../../components/Modals/ErrorModal";
import WarnModal from "../../components/Modals/WarnModal";

import styles from "./FileUpload.module.css";


export default function FileUpload({ acceptedFileType, title, date, setDate, uploadedFile, setUploadedFile, setDataFrames, setPassword, formattedDate, disabled=false}) {
    const allowedTypes = acceptedFileType.split(',').map(type => type.trim());
    const [show, setShow] = useState(false);
    const [wrong, setWrong]=useState(false);
    const [errorModal, setErrorModal]=useState(false);
    const [warnModal, setWarnModal]=useState(false);
    const [message, setMessage]=useState("");
    const [invokeSendFile, setInvokeSendFile]=useState(false);
    const fileUploadRef = useRef(null);
    const labelRef = useRef(null);
    const [warning, setWarning] = useState(false)
    
    pdfjs.GlobalWorkerOptions.workerSrc = "js/pdf.worker.min.js";

    useEffect(() => {
        // Code to execute when the invokeSendFile state updates
        // Small caveat: setting invokeSendFile to true will call this useEffect twice
        // once from the initial state change, another when reverting it back to false
        if (invokeSendFile) {
            sendFileWithPassword()
            setInvokeSendFile(false)
        }
      }, [invokeSendFile]);
    
    useEffect(() => {
        const preventDefault = e => e.preventDefault()
        fileUploadRef.current.addEventListener("dragover", preventDefault)
        fileUploadRef.current.addEventListener("drop", preventDefault)
    }, [])
    
    const handleButtonClick = () => {
        // problem: we clear the input everytime we click on the button
        // but ok to do this since the input element isn't used to submit a form
        labelRef.current.value = labelRef.current.defaultValue
        labelRef.current.click();
    }

    async function sendFileWithPassword(password=''){
        const formData = new FormData();
        console.log(uploadedFile, password, title)
        formData.append('file', uploadedFile);
        formData.append("password", password);
        formData.append("title", title);
        try {
            const response = await fetch("http://127.0.0.1:5000/verify", {
                method: "POST",
                body: formData,
            })
            const result = await response.json()
            console.log(result)
            if (result.wrong_password) {
                setShow(true)
                setWrong(true)
            } else {
                setDate(result.date)
                setPassword(password)
                setMessage(result.message)
                setDataFrames(result.dataframe)
                statusDispatcher(result)
            }
        } catch (error) {
            console.error("Error:", error)
        }
    }

    const statusDispatcher = result => {
        // To handle different status
        if (result.dataframe && !result.message) {
            // NORMAL status
            return
        } else if (!result.dataframe && result.message) {
            // ERROR status
            setErrorModal(true)
            return
        } else if (result.dataframe && result.message) {
            // WARNING status
            setWarnModal(true)
            return
        } else {
            console.error("Invalid verification status with message:", result.message)
        }
    }

    const checkExcelFile = async (file) => {
        file.text().then(x=> {
            console.log("isEncrypted", x.includes("Encrypt")) // true, if Encrypted
            console.log(file.name);
            if(x.includes("Encrypt")){
                setShow(true)
            }
            else{
                setInvokeSendFile(true)
            }
        });
      };

    const checkOldExcelFile = async (file) => {
        const workbook = new ExcelJS.Workbook();
      
        try {
          await workbook.xlsx.load(file);
      
          setInvokeSendFile(true)
          
        } catch (error) {
          setShow(true)
        }
    };
    
    const handleChange = e => {
        if (e.target.files[0]) {
            if (allowedTypes.includes(e.target.files[0].type)) {
                setUploadedFile(e.target.files[0])
                const file = e.target.files[0];
                if(file.type==='application/pdf'){
                    const reader = new FileReader();
                    reader.onload=e=>{
                        let res = reader.result;
                        
                        pdfjs.getDocument(res).promise.then((pdf) => {
                            // let pages = pdf.numPages;
                            setInvokeSendFile(true)
                        })
                        .catch((error) =>{
                            setShow(true)
                          });
                    };
                    reader.readAsArrayBuffer(file)
                };
                if(file.type==='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' || file.type==='application/vnd.ms-excel'){
                    checkExcelFile(file)
                }
                if(file.type==='text/plain'||file.type==='text/csv'){
                    setInvokeSendFile(true)
                }
            } else {
                wrongFileType();
            }
        } 
    }



    const handleDrop = e => {
        if (e.dataTransfer.files[0]) {
            if (allowedTypes.includes(e.dataTransfer.files[0].type)) {
                const file = e.dataTransfer.files[0];
                setUploadedFile(e.dataTransfer.files[0]);
                if(file.type==='application/pdf'){
                    const reader = new FileReader();
                    reader.onload=e=>{
                        let res = reader.result;
                        
                        pdfjs.getDocument(res).promise.then((pdf) => {
                            // let pages = pdf.numPages;
                            setInvokeSendFile(true)
                        })
                        .catch((error) =>{
                            setShow(true)
                          });
                    };
                    reader.readAsArrayBuffer(file)
                };
                
                if(file.type==='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' || file.type==='application/vnd.ms-excel'){
                    checkExcelFile(file)
                }
                if(file.type==='text/plain'||file.type==='text/csv'){
                    setInvokeSendFile(true)
                }
            } else {
                wrongFileType();
            }
        }
    }
    
    const removeFile = e => {
        if(e){
            e.stopPropagation()
        }
        setUploadedFile(null)
        setDate("文件日期")
    }

    const wrongFileType = () => {
        setWarning(true)
        setTimeout(() => setWarning(false), 2000)
    }

    // Runs func if disabled prop is False
    // Else warning
    const checkDisabled = (func) => {
        if (disabled) {
            console.log('disabled')
        } else {
            func()
        }
    }

    
    return (
        <div className={styles.fileUploadWrapper}>
            <PasswordModal uploadedFile={uploadedFile} show={show} setShow={setShow} sendFileWithPassword={sendFileWithPassword} wrong={wrong} setWrong={setWrong} removeFile={removeFile} />
            <WarnModal message={message} show={warnModal} setShow={setWarnModal} removeFile={removeFile} />
            <ErrorModal message={message} show={errorModal} setShow={setErrorModal}  removeFile={removeFile} />
            <div className={styles.title}>
                {title}
            </div>
            <div className={`${styles.fileUpload} ${warning ? styles.warning : ""}`} ref={fileUploadRef} >
                <input type="file" className={styles.fileUploadInput} multiple={false} accept= {acceptedFileType} onChange={handleChange} ref={labelRef}/>
                <div className={styles.fileUploadArea} onDrop={e => checkDisabled(() => handleDrop(e))} onClick={e => checkDisabled(() => handleButtonClick(e))}>

                    {!uploadedFile && !disabled && <div className={styles.uploadedFile} >
                        <FileUploadIcon className={styles.fileUploadIcon} />
                        <p className={styles.browseButton}>上传文件</p>
                        {warning && <div className={styles.wrongFileType}>Invalid file type</div>}
                    </div>}

                    {uploadedFile && <div className={styles.uploadedFile} >
                        <img className={styles.fileFormatIcon} src={chooseFileIcon(uploadedFile)} alt="Icon of a file"/>
                        <DeleteButtonIcon className={styles.deleteButton} onClick={removeFile}/>
                        {warning && <div className={styles.wrongFileType}>Invalid file type</div>}
                    </div>}
                </div>
            </div>
            <div className={date===formattedDate || date==="文件日期"?styles.date:styles.wrong}>
                {date}
            </div>
        </div>
    )
}


function chooseFileIcon(file) {
    if (file === null) {
        return BlankIcon;
    }
    
    if (file.type === "application/pdf") {
        return PdfIcon;
    } else if (file.type === "application/msword" || file.type === "application/vnd.openxmlformats-officedocument.wordprocessingml.document") {
        return WordIcon;
    } else if (file.type.split("/")[0] === "image") {
        return ImageIcon;
    } else if (file.type === "text/csv" || file.type === 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' || file.type === 'application/vnd.ms-excel') {
        return XlsIcon;
    }

    return BlankIcon;
}
