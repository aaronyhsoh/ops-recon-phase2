import styles from './Button.module.css'

export default function Button({ disabled, children, onClick=() => null }) {
    return (
        <button type="button" onClick={onClick} className={`${styles.button} ${disabled?styles.disabled:""}`} disabled={disabled}>{children}</button>
    )
}
