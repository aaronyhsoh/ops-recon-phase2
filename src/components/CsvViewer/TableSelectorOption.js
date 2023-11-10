import styles from './TableSelectorOption.module.css'

export default function TableSelectorOption({ title, isSelected, setSelected }) {
    return (
        <div className={styles.optionContainer}>
            <div className={`${styles.optionText} ${isSelected ? styles.selected : ''}`} onClick={setSelected}>
                {title}
            </div>
        </div>
    )
}