import pandas as pd
import re
import PyPDF2
from datetime import datetime
import io

def process_hk_pdf_file(pdf_bytes, ledger_file):
    try:
        warning = ""

        # Initialize the Return DataFrame
        columns = ['ISIN', 'Securities Name', 'Statement/Ledger', 'Buy/Sell', 'Face Amount', 'Source', 'Currency']
        filtered_df = pd.DataFrame(columns=columns)
        pdf_file = io.BytesIO(pdf_bytes)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        num_pages = len(pdf_reader.pages)
        file_content = ""
        
        # Extract text from each page
        for page_number in range(num_pages):
            page = pdf_reader.pages[page_number]
            file_content += page.extract_text()
        # Extract date from the PDF file
        date = extract_date(file_content)

        # check if no valid data
        b_nil = extract_nil(file_content)
        if b_nil:
            return filtered_df, date, warning

        # Extract the ISIN number from the PDF content
        isin_orig = extract_isin(file_content)
        if isin_orig=="": warning = "ISIN parsing failed"
        isin_exact = isin_orig+'.IB'

        # Read the Excel file into a DataFrame
        ledger_df = pd.read_excel(ledger_file)
        
        # Extract the ISIN number and Date from the text file
        
        matches = (ledger_df['Alt ID'] == isin_exact)
        if not matches.any(): #no exact match, then find row number by partial search
            indices = ambiguous_search(ledger_df['Alt ID'], isin_orig) 
            if len(indices)==0:
                warning = "no ISIN found for {ISIN}, even by partial search".format(ISIN=isin_orig)
                return None, date, warning
            else:
                index = indices[0] # if "IB" not matched, fetch the first ambiguous result
                warning = "no exact ISIN found for {ISIN}".format(ISIN=isin_exact)
            isin_ambi = ledger_df['Alt ID'][index]
            filtered_df['ISIN'] = [isin_ambi]
            filtered_df['Securities Name'] = ledger_df['Security'].loc[index]
            # Extract date from the excel file
            #date = ledger_df['Position Date'].loc[index]
            #date = date.strftime('%Y-%m-%d')
        else:
            filtered_df['ISIN'] = [isin_exact]
            filtered_df['Securities Name'] = ledger_df[matches]['Security'].values
            # Extract date from the excel file
            #date = ledger_df[matches]['Position Date'].values[0]
            #date = date.astype('datetime64[D]').item().strftime('%Y-%m-%d')

        # Extract the amount from the text file
        amount = extract_amount(file_content)

        # Add the extracted amount to the DataFrame
        filtered_df['Face Amount'] = [amount]

        # Fill in other default columns
        filtered_df['Statement/Ledger'] = ['Statement']
        filtered_df['Buy/Sell'] = ['Buy']
        filtered_df['Source'] = ['SPDB HK']
        filtered_df['Currency'] = ['CNY']

        return filtered_df, date, warning

    except Exception as e:
        error_message = str(e)
        return None, None, error_message

def extract_nil(file_content):
    isin_pattern = r"Nil holding as at statement date" 
    match = re.search(isin_pattern, file_content)
    return match

def extract_date(file_content):
    date_pattern = r"From\s+([\d/]+)"
    match = re.search(date_pattern, file_content)
    if match:
        date_string = match.group(1)
        datetime_obj = datetime.strptime(date_string, "%Y/%m/%d")
        formatted_date = datetime_obj.strftime("%Y-%m-%d")
        return formatted_date
    else:
        return None  # Return None if no date found

def ambiguous_search(IDs, partial_isin):
    # Perform partial search on 'Alt ID' column
    matches = IDs[IDs.str.contains(partial_isin, case=False, na=False)]
    
    # Return the indices of matching rows
    indices = matches.index.tolist()
    
    return indices

def extract_isin(file_content):
    isin_pattern = r"CN\s+SH(\w+)\s+CHINA"  #r"CN\s+(\w+)\s+CHINA"
    match = re.search(isin_pattern, file_content)
    if match:
        isin = match.group(1)
    else:
        isin = ""  # Empty string if no match found
    return isin

def extract_amount(file_content):
    amount_pattern = r"\b([\d,]+)\s+NOM\b"
    match = re.search(amount_pattern, file_content)
    if match:
        amount = match.group(1).replace(',', '')  # Remove commas from the amount
    else:
        amount = ""  # Empty string if no match found
    return amount


if __name__=="__main__":
    #result = process_hk_pdf_file(hk_file="HK_nil.pdf", ledger_file="Ledger_Raw Data.xls")
    # Read the PDF file
    hk_file = "Input_files/HK.pdf"
    with open(hk_file, "rb") as pdf_file:
        #pdf_file = io.BytesIO(pdf_bytes)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        num_pages = len(pdf_reader.pages)
        file_content = ""
        
        # Extract text from each page
        for page_number in range(num_pages):
            page = pdf_reader.pages[page_number]
            file_content += page.extract_text()

    ledger_file="Input_files/Ledger_Raw Data.xls"
    ledger_df = pd.read_excel(ledger_file)
    df, date, msg = process_hk_pdf_file(file_content, ledger_df)
