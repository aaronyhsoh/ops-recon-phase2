import OpsReconciliationTemplate from "./OpsReconciliationTemplate";

const json = {
    'title':"上传 Bond Custody (Client) 对账文件",
    'fileUploadSettings': [
        {
            'title':"Customer Statement",
            'acceptedFileType':'application/pdf,application/vnd.ms-excel,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,text/plain,text/csv',
        },
        {
            'title':"Ledger",
            'acceptedFileType':'application/pdf,application/vnd.ms-excel,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,text/plain,text/csv',
        },
    ],
    'apiReconcileRoute': '/bondcustodyclient/reconcile',
}

export default function BondCustodyClient() {
    return (
        <OpsReconciliationTemplate settings={json} />
    )
}
