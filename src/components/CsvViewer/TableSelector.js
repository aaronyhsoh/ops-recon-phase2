import styles from './TableSelector.module.css'
import TableSelectorOption from './TableSelectorOption'

export default function TableSelector({ titles, selected, setSelected }) {
    return (
        <div className={styles.container}>
            {titles.map((title, idx) => {
                return (
                    <TableSelectorOption title={title} key={idx} isSelected={selected === idx} setSelected={() => setSelected(idx)} />
                )
            })}
        </div>
    )
}