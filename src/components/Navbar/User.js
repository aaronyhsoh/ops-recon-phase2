import { useEffect, useRef } from 'react'
import { ReactComponent as Arrow } from '../../assets/arrow.svg'
import DefaultUserIcon from '../../assets/Navbar/default-user-icon.png'

import styles from "./User.module.css"

export default function User({ name="user", imgSrc=DefaultUserIcon }) {
    const userIconWrapperRef = useRef(null)

    useEffect(() => {
        userIconWrapperRef.current.style.backgroundImage = `url(${imgSrc})`
    }, [imgSrc])

    return (
        <div className={styles.user}>
            <div className={styles.userIconWrapper} ref={userIconWrapperRef} />
            <div className={styles.userName}>{name}</div>
            <Arrow className={styles.userArrow} />
        </div>
    )
}