# -*- coding: utf-8 -*-
"""
Created on Wed Jun 28 18:15:53 2023

@author: yanminghao
"""

import pandas as pd
import numpy as np
import json
from update_IBCode import main_read
import PyPDF2
from HK import process_hk_pdf_file
from MAS import process_mas_txt_files
import io
import openpyxl

#summit (Ledger_Raw Data)
def Summit_data_process(bytes_data):
    try:
        Msg = ""
        data = io.BytesIO(bytes_data)
        db = pd.read_excel(data)
      
        date = pd.to_datetime(db['Position Date'], format='%Y%m%d').dt.date.value_counts().idxmax()
        db['ISIN'] = db["Alt ID"]
        db["Security_name"] = db["Security"]
        db["Statement/Ledger"] = "Statement"
        db["Buy/Sell"] = np.where(db['Settlement Date Net Pos'] < 0 , 'Sell', 'Buy')
        db["Face Amount"] = db['Settlement Date Net Pos']*-1
        db["Source"] = "SUMMIT"
        db["Currency"] = db['Ccy']
        df = db[['ISIN',
                "Security_name",
                "Statement/Ledger",
                "Buy/Sell",
                "Face Amount",
                "Source",
                "Currency",
                "Position Style",
                ]]
        return df, str(date), Msg
    except Exception as e:
        Msg = str(e)
        #print(Msg)
        return None, None, Msg
    
#Clearstream
def Clearstream_data_process(bytes_data):
    try:
        Msg = ""    
        data = io.BytesIO(bytes_data)
        db = pd.read_excel(data)
        date = pd.to_datetime(db['Business Date'], format='%Y%m%d').dt.date.value_counts().idxmax()
        db['ISIN'] = db["Fin. instrument   "]
        db["Security_name"] = db["Fin. instr. description"]
        db["Statement/Ledger"] = "Statement"
        db["Buy/Sell"] = 'Buy'
        db["Face Amount"] = db['Quantity']
        db["Source"] = "Clearstream"
        db["Currency"] = db["Fin. instr. description"].str[:3]
        df = db[['ISIN',
                "Security_name",
                "Statement/Ledger",
                "Buy/Sell",
                "Face Amount",
                "Source",
                "Currency",
                ]]   
        return df, str(date), Msg
    except Exception as e:
        Msg = str(e)
        return None, None, Msg
    
#DBS
def DBS_data_process(bytes_data):
    try:
        Msg = ""     
        data = io.BytesIO(bytes_data)
        db = pd.read_excel(data, sheet_name='Holdings')        
        date = pd.to_datetime(db['Value date as at'], format='%d %b %Y').dt.date.value_counts().idxmax()
        db['ISIN'] = db["ISIN"]
        db["Security_name"] = db["Security name"]
        db["Statement/Ledger"] = "Statement"
        db["Buy/Sell"] = 'Buy'
        db["Face Amount"] = db['Settled balance']
        db["Source"] = "DBS"
        db["Currency"] = db["Security currency"]
        df = db[['ISIN',
                "Security_name",
                "Statement/Ledger",
                "Buy/Sell",
                "Face Amount",
                "Source",
                "Currency",
                ]]   
        return df, str(date), Msg
    except Exception as e:
        Msg = str(e)
        return None, None, Msg

