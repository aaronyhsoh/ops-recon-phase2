import { NavLink } from "react-router-dom";

import styles from './Page.module.css'

export default function Page({ title, to }) {
    return (
        <NavLink className={styles.link} to={to}>
            {({ isActive }) => 
                <li className={`${styles.page} ${isActive ? styles.active : ""}`}>
                    { title }
                </li>
            }
        </NavLink>
    )
}
