import Modal from "./Modal"

export default function ConfirmModal({show, ...props}) {
    return (
        <Modal show={show}>
            <ConfirmModalContent {...props} />
        </Modal>
    )
}

function ConfirmModalContent({PostAPI, setShow, filesWithWrongDate}) {  
    const closeModal =()=> {
        setShow(false)
    }
    
    const onConfirm =()=> {
        PostAPI()
        setShow(false)
    }

    return (
        <>
            <div className='modalheader'>
                提醒！
            </div>

            <div className='modalcontent'>
                <p>
                    文件日期与当前日期不符，是否继续？
                </p>
            </div>
            
            <div className='modalfooter'>
                <button className='modalquitbutton' onClick={closeModal}>取消</button>
                <button className='modalconfirmbutton' onClick={onConfirm}>继续</button>
            </div>
        </>
    )
}