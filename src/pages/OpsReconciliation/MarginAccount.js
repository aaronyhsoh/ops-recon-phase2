import OpsReconciliationTemplate from "./OpsReconciliationTemplate";

const json = {
    'title':"上传 Margin Account 对账文件",
    'fileUploadSettings': [
        {
            'title':"F86",
            'acceptedFileType':'application/pdf,application/vnd.ms-excel,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,text/plain,text/csv',
        },
    ],    
    'apiReconcileRoute': '/marginaccount/reconcile',
}

export default function MarginAccount() {
    return (
        <OpsReconciliationTemplate settings={json} />
    )
}