#CCDC
def CCDC_data_process(bytes_data, name):
    try:
        Msg = ""   
        data = io.BytesIO(bytes_data)
        db_1 = pd.read_excel(data)  
        date = db_1.iloc[0][1].replace('年', '-').replace('月', '-').replace('日', '')
        _index = db_1.index[db_1.iloc[:, 0] == '序号'].tolist()[0]#find '序号's position
        db_1 = db_1.tail(db_1.shape[0]-_index)
        new_header = db_1.iloc[0] #grab the first row for the header
        db_1 = db_1[1:] #take the data less the header row
        db_1.columns = new_header #set the header row as the df header    
        
        #Map IB Code to ISIN
        IbCode_ISIN = main_read()
        db_1['ISIN'] = db_1["债券代码"].astype(str).map(IbCode_ISIN)
        print("11111111",db_1[['ISIN',"债券代码"]],IbCode_ISIN)
        #Map Security name from Summit data
        db_2= pd.read_excel(name) 
        ISIN_Security = db_2.drop_duplicates(subset='Alt ID').set_index("Alt ID")["Security"]
        print("222222222", ISIN_Security)
        db_1["Security_name"] = db_1["ISIN"].map(ISIN_Security)
        
        #check if IB code information is sufficient or not.
        check_1 = False
        check_2 = False
        if (db_1['Security_name'].isna() & ~db_1['ISIN'].isna()).any():
            check_1 = True
        if (db_1['ISIN'].isna() & ~db_1['债券简称'].isna()).any():
            check_2 = True
        
        print("33333333", check_1, check_2)
        check_result_1 = db_1.loc[db_1['Security_name'].isna() & ~db_1['ISIN'].isna(), ['ISIN','债券代码']].values
        check_result_2 = db_1.loc[db_1['ISIN'].isna() & ~db_1['债券简称'].isna(), '债券代码'].values
        print('4444444444',check_result_1,check_result_2)
        if check_1 and not check_2:
            Msg = '无法在ledger中找到IB Code:'+ str(check_result_1[0][1])+'对应的ISIN: '+ str(check_result_1[0][0]) + ', 请在CCDC holding设置中更新。'
            return None, None, Msg
        elif check_2 and not check_1:
            Msg = '无法找到 IB Code '+ str(check_result_2)+'对应的ISIN, 请在CCDC holding设置中添加。'
            return None, None, Msg
        elif check_1 and check_2:
            Msg = '无法在ledger中找到IB Code:'+ str(check_result_1[0][1])+'对应的ISIN: '+ str(check_result_1[0][0]) + ', 请在CCDC holding设置中更新。\n' + \
                '无法找到 IB Code '+ str(check_result_2)+'对应的ISIN, 请在CCDC holding设置中添加。'
            return None, None, Msg
        else:
            db_1["Statement/Ledger"] = "Statement"
            db_1["Buy/Sell"] = 'Buy'
            db_1["Face Amount"] = db_1['合计'].astype(float)*10000
            db_1["Source"] = "CCDC"
            db_1["Currency"] = "CNY"
            df = db_1[['ISIN',
                    "Security_name",
                    "Statement/Ledger",
                    "Buy/Sell",
                    "Face Amount",
                    "Source",
                    "Currency",
                    ]]   
            return df, date, Msg
    except Exception as e:
        Msg = str(e)
        return None, None, Msg        

