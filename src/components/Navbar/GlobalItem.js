import styles from './GlobalItem.module.css'

export default function GlobalItem({ imgSrc, imgAlt, flagCount=0 }) {
    return (
        <li className={styles.globalItem}>
            <img src={imgSrc} alt={imgAlt} />
            <div className={flagCount !== 0 ? styles.flagCount : ""}>{flagCount !== 0 ? flagCount : ""}</div>
        </li>
    )
}