# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 13:46:18 2023

@author: billy.yu
"""

import pandas as pd
from datetime import datetime
import io

def read_Customer_Statement(fileBytes):
    msg = ''
    try:
        columns = ['Value date as at','Service location','Securities account name','Securities account number','Security type',
           'Security name','ISIN','Place of settlement','Settled balance','Anticipated debits','Available balance',
           'Anticipated credits','Traded balance','Security currency','Security price','Indicative settled value',
           'Indicative traded value','Indicative settled value in SGD','Indicative traded value in SGD']
        sheetname = 'Holdings'
        data = io.BytesIO(fileBytes)
        df = pd.read_excel(data, sheet_name=sheetname, usecols=columns)
        return msg, df
            
    except Exception as e:
        msg = "An error occurred while processing file, Error message: {str(e)}"
#        print(f"An error occurred while processing file")
#        print(f"Error message: {str(e)}")
        return msg, None

def read_Ledger(fileBytes):
    msg = ''
    try:
        columns = ['Summit Ref','ISIN','Security Name','Market Type','Buy/Sell','Quantity','Clean Price','Dirty Price','Yield',
               'Trade Date','Value Date','Settlement Date','Maturity Date','Accrued interest','Currency',
               'Proceeds/Settlement Amount','Counterparty Code','Counterparty Name','RM Name','Customer Custody Account no',
               'Customer Current Account no','Security Withdrawal Fee (FOP transfer)','3rd Party Fee','Management of Assets',
               'Custodise with SPDBSG (Y/N)','Maker ID','Checker ID','Remarks','Market Price']
    #    sheetname_ledger = 'Bond'
        sheetname_ledger = 'Transactions'
        data = io.BytesIO(fileBytes)
        df = pd.read_excel(data, sheet_name=sheetname_ledger, usecols=columns)
        return msg, df
            
    except Exception as e:
        msg = "An error occurred while processing file, Error message: {str(e)}"
#        print(f"An error occurred while processing file")
#        print(f"Error message: {str(e)}")
        return msg, None

def test():
    data = {
    'ISIN': ['XS1605397394', 'XS1605397394', 'XS1605397395', 'XS1605397395'],
    'Securities Name': ['S_TCZIRA_5.125_50322', 'TURKIYE CUMHURIYETI ZIRAAT BANKASI 5.125 PCT NOTES DUE 03.05.2022', 'S_TCZIRA_5.125_50322', 'TURKIYE CUMHURIYETI ZIRAAT BANKASI 5.125 PCT NOTES DUE 03.05.2022'],
    'Statement/Ledger': ['Ledger', 'Statement', 'Ledger', 'Statement'],
    'Buy/Sell': ['Buy', 'Buy', 'Buy', 'Buy'],
    'Face Amount': ['-300,000.00', '300,000.00', '-400,000.00', '410,000.00'],
    'Source': ['Bond custody excel file', 'DBS', 'Bond custody excel file', 'DBS'],
    'Security currency': ['USD', 'USD', 'USD', 'USD']
    }
    df_Recon = pd.DataFrame(data)
    df_Recon['Face Amount'] = df_Recon['Face Amount'].str.replace(',', '').astype(float)

    return df_Recon

def Customer_Statement(fileBytes):
    msg, df_DBS = read_Customer_Statement(fileBytes)  
    date_DBS = list(df_DBS['Value date as at'])[0]
    print(date_DBS)
    date_DBS = datetime.strptime(date_DBS, '%d %b %Y')
    date_DBS = date_DBS.strftime('%Y-%m-%d')
    print(date_DBS)
    
    recon_DBS_columns = ['ISIN','Securities Name','Statement/Ledger','Buy/Sell','Face Amount','Source','Security currency']
    df_recon_DBS = pd.DataFrame(columns=recon_DBS_columns)
    df_recon_DBS['ISIN'] = df_DBS['ISIN']
    df_recon_DBS['Securities Name'] = df_DBS['Security name']
    df_recon_DBS['Statement/Ledger'] = 'Statement'
    df_recon_DBS['Buy/Sell'] = 'Buy'
    df_recon_DBS['Face Amount'] = df_DBS['Settled balance']
    df_recon_DBS['Source'] = 'DBS'
    df_recon_DBS['Security currency'] = df_DBS['Security currency']
    
    return df_recon_DBS, date_DBS, msg
    
def Ledger(fileBytes):
    msg, df_ledger = read_Ledger(fileBytes)
    recon_Ledger_columns = ['ISIN','Securities Name','Statement/Ledger','Buy/Sell','Face Amount','Source','Security currency']

    df_recon_Ledger = pd.DataFrame(columns=recon_Ledger_columns)
    df_recon_Ledger['ISIN'] = df_ledger['ISIN']
    df_recon_Ledger['Securities Name'] = df_ledger['Security Name']
    df_recon_Ledger['Statement/Ledger'] = 'Ledger'
    df_recon_Ledger['Buy/Sell'] = df_ledger['Buy/Sell']
    df_recon_Ledger['Face Amount'] = df_ledger.apply(lambda row: row['Quantity']*(-1) if str(row['Buy/Sell']).upper() == 'BUY'
                                                    else row['Quantity'], axis=1)
    df_recon_Ledger['Source'] = 'Bond custody excel file'
    df_recon_Ledger['Security currency'] = df_ledger['Currency']

    return df_recon_Ledger, '', msg

def recon_DBS(df_recon_DBS, df_recon_Ledger):
    msg = ''
    try:
    
      #  df_Recon = test()
      
        df_Recon = pd.concat([df_recon_DBS, df_recon_Ledger])
        
        df_pt = df_Recon.pivot_table(index=['ISIN', 'Statement/Ledger'], values='Face Amount', aggfunc=sum, fill_value=0)
        df_pt.reset_index(inplace=True)
        df_pt['Row Labels'] = df_pt['ISIN']
        df_pt.drop('ISIN', axis=1, inplace=True)
        
        df_pt_final = pd.DataFrame(columns=['Row Labels', 'Sum of Face Amount'])
        for isin in df_pt['Row Labels'].unique():
            df_isin = df_pt[df_pt['Row Labels'] == isin]
            df_pt_final = df_pt_final.append({'Row Labels': isin, 'Sum of Face Amount': df_isin['Face Amount'].sum()}, ignore_index=True)
            df_isin2 = df_isin.drop('Row Labels', axis=1)
            df_isin2 = df_isin2.rename(columns={'Statement/Ledger': 'Row Labels', 
                                           'Face Amount': 'Sum of Face Amount'})
    
            df_pt_final = pd.concat([df_pt_final, df_isin2], axis=0)
        
        grand_total = df_Recon['Face Amount'].sum()
        df_pt_final = df_pt_final.append({'Row Labels':'Grand Total', 'Sum of Face Amount':grand_total}, ignore_index=True)
        
        return df_pt_final, msg
    except Exception as e:
        msg = "An error occurred while processing file, Error message: {str(e)}"
#        print(f"An error occurred while processing file")
#        print(f"Error message: {str(e)}")
        return None, msg

        
    
    
if __name__ == '__main__':
    filename_DBS = 'CLIENT_DBS_HOLDINGS_YEOHTS_SHANPUD3_20211110_1e1960 - 31 Jan 2022.xls'
    sheetname_DBS = 'Holdings'
    columns_DBS = ['Value date as at','Service location','Securities account name','Securities account number','Security type',
           'Security name','ISIN','Place of settlement','Settled balance','Anticipated debits','Available balance',
           'Anticipated credits','Traded balance','Security currency','Security price','Indicative settled value',
           'Indicative traded value','Indicative settled value in SGD','Indicative traded value in SGD']
    
    filename_ledger = 'Bond Custody Services working file V1.0.xlsx-31 Jan 2022.xlsx'
#    sheetname_ledger = 'Bond'
    sheetname_ledger = 'Transactions'
    columns_ledger = ['Summit Ref','ISIN','Security Name','Market Type','Buy/Sell','Quantity','Clean Price','Dirty Price','Yield',
               'Trade Date','Value Date','Settlement Date','Maturity Date','Accrued interest','Currency',
               'Proceeds/Settlement Amount','Counterparty Code','Counterparty Name','RM Name','Customer Custody Account no',
               'Customer Current Account no','Security Withdrawal Fee (FOP transfer)','3rd Party Fee','Management of Assets',
               'Custodise with SPDBSG (Y/N)','Maker ID','Checker ID','Remarks','Market Price']
    
    recon_Ledger_columns = ['ISIN','Securities Name','Statement/Ledger','Buy/Sell','Face Amount','Source','Security currency']
    with open(filename_DBS, 'rb') as fp:
        fileBytes_DBS = fp.read()
    with open(filename_ledger, 'rb') as fp:
        fileBytes_Ledger = fp.read()
    df_recon_DBS, date_DBS, msg_DBS = Customer_Statement(fileBytes_DBS)
    df_recon_Ledger, date_Ledger, msg_Ledger = Ledger(fileBytes_Ledger)
    
    df_BREAKS, msg = recon_DBS(df_recon_DBS, df_recon_Ledger)
    
    print('date: ', date_DBS)
    print(df_BREAKS)
