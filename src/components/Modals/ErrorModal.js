import Modal from "./Modal";
import styles from "./ErrorModal.module.css"

export default function ErrorModal({show, ...props}) {
    return (
        <Modal show={show}>
            <ErrorModalContent {...props} />
        </Modal>
    )
}

function ErrorModalContent({message,setShow,removeFile=()=>{}}) {
    const closeModal=()=>{
        removeFile()
        setShow(false)
    }
    
    return (
       <>
            <div className='modalheader'>
                Error
            </div>

            <div className={`${(styles.icon)} ${'modalcontent'}`}>
                <p>
                    {message}
                </p>
            </div>
            
            <div className='modalfooter'>
                <button className='modalquitbutton' type='button' onClick={closeModal}>取消</button>
            </div>
        </>
    )
}