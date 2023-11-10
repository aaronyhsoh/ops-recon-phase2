import styles from './CsvViewer.module.css'
import { useState, useEffect, useCallback, useRef } from 'react'
import { AgGridReact } from 'ag-grid-react'
import CsvViewerFooter from './CsvViewerFooter/CsvViewerFooter'
import 'ag-grid-enterprise'

import 'ag-grid-community/styles/ag-grid.css'
import 'ag-grid-community/styles/ag-theme-alpine.css'; // Optional theme CSS

// copied from https://stackoverflow.com/questions/8493195/how-can-i-parse-a-csv-string-with-javascript-which-contains-comma-in-data
function CSVtoArray(text) {
    const re_value = /(?!\s*$)\s*(?:'([^'\\]*(?:\\[\S\s][^'\\]*)*)'|"([^"\\]*(?:\\[\S\s][^"\\]*)*)"|([^,'"\s\\]*(?:\s+[^,'"\s\\]+)*))\s*(?:,|$)/g;
    const arr = [];                     // Initialize array to receive values.
    text.replace(re_value, // "Walk" the string using replace with callback.
        function(m0, m1, m2, m3) {
            // Remove backslash from \' in single quoted values.
            if      (m1 !== undefined) arr.push(m1.replace(/\\'/g, "'"));
            // Remove backslash from \" in double quoted values.
            else if (m2 !== undefined) arr.push(m2.replace(/\\"/g, '"'));
            else if (m3 !== undefined) arr.push(m3);
            return ''; // Return empty string.
        });
    // Handle special case of empty last value.
    if (/,\s*$/.test(text)) arr.push('');
    return arr;
};

export default function CsvViewer({ cFile }) {
    const gridRef = useRef();
    const [rowData, setRowData] = useState([]);
    const [columnDefs, setColumnDefs] = useState([]);
    const [rowDataTracker, setRowDataTracker] = useState({});
    
    // Load csv data
    useEffect(() => {
        if (cFile) {
            fetch(cFile)
            .then(response => {
                console.log(response)
                const res = response.text();
                console.log(res);
                return res;
            })
            .then(csv => csv.split('\r\n'))
            .then(rows => rows.map(row => CSVtoArray(row)))
            .then(rows => rows.filter(row => row.length === rows[0].length))
            .then(rows => {
                console.log(rows)
                const colHeaders = rows[0]
                setColumnDefs(colHeaders.map(colHeader => {
                    const obj = {field: colHeader}
                    return obj
                }))

                const dataRows = rows.slice(1)
                setRowData(dataRows.map(dataRow => {
                    const rowJson = {}
                    dataRow.forEach((dataValue, idx) => {
                        rowJson[colHeaders[idx]] = dataValue
                    })
                    return rowJson
                }))
            })
        } else {
            setRowData([])
            setColumnDefs([])
            setRowDataTracker({})
        }
    }, [cFile]);

    const _onCellValueChanged = (e) => {
        const storeEdit = (rowId, colId, oldValue, newValue) => {
            setRowDataTracker(prev => {
                if (!prev[rowId]) {
                    prev[rowId] = {}
                }
        
                if (!prev[rowId][colId]) {
                    prev[rowId][colId] = [oldValue, newValue]
                } else {
                    prev[rowId][colId] = [prev[rowId][colId][0], newValue]
                }
                return prev
            })
        }

        const oldValue = e.oldValue ? e.oldValue : ''
        const newValue = e.newValue ? e.newValue : ''
        
        if (oldValue.toString() !== newValue.toString()) {
            storeEdit(e.node.id, e.column.colId, oldValue, newValue)
        }
        console.log(rowDataTracker)
        gridRef.current.api.refreshCells();
    }

    const resetData = useCallback(() => {
        // Reset column state
        gridRef.current.columnApi.resetColumnState();

        // Reset column filters
        gridRef.current.api.setFilterModel(null);

        // Reset grid data to original
        gridRef.current.api.forEachNode((node) => {
            if (rowDataTracker[node.id]) {
                const data = node.data
                Object.keys(rowDataTracker[node.id]).forEach(key => {
                    data[key] = rowDataTracker[node.id][key][0]
                })
                node.updateData(data)
            }
        })

        setRowDataTracker({})
        gridRef.current.api.refreshCells();
    }, [rowDataTracker])

    const downloadData = useCallback(() => {
        gridRef.current.api.exportDataAsExcel();
    }, []);

    const defaultColDef = {
        sortable: true,
        filter: true,
        cellClass: styles.cell,
        headerClass: styles.header,
        minWidth: 200,
        flex: 1,
        resizable: true,
        lockPosition: 'left',
        editable: true,
        singleClickEdit: true,
        onCellValueChanged: _onCellValueChanged,
    };

    return (
        <>
            <div className={styles.gridContainer}>
                <div className={`ag-theme-alpine ${styles.gridTable}`}>
                    <AgGridReact
                        ref={gridRef}
                        rowData={rowData} // Row Data for Rows

                        columnDefs={columnDefs} // Column Defs for Columns
                        defaultColDef={defaultColDef} // Default Column Properties

                        stopEditingWhenCellsLoseFocus={true}
                        animateRows={true} // Optional - set to 'true' to have rows animate when sorted
                        rowSelection='multiple' // Options - allows click selection of rows
                    />
                </div>
                {
                    rowData.length !== 0 && <CsvViewerFooter resetData={resetData} downloadData={downloadData}/>
                }
            </div> 
        </>
    )
}