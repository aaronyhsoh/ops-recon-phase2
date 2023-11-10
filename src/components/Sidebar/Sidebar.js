import Operation from "./Operation"
import Page from "./Page"

import styles from './Sidebar.module.css'

export default function Sidebar() {
    return (
        <ul className={styles.sidebar}>
            <Operation title="运营对账" active={true}>
                <Page title="Reconcile All" to="" />
                <Page title="Bond Custody (Inter.)" to="bondcustodyinter" />
                <Page title="Bond Custody (Client)" to="bondcustodyclient" />
                <Page title="Margin Account" to="marginaccount" />
                <Page title="Mutual Fund" to="mutualfund" />
            </Operation>
            <Operation title="数据分析">
            </Operation>
            <Operation title="系统设置">
                <Page title="CCDC Holding 设置" to="CCDCHoldingSetting" />
                <Page title="Path Setting" to="PathSetting" />
                <Page title="placeholder1" to="placeholder1" />
                <Page title="placeholder2" to="placeholder2" />
            </Operation>
        </ul>
    )
}