def Bond_Custody_Inter_Reconciliation(**kwargs):
    try:
        Msg = ""  

        Summit_data = kwargs['Summit']
        #Map Asset/Liab from Summit data
        ISIN_AssetLiab = Summit_data.drop_duplicates(subset='ISIN').set_index("ISIN")["Position Style"]
        del Summit_data['Position Style']
        kwargs['Summit'] = Summit_data
        
        
        df = pd.concat([value for value in kwargs.values()])
        #Sum Face Amount by each ISIN and filter out sum value=0
        df['Face Amount'] = df['Face Amount'].astype(float)
        df_sum = df.groupby('ISIN')['Face Amount'].sum().reset_index()
        df_sum = df_sum.loc[df_sum['Face Amount'] != 0]
        
        #Map Security name, Source, Statement/Ledger, Currency from Reconciliation data
        ISIN_Security = df.drop_duplicates(subset='ISIN').set_index("ISIN")["Security_name"]  
        ISIN_Source = df.drop_duplicates(subset='ISIN').set_index("ISIN")["Source"] 
        ISIN_StatementLedger = df.drop_duplicates(subset='ISIN').set_index("ISIN")["Statement/Ledger"] 
        ISIN_CCY = df.drop_duplicates(subset='ISIN').set_index("ISIN")["Currency"] 
        df_sum["Sec Name"] = df_sum["ISIN"].map(ISIN_Security)
        df_sum["Source"] = df_sum["ISIN"].map(ISIN_Source)
        df_sum["Statement/Ledger"] = df_sum["ISIN"].map(ISIN_StatementLedger)
        df_sum["Currency"] = df_sum["ISIN"].map(ISIN_CCY)
        
        #Map Asset/Liab from Summit data, it is "buy" if =='asset', else is "sell"
        df_sum["Asset/Liab"] = df_sum["ISIN"].map(ISIN_AssetLiab)
        df_sum["Buy/Sell"] = 'Sell'
        df_sum.loc[df_sum["Asset/Liab"].str.lower()=='asset', "Buy/Sell"]= 'Buy'
        
        #add Explanation
        df_sum.loc[df_sum['Sec Name'].str.contains('S_SHANPU', case=False), 
                   "Break Explanation"] = 'CD Issuance issued by SPDB SG BRH'
        df_sum['Amount'] = df_sum['Face Amount']
        df_sum["Day Count"] = '-'
        df_sum["Responsible Party"] = 'Treasury Ops'
        df_sum["Settlement date "] = ''
        df_sum["Abnormal (Y/N)"] = 'N'
        return df_sum, Msg
  
    except Exception as e:
        Msg = str(e)
        return None, Msg



# def main(**kwargs):
#     if len(kwargs) > 1:
#         Summit_date = kwargs['Summit'][1]       
#         if all(variable == Summit_date for variable in [value[1] for value in kwargs.values()]):
#             df, Msg = Reconciliation(**kwargs)
#             return df, Msg
#         else:
#             Msg = '文件日期不匹配，是否继续'
#             return None, Msg                
#     else:
#         Msg = 'Insuffient Reconciliation files'
#         print(Msg)
#         return None, Msg

# def save_to_csv(df):
#     df.to_csv('Custody_Reconciliation.csv', index=False)         

    
if __name__ == '__main__':
    folder = "Input_files"
    filename_Summit = "SUMMIT bond positions 26 Jun 2023.xlsx"
    filename_clearstream = "Xact  26 Jun 2023.xlsx"
    filename_DBS = "AMR_-DAILY_BOND_HOLDING_REPORT_YEOHTS_SHANPUD3_20230626_432148 - 26 Jun 23.xls"
    filename_ccdc = "副本托管账户总对账单0626-中债.xlsx"
    filename_HK = "HK_nil.pdf" #"HK.pdf"
    filename_MAS = "MAS.txt"
    
    with open(folder+"/"+filename_Summit, 'rb') as fp:
        db_summit = fp.read()   

    with open(folder+"/"+filename_clearstream, 'rb') as fp:
        db_clearstream = fp.read()   

    with open(folder+"/"+filename_DBS, 'rb') as fp:
        db_DBS = fp.read()           

    with open(folder+"/"+filename_ccdc, 'rb') as fp:
        db_ccdc = fp.read()            
        
    with open(folder+"/"+filename_HK, 'rb') as fp:
        db_HK = fp.read()     

    with open(folder+"/"+filename_MAS, 'rb') as fp:
        db_MAS = fp.read()             


    #process input data
    result_Summit,_,_ = Summit_data_process(db_summit)
    result_Clearstream,_,_ = Clearstream_data_process(db_clearstream)
    result_DBS,_,_ = DBS_data_process(db_DBS)
    result_ccdc,_,_ = CCDC_data_process(db_ccdc, db_summit) 
    result_HK,_,_ = process_hk_pdf_file(db_HK, db_summit) 
    result_MAS,_,_ = process_mas_txt_files(db_MAS, db_summit) 
    
    #main
    df = main(Summit=result_Summit, 
              Clearstream=result_Clearstream, 
              DBS=result_DBS, 
              CCDC=result_ccdc, 
              HK=result_ccdc, 
              MAS=result_MAS,
              )