import Button from "../components/Button";
import DatePicker from "react-datepicker";
import styles from "./Calender.module.css";
import "react-datepicker/dist/react-datepicker.css";
import { useState, useEffect } from "react";

const DATAFRAME_ABSENT = '2'
const DATAFRAME_PRESENT = '1'
const DATAFRAME_ERROR = '0'

// where parameters a, b are Date objects
// returns true if a and b have the same Date (day, month and year)
const compareDate = (a, b) => {
    return a.getDate() === b.getDate() && a.getMonth() === b.getMonth() && a.getFullYear() === b.getFullYear()
}

export default function Calender({calDate,setCalDate,ReconcileAll}) {
    // dates is a dictionary, where the keys are one of :
    //      DATAFRAME_ABSENT, DATAFRAME_PRESENT, DATAFRAME_ERROR
    // and the value is a list containing the dates that fix those flags
    const [dates, setDates] = useState({
        [DATAFRAME_ABSENT]: [],
        [DATAFRAME_PRESENT]: [],
        [DATAFRAME_ERROR]: []
    })

    const isValidDate = (date) => {
        const datesConcat = Object.values(dates).reduce((a, b) => a.concat(b))

        return compareDate(date, new Date()) 
            || datesConcat.some(x => compareDate(x, date))
      };

    useEffect(() => {
        fetch('http://127.0.0.1:5000/get_calender_status')
        .then(res => res.json())
        .then(res => JSON.parse(res.data))
        .then(res => {
            console.log(res)
            const dateColIdx = res.columns.findIndex(x => x === 'date')
            const flagColIdx = res.columns.findIndex(x => x === 'flag')

            const curr = {
                [DATAFRAME_ABSENT]: [],
                [DATAFRAME_PRESENT]: [],
                [DATAFRAME_ERROR]: []
            }

            res.data.forEach(row => {
                if (row[flagColIdx] === DATAFRAME_ERROR) {
                    curr[DATAFRAME_ERROR].push(new Date(row[dateColIdx]))
                }
                
                if (row[flagColIdx] === DATAFRAME_PRESENT) {
                    curr[DATAFRAME_PRESENT].push(new Date(row[dateColIdx]))
                }

                if (row[flagColIdx] === DATAFRAME_ABSENT) {
                    curr[DATAFRAME_ABSENT].push(new Date(row[dateColIdx]))
                }
            })

            setDates(curr)
        })
        .catch(e => console.error(e))
    }, [])

    const changeDate = e => {
        console.log(calDate)
        ReconcileAll()
    }

    const highlightWithRanges = [
        {
            [styles.highlightError]: dates[DATAFRAME_ERROR]
        },
        {
            [styles.highlightPresent]: dates[DATAFRAME_PRESENT]
        },
        {
            [styles.highlightAbsent]: dates[DATAFRAME_ABSENT]
        },
    ]


    return (
        <div className={styles.flex}> 
            <DatePicker
                showIcon
                selected={new Date(calDate)}
                onChange={(date) => setCalDate(date)}
                // Add any custom styles here
                highlightDates={highlightWithRanges} // Pass the custom highlight function here
                filterDate={isValidDate}
                className="custom-datepicker"
                dateFormat="dd-MM-yyyy" // Customize the date format
            />
            <Button onClick={changeDate}>复取</Button>
        </div>
    )
}