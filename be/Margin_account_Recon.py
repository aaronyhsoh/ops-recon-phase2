# -*- coding: utf-8 -*-
"""
Created on Fri Jun 30 17:44:49 2023

@author: yanminghao
"""

import pandas as pd
import numpy as np
import io

def Margin_Account_Process(bytes_data):
    try:
        Msg = ""
        subject_ID = ['10400100',
                      '10400101',
                      '10400102',
                      ]

        #convert Bytes data to dataframe
        data = io.BytesIO(bytes_data)
        data = pd.read_excel(data)

        #extract date
        date = [value for value in data.columns if 'F86' in value][0].split('\n')[-1]     
         
        #Format dataframe        
        row_indices, col_indices = np.where(data.values == 'Book')
        if row_indices[0] > 0 :
            data = data.tail(data.shape[0]-row_indices[0])
        if col_indices[0] > 0 : 
            data = data.drop(data.columns[col_indices[0]-1], axis=1)
        new_header = data.iloc[0] #grab the first row for the header
        data = data[1:] #take the data less the header row
        data.columns = new_header #set the header row as the df header   
        
        
        #Select Book is 9928
        data = data.loc[data['Book'] == "9928"]
        #Select Subject ID
        data = data.loc[data['Subject No'].isin(subject_ID)]
        #Select 全币折美元
        data = data.loc[data['Currency Chinese Name']=="全币折美元"]
        return data, date, Msg
    except Exception as e:
        Msg = str(e)
        return None, None, Msg

def Margin_Account_Recon(df_Margin):
    try:
        Msg = ""
        columns =["Subject No",
              "Level II subject",
              "Level I subject",
              "Subject name",
              "Subject level",
              "Previous period debit balance",
              "Previous period credit balance",
              "Debit amount",
              "Credit Amount",
              "Current period debit balance",
              "Current period credit balance",
              "Closing Balance",
              "Description",
              ]
        #Calculate Closing Balance
        df_Margin["Closing Balance"] = df_Margin["Current period debit balance"] - df_Margin["Current period credit balance"]
        
        df_Margin['Description']=""
        df_Margin["Level II subject"] = df_Margin['Subject No'].astype(str).str[:6]
        df_Margin["Level I subject"] = df_Margin['Subject No'].astype(str).str[:4]
        return df_Margin[columns], Msg
    except Exception as e:
        Msg = str(e)    
        return None, Msg

# def save_to_csv(df):
#     df.to_csv('Margin Account.csv', index=False)        

if __name__ == '__main__':
    filename_F86 = 'F86_Daily_Trial_Balance (OPS) (5).xlsx-02 May 2022.xlsx'
    with open(filename_F86, 'rb') as fp:
        fileBytes_F86 = fp.read()
    df_Margin, date_margin, Msg_Margin = Margin_Account_Process(fileBytes_F86)
    df = Margin_Account_Recon(df_Margin)
    # save_to_csv(df_Margin)