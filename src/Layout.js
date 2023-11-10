import { Outlet } from "react-router-dom";

import Navbar from './components/Navbar/Navbar'
import Sidebar from './components/Sidebar/Sidebar'
import Main from './components/Main/Main'
import Footer from './components/Footer/Footer'

import styles from './Layout.module.css'

export default function Layout() {
    return (
        <div className={styles.layout}>
            <Navbar />
            <div className={styles.content}>
                <div className={styles.sidebar}>
                    <Sidebar />
                </div>
                <div className={styles.main}>
                    <Main>
                        <Outlet />
                    </Main>
                </div>
            </div>
            <Footer />
        </div>
    )
}