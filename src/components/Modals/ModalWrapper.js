import ConfirmModal from './ConfirmModal';
import PasswordModal from './PasswordModal';
import { useState } from 'react';

/*
Wrapper for Modal components

This component handles the modal interactions upon clicking '对账' button
*/

export function ModalWrapper() {
    const [showPasswordModal, setShowPasswordModal] = useState(false);
    const [showConfirmModal, setShowConfirmModal] = useState(false);

    return (
        <>
            <PasswordModal show={showPasswordModal} closeModal={() => setShowPasswordModal(false)} onConfirm={() => {setShowPasswordModal(false); setShowConfirmModal(true)}} />
            <ConfirmModal show={showConfirmModal} closeModal={() => setShowConfirmModal(false)} onConfirm={() => setShowConfirmModal(false)} />
        </>
    )
}
