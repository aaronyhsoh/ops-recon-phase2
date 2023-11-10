import OpsReconciliationTemplate from "./OpsReconciliationTemplate";

const json = {
    'title':"上传 Bond Custody (Inter.) 对账文件",
    'fileUploadSettings': [
        {
            'title':"Ledger Raw Data",
            'acceptedFileType':'application/pdf,application/vnd.ms-excel,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,text/plain,text/csv',
        },
        {
            'title':"CCDC Holding",
            'acceptedFileType':'application/pdf,application/vnd.ms-excel,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,text/plain,text/csv',
        },
        {
            'title':"SPDB HK",
            'acceptedFileType':'application/pdf,application/vnd.ms-excel,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,text/plain,text/csv',
        },
        {
            'title':"MAS File",
            'acceptedFileType':'application/pdf,application/vnd.ms-excel,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,text/plain,text/csv',
        },
        {
            'title':"DBS Holdings",
            'acceptedFileType':'application/pdf,application/vnd.ms-excel,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,text/plain,text/csv',
        },
        {
            'title':"Clearstream",
            'acceptedFileType':'application/pdf,application/vnd.ms-excel,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,text/plain,text/csv',
        }
    ],
    'apiReconcileRoute': '/bondcustodyinter/reconcile',
}

export default function BondCustodyInter() {
    return (
        <OpsReconciliationTemplate settings={json} />
    )
}
