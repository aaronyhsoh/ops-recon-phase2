import OpsReconciliationTemplate from "./OpsReconciliationTemplate";

const json = {
    'title':"上传 Mutual Fund 对账文件",
    'fileUploadSettings': [
        {
            'title':"VESTIMA",
            'acceptedFileType':'application/pdf,application/vnd.ms-excel,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,text/plain,text/csv',
        },
        {
            'title':"Bond Custody Services",
            'acceptedFileType':'application/pdf,application/vnd.ms-excel,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,text/plain,text/csv',
        },
    ],
    'apiReconcileRoute': '/mutualfund/reconcile',
}

export default function MutualFund() {
    return (
        <OpsReconciliationTemplate settings={json} />
    )
}
