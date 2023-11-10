import Search from '../../assets/Navbar/search.png'
import Calendar from '../../assets/Navbar/calendar.png'
import Notification from '../../assets/Navbar/notification.png'
import Envelope from '../../assets/Navbar/envelope.png'
import GlobalItem from './GlobalItem'

import styles from './GlobalBar.module.css'

export default function GlobalBar() {
    return (
        <ul className={styles.globalBar}>
            <GlobalItem imgSrc={Search} imgAlt="Search" />
            <GlobalItem imgSrc={Calendar} imgAlt="Calendar" />
            <GlobalItem imgSrc={Notification} imgAlt="Notification" flagCount={3} />
            <GlobalItem imgSrc={Envelope} imgAlt="Envelope" flagCount={64} />
        </ul>
    )
}