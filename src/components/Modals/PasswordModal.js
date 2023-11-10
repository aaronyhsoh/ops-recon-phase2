import Modal from "./Modal";
import styles from './PasswordModal.module.css'

export default function PasswordModal({show, ...props}) {
    return (
        <Modal show={show}>
            <PasswordModalContent {...props} />
        </Modal>
    )
}

function PasswordModalContent({uploadedFile, sendFileWithPassword, setShow, wrong, setWrong, removeFile}) {
    const SetPass = (e) => {
        e.preventDefault();
        const input = document.getElementById('passwordInput').value;
        setShow(false)
        setWrong(false)
        sendFileWithPassword(input)
      };

    const closeModal=()=>{
        removeFile()
        setShow(false)
        setWrong(false)
    }
    
    return (
       <>
            <div className='modalheader'>
                输入文件密码
            </div>

            <div className='modalcontent'>
                <p>
                    文件名: <br/>
                    {uploadedFile.name}
                </p>
                {/* <input type="password" className={styles.passwordinput} onChange={SetPass}/> */}
                <input type="password" id="passwordInput" className={styles.passwordinput}/>
                {wrong?<div className={styles.red}>wrong password</div>:""}
            </div>
            
            <div className='modalfooter'>
                <button className='modalquitbutton' type='button' onClick={closeModal}>取消</button>
                <button className='modalconfirmbutton' type='submit' onClick={SetPass}>确认</button>
            </div>
        </>
    )
}