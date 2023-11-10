import AppWrapper from "../../components/AppWrapper";
import CCDCSetting from "../../components/Settings/CCDCSetting";

export default function CCDCHoldingSetting() {
    return (
        <>
            <AppWrapper title='CCDC Holding 设置' titleAlign='left'>
                <CCDCSetting />
            </AppWrapper>
        </>
    )
}
