import pandas as pd
from datetime import datetime
import io


def read_Statement(df):
    msg = ''
    try:
        df.rename(columns=lambda x: x.strip(), inplace=True)
        df.dropna(subset='ISIN Code', inplace=True)
        return msg, df
    except Exception as e:
        msg = "Error message in read_Statement: " + str(e)
        return msg, None


def mutual_fund_vistima(fileBytes):
    data = io.BytesIO(fileBytes)
    msg = ''
    try:
        df = pd.read_csv(data, header=1)
        df.rename(columns=lambda x: x.strip(), inplace=True)
        df.dropna(subset='ISIN Code', inplace=True)
        date_statement = df['Date'][0]
        date_object_statement = datetime.strptime(date_statement, '%Y/%m/%d')
        formatted_date_statement = date_object_statement.strftime('%Y-%m-%d')
        return df, formatted_date_statement, msg
    except Exception as e:
        msg = "Error message in mutual_fund_vistima: " + str(e)
        return None, None, msg


def mutual_fund_leger(fileBytes, files):
    data = io.BytesIO(fileBytes)
    msg = ''
    try:
        df = pd.read_excel(data, sheet_name='Mutual Funds')
        df.rename(columns=lambda x: x.strip(), inplace=True)
        for file in files:
            filename = str(file.filename)
        # print(filename)
        date_ledger = filename.split('.')[1].split('-')[-1]
        date_object_ledger = datetime.strptime(date_ledger, '%d %b %y')
        formatted_date_ledger = date_object_ledger.strftime('%Y-%m-%d')
        # formatted_date_ledger = '2023-06-23'
        return df, formatted_date_ledger, msg
    except Exception as e:
        msg = "Error message in mutual_fund_leger: " + str(e)
        return None, None, msg


def read_Ledger(df):
    msg = ''
    try:
        df.rename(columns=lambda x: x.strip(), inplace=True)
        return msg, df
    except Exception as e:
        msg = "read_Ledger, Error message: " + str(e)
        return msg, None


def handle_zero(x):
    ans = round(x, 2)
    if abs(ans) < 0.001:
        ans = 0
    return ans


def mutual_fund_recon(df1, df2):
    msg_statement, df_statement = read_Statement(df1)
    msg_ledger, df_ledger = read_Ledger(df2)
    # return df_statement, str(df_statement.shape)
    cols = ['ISIN Code', 'Name of Security', 'Statement/Ledger', 'Buy/Sell', 'units', 'Source', 'CURRENCY']

    # Filter columns for statement
    df_stt = df_statement[['ISIN Code', 'Name of Security', 'Balance', 'NAV Currency']]
    df_stt['Statement/Ledger'] = 'Statement'
    df_stt['Source'] = "X'ACT-VESTIMA"
    df_stt['Buy/Sell'] = 'Buy'
    df_stt = df_stt.rename(columns={'Balance': 'units',
                                    'NAV Currency': 'CURRENCY'})
    df_stt = df_stt[cols]

    # compute units for ledger
    ledger_units = []
    for index, row in df_ledger.iterrows():
        if row['Type of transaction'].upper() in ['BUY', 'TRANSFER IN']:
            tmp_unit = -1 * row['Qty/Unit']
        else:
            tmp_unit = row['Qty/Unit']
        ledger_units.append(tmp_unit)

    # Filter columns for ledger
    df_ldg = df_ledger[['ISIN', 'Fund Name', 'Type of transaction', 'Investment Currency']]
    df_ldg = df_ldg.rename(columns={'ISIN': 'ISIN Code',
                                    'Fund Name': 'Name of Security',
                                    'Type of transaction': 'Buy/Sell',
                                    'Investment Currency': 'CURRENCY'})
    df_ldg['Statement/Ledger'] = 'Ledger'
    df_ldg['units'] = ledger_units
    df_ldg['Source'] = 'Bond custody excel file'
    df_ldg = df_ldg[cols]

    # Combine dataframes from statement and ledger
    df_all = pd.concat([df_stt, df_ldg], ignore_index=True)

    # Check breaks
    df_breaks = df_all.groupby('ISIN Code')['units'].sum().reset_index()
    df_breaks['Sum of Units'] = df_breaks.apply(lambda row: handle_zero(row['units']), axis=1)
    df_output = df_breaks[['ISIN Code', 'Sum of Units']]

    isin_breaks = df_breaks[df_breaks['Sum of Units'] != 0]['ISIN Code'].to_list()
    if len(isin_breaks) > 0:
        df_details = df_all[df_all['ISIN Code'].isin(isin_breaks)]
        df_details = df_details.sort_values(by='ISIN Code').reset_index()
        return df_details, msg_statement + msg_ledger
    else:
        return df_output, msg_statement + msg_ledger
