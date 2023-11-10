import { useState } from 'react'

import { ReactComponent as Arrow} from '../../assets/arrow.svg'

import styles from './Operation.module.css'

export default function Operation({ title, children }) {
    const [active, setActive] = useState(true)

    const toggleActive = () => {
        setActive(!active)
    }

    return (
        <li className={styles.operation}>
            <div className={styles.operationTitle} onClick={toggleActive}>
                {title}
                <Arrow className={`${styles.arrow} ${active ? styles.active : ""}`}/>
            </div>
            <ul className={`${styles.operationItems} ${active ? "" : styles.collapsed}`}>
                {children}
            </ul>
        </li>
    )
}
