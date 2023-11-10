import { createPortal } from 'react-dom'
import './Modal.css'

/*
Classes available for use are
- modalheader
- modalcontent
- modalfooter
- modalconfirmbutton
- modalquitbutton

Example usage:
    <Modal>
        <div className='modalheader'>
            This is the header
        </div>

        <div className='modalcontent'>
            <div>First content</div>
            <div>Second content</div>
        </div>

        <div className='modalfooter'>
            <button className='modalquitbutton'>Quit</button>
            <button className='modalconfirmbutton'>Confirm</button>
        </div>
    </Modal>
*/

export default function Modal({ show, children }) {
    return (
        <>
            {
                show && createPortal(
                    <div className='overlay'>
                        <div className='modalcontainer'>
                            {children}
                        </div>
                    </div>,
                    document.body)
            }
        </>
        
    )
}