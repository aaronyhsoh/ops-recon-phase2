import pandas as pd
import re
from datetime import datetime
import io

def process_mas_txt_files(file_bytes, ledger_file):
    try:
        warning = ""


        # Initialize the Return DataFrame
        columns = ['ISIN', 'Securities Name', 'Statement/Ledger', 'Buy/Sell', 'Face Amount', 'Source', 'Currency']
        filtered_df = pd.DataFrame(columns=columns)
        
        #read file content
        txt_file = io.BytesIO(file_bytes)
        file_content = txt_file.read().decode('UTF-8')
        print(file_content)
        
        # Extract the date from the text file
        date = datetime.strptime(extract_date(file_content), '%d-%b-%Y')
        date = date.strftime('%Y-%m-%d')

        # Extract the ISIN number from the text file
        isins = extract_isin(file_content) #can be multiple
        if len(isins)==0:
            warning = "ISIN parsing failed"
            return None, date, warning

        # Read the Excel file into a DataFrame
        ledger_df = pd.read_excel(ledger_file)

        # Extract the ISIN number from the text file
        filtered_df['ISIN'] = isins
        names = [[]]*len(isins)
        for k,isin in enumerate(isins):
            names[k] = ledger_df[ledger_df['Alt ID'] == isin]['Security'].values[0]
        filtered_df['Securities Name'] = names

        # Extract the amount from the text file
        amounts = extract_amount(file_content)
        if len(amounts)==0:
            warning = "Amount parsing failed"

        # Add the extracted amount to the DataFrame
        filtered_df['Face Amount'] = amounts

        # Fill in other default columns
        filtered_df['Statement/Ledger'] = ['Statement']*len(isins)
        filtered_df['Buy/Sell'] = ['Buy']*len(isins)
        filtered_df['Source'] = ['MAS']*len(isins)
        filtered_df['Currency'] = ['SGD']*len(isins)

        return filtered_df, date, warning

    except Exception as e:
        error_message = str(e)
        return None, None, error_message

def extract_date(file_content):
    date_pattern = r"(\d{2}-[A-Z]{3}-\d{4})"
    match = re.search(date_pattern, file_content)
    if match:
        date = match.group(1)
    else:
        date = ""  # Empty string if no match found
    return date

def extract_isin(file_content, b_findall=True):
    isin_pattern = r"[^:]*:35B:ISIN (\w+)"
    matches = re.findall(isin_pattern, file_content) #find all
    isin = matches[:]
    return isin

def extract_amount(file_content):
    amount_pattern = r"[^:]*:93B::AGGR//FAMT/(\d+)"
    matches = re.findall(amount_pattern, file_content)
    amount = matches[:]
    return amount

if __name__=="__main__":
        # Read the text file
    mas_file= "Input_files/MAS.txt"
    with open(mas_file, "r") as txt_file:
        #txt_file = io.BytesIO(file_bytes)
        file_content = txt_file.read()
    ledger_file="Input_files/Ledger_Raw Data.xls"
    ledger_df = pd.read_excel(ledger_file)
    df, date, msg = process_mas_txt_files(file_content, ledger_df)
