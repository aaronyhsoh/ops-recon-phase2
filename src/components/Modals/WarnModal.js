import Modal from "./Modal";
import styles from "./WarnModal.module.css"

export default function WarnModal({show, ...props}) {
    return (
        <Modal show={show}>
            <WarnModalContent {...props} />
        </Modal>
    )
}

function WarnModalContent({message,setShow,removeFile}) {
    const okay = () => {
        setShow(false)
      };

    const closeModal=()=>{
        removeFile()
        setShow(false)
    }
    
    return (
       <>
            <div className='modalheader'>
                Warning
            </div>

            <div className={`${(styles.icon)} ${'modalcontent'}`}>
                <p>
                    {message}
                </p>
            </div>
            
            <div className='modalfooter'>
                <button className='modalquitbutton' type='button' onClick={closeModal}>取消</button>
                <button className='modalconfirmbutton' type='submit' onClick={okay}>继续</button>
            </div>
        </>
    )
}