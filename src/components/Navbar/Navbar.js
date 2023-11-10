import { Link } from 'react-router-dom'

import GlobalBar from './GlobalBar'
import User from './User'

import SpdbLogo from '../../assets/Navbar/logo-spdb.png'

import styles from './Navbar.module.css'

export default function Navbar() {
    return (
        <nav className={styles.navbar}>
            <div className={styles.left}>
                <Link to=".">
                <img className={styles.logo} src={SpdbLogo} alt="Shanghai Pudong Development Bank"/>
                </Link>
            </div>
            <div className={styles.right}>
                <GlobalBar />
                <User name="Yan Minghao"/>
            </div>
        </nav>
    )
}
