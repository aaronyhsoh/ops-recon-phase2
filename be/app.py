from base64 import b64encode
from flask import Flask, request, jsonify
from tempfile import NamedTemporaryFile
import msoffcrypto
import json
import random
from datetime import date, timedelta
import pikepdf
import pandas as pd
from waitress import serve
from collections import defaultdict
import io
from os import path
from Bond_Custody_Inter_Reconciliation import *
from Margin_account_Recon import *
from MAS import *
from HK import *
from Bond_Client import *
from Mutual_Fund import *

app = Flask(__name__)
app.logger.setLevel("INFO")
fileDic = defaultdict(lambda:None)
# ===========================================================================================================
# Verifies password for the file if it is password protected as well as sending back the date parsed for the file uploaded.
#
# Receives:
#   file: xlsx, pdf or txt file to be checked for password and verified, and parsing for the date of the file.
#   password: string
#   title: string title of file currently being verified, eg. 'VESTIMA'
# Sends: JSON containing:
#   date: parsed date from the document. this field is only sent if the file is unprotected or can be unprotected using the password.
#   dataframe: parsed dataframe from the document
#   message: any error or warning messages that resulted from parsing the document
#   wrong_password: this field is only sent if the file is password protected and the input password is invalid.
@app.route("/verify", methods=["POST"])
def verify_file():
    if 'file' not in request.files:
        # Handle missing file here
        # Should never end up here
        return
    
    uploaded_file = request.files["file"]
    password = request.form.get("password", "")

    # file title to be verified
    # eg. "Ledger Raw Data"
    title = request.form.get('title', '')

    response_data = {}
    try:
        decrypted_file = decryption_dispatcher(uploaded_file, password)
        fileBytes = decrypted_file.read()
        if title != "":
            fileDic[title]=fileBytes
        if title=="Ledger Raw Data":
            dataframe, parse_date, message = Summit_data_process(fileBytes) ##Your Function HERE
            b = io.BytesIO(fileBytes) ## Some random BytesIO Object
            with open("Ledger Raw Data.xlsx",'wb') as out: ## Open temporary file as bytes
                out.write(b.read()) 

        if title=="CCDC Holding":
            dataframe, parse_date, message = CCDC_data_process(fileBytes, fileDic['Ledger Raw Data']) ##Your Function HERE

        if title=="SPDB HK":
            dataframe, parse_date, message = process_hk_pdf_file(fileBytes, fileDic['Ledger Raw Data']) ##Your Function HERE

        if title=="MAS File":
            dataframe, parse_date, message = process_mas_txt_files(fileBytes, fileDic['Ledger Raw Data']) ##Your Function HERE

        if title=="DBS Holdings":
            dataframe, parse_date, message = DBS_data_process(fileBytes) ##Your Function HERE

        if title=="Clearstream":
            dataframe, parse_date, message = Clearstream_data_process(fileBytes) ##Your Function HERE

        if title=="Customer Statement":
            dataframe, parse_date, message = Customer_Statement(fileBytes) ##Your Function HERE

        if title=="Ledger":
            dataframe, parse_date, message = Ledger(fileBytes) ##Your Function HERE

        if title=="F86":
            dataframe, parse_date, message = Margin_Account_Process(fileBytes) ##Your Function HERE

        if title=="VESTIMA":
            dataframe, parse_date, message = mutual_fund_vistima(fileBytes) ##Your Function HERE

        if title=="Bond Custody Services":
            dataframe, parse_date, message = mutual_fund_leger(fileBytes, request.files.values()) ##Your Function HERE

        decrypted_file.close()
    except (msoffcrypto.exceptions.DecryptionError, msoffcrypto.exceptions.InvalidKeyError, pikepdf._core.PasswordError) as e:
        app.logger.info("/verify, invalid password")
        response_data["wrong_password"] = True


    if not response_data.get("wrong_password"):
        if dataframe is None: #or dataframe.empty
            response_data["dataframe"]=None
        else:
            response_data["dataframe"]=dataframe.to_csv(index=False)
        response_data["date"]=parse_date
        response_data["message"]=message


    response = jsonify(response_data)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

# API route for Bond Custody (Inter.)
@app.route("/bondcustodyinter/reconcile", methods=["POST"])
def bondcustodyinter_reconcile():
    uploaded_files = request.files
    passwords = json.loads(request.form["passwords"])
    dataframes = json.loads(request.form["dataframes"])
    
    if len(request.files) != 6:
        # Handle error
        return
    if len(uploaded_files) != len(passwords):
        return
    
    ledger_raw_data_df= pd.read_csv(io.StringIO(dataframes[0]))
    ccdc_holding_df=pd.read_csv(io.StringIO(dataframes[1]))
    #print("00000000000\n"+dataframes[2])
    spdb_hk_df=pd.read_csv(io.StringIO(dataframes[2]))
    masfile_df=pd.read_csv(io.StringIO(dataframes[3]))
    dbs_holdings_df=pd.read_csv(io.StringIO(dataframes[4]))
    clearstream_df=pd.read_csv(io.StringIO(dataframes[5]))

    #print("1111111111111111111"+ledger_raw_data_df.head())
    # ledger_raw_data, ccdc_holding, spdb_hk, mas_file, dbs_holdings, clearstream, *rest = get_decrypted_files(uploaded_files, passwords, len(request.files))

    # if len(rest) > 0:
    #     # Error: Not supposed to have extra file objects
    #     return
    
    # ledger_raw_data_bytes = ledger_raw_data.read()
    # ccdc_holding_bytes = ccdc_holding.read()
    # spdb_hk_bytes = spdb_hk.read()
    # mas_file_bytes = mas_file.read()
    # dbs_holdings_bytes = dbs_holdings.read()
    # clearstream_bytes = clearstream.read()

    # INSERT FUNCTION HERE
    dataframe, msg = Bond_Custody_Inter_Reconciliation(Summit=ledger_raw_data_df, 
                                                       CCDC=ccdc_holding_df, 
                                                       HK=spdb_hk_df, 
                                                       MAS=masfile_df, 
                                                       DBS=dbs_holdings_df, 
                                                       Clearstream=clearstream_df,
                                                       )
    print("111111111111111111"+msg)
    # To convert csv_data into base64 string:

    response_data = {}
    if dataframe is None or dataframe.empty:
        response_data['cfile']=None
    else:
        csv_data=dataframe.to_csv(index=False)
        cfile_base64 = b64encode(csv_data.encode('utf-8')).decode('utf-8')
        c_str = "data:text/csv;base64," + cfile_base64
        response_data["cfile"]= c_str
    
    response_data["message"]=msg
    
    response = jsonify(response_data)
    response.headers['Access-Control-Allow-Origin'] = '*'  # May be unsafe for production

    # # Close the TemporaryNamedFile file pointers
    # ledger_raw_data.close()
    # ccdc_holding.close()
    # spdb_hk.close()
    # mas_file.close()
    # dbs_holdings.close()
    # clearstream.close()

    return response

# API route for Bond Custody (Client)
@app.route("/bondcustodyclient/reconcile", methods=["POST"])
def bondcustodyclient_reconcile():
    uploaded_files = request.files
    passwords = json.loads(request.form["passwords"])
    dataframes = json.loads(request.form["dataframes"])
    
    if len(request.files) != 2:
        # Handle error
        return
    if len(uploaded_files) != len(passwords):
        return

    customer_statement_df= pd.read_csv(io.StringIO(dataframes[0]))
    ledger_df=pd.read_csv(io.StringIO(dataframes[1]))

    # customer_statement, ledger, *rest = get_decrypted_files(uploaded_files, passwords, len(request.files))

    # if len(rest) > 0:
    #     # Error: Not supposed to have extra file objects
    #     return

    # customer_statement_bytes = customer_statement.read()
    # ledger_bytes = ledger.read()

    # INSERT FUNCTION HERE
    dataframe, msg = recon_DBS(customer_statement_df, ledger_df)
    # print("111111111111111"+msg)

    # To convert csv_data into base64 string:
    response_data = {}
    if dataframe is None or dataframe.empty:
        response_data['cfile']=None
    else:
        csv_data=dataframe.to_csv(index=False)
        cfile_base64 = b64encode(csv_data.encode('utf-8')).decode('utf-8')
        c_str = "data:text/csv;base64," + cfile_base64
        response_data["cfile"]= c_str
    
    response_data["message"]=msg
    
    response = jsonify(response_data)
    response.headers['Access-Control-Allow-Origin'] = '*'  # May be unsafe for production

    # # Close the TemporaryNamedFile file pointers
    # customer_statement.close()
    # ledger.close()

    return response

# API route for Margin Account
@app.route("/marginaccount/reconcile", methods=["POST"])
def marginaccount_reconcile():
    uploaded_files = request.files
    passwords = json.loads(request.form["passwords"])
    dataframes = json.loads(request.form["dataframes"])
    
    if len(request.files) != 1:
        # Handle error
        return
    if len(uploaded_files) != len(passwords):
        return
    
    f86_df= pd.read_csv(io.StringIO(dataframes[0]))

    # f86, *rest = get_decrypted_files(uploaded_files, passwords, len(request.files))

    # if len(rest) > 0:
    #     # Error: Not supposed to have extra file objects
    #     return

    # f86_bytes = f86.read()

    # INSERT FUNCTION HERE
    dataframe, msg = Margin_Account_Recon(f86_df)

    # To convert csv_data into base64 string:
    response_data = {}
    if dataframe is None or dataframe.empty:
        response_data['cfile']=None
    else:
        csv_data=dataframe.to_csv(index=False)
        cfile_base64 = b64encode(csv_data.encode('utf-8')).decode('utf-8')
        c_str = "data:text/csv;base64," + cfile_base64
        response_data["cfile"]= c_str
    
    response_data["message"]=msg
    
    response = jsonify(response_data)
    response.headers['Access-Control-Allow-Origin'] = '*'  # May be unsafe for production

    # # Close the TemporaryNamedFile file pointers
    # f86.close()

    return response

# API route for Mutual Fund
@app.route("/mutualfund/reconcile", methods=["POST"])
def mutualfund_reconcile():
    uploaded_files = request.files
    passwords = json.loads(request.form["passwords"])
    dataframes = json.loads(request.form["dataframes"])
    
    if len(request.files) != 2:
        # Handle error
        return
    if len(uploaded_files) != len(passwords):
        return
    
    uploaded_files = request.files
    file_list = list(uploaded_files.values())
    content = file_list[1].read()
    content_vestima = file_list[0].read()
    vestima_df = pd.read_csv(io.BytesIO(content_vestima), header=1)
    bond_custody_services_df = pd.read_excel(io.BytesIO(content), sheet_name='Mutual Funds')

    # vestima, bond_custody_services, *rest = get_decrypted_files(uploaded_files, passwords, len(request.files))

    # if len(rest) > 0:
    #     # Error: Not supposed to have extra file objects
    #     return

    # vestima_bytes = vestima.read()
    # bond_custody_services_bytes = bond_custody_services.read()

    # INSERT FUNCTION HERE
    dataframe, msg = mutual_fund_recon(vestima_df, bond_custody_services_df)

    # To convert csv_data into base64 string:
    response_data = {}
    if dataframe is None or dataframe.empty:
        response_data['cfile']=None
    else:
        csv_data=dataframe.to_csv(index=False)
        cfile_base64 = b64encode(csv_data.encode('utf-8')).decode('utf-8')
        c_str = "data:text/csv;base64," + cfile_base64
        response_data["cfile"]= c_str
    
    response_data["message"]=msg
    
    response = jsonify(response_data)
    response.headers['Access-Control-Allow-Origin'] = '*'  # May be unsafe for production

    # # Close the TemporaryNamedFile file pointers
    # vestima.close()
    # bond_custody_services.close()

    return response

# 'file_path.txt' contains the user's folder path settings in string format
    # NOTE: this has been validated, it is guaranteed to exist
        # however, this folder has not been validated if it contains the correct files
@app.route("/all", methods=["GET"])
def allFunc():
    
    response_data = {}

    with open('file_path.txt', 'r') as file:
        filePath = file.read()    

    # Temporary csv files
    # Can remove after inserting functions ###############
    cFileList=[None, None, None, None]
    for i,csv_file_path in enumerate(['./test100.csv', './test200.csv', './test100.csv']):
        with open(csv_file_path, 'rb') as file:
            csv_data = file.read()
            cfile_base64 = b64encode(csv_data).decode('utf-8')
        c_str = "data:text/csv;base64," + cfile_base64
        cFileList[i]=c_str
    ######################################################

    ############## Include this chunk of code after inserting function ################
    # cFileList, msg = RECONCILE_ALL_FUNCTION(filePath) #insert your function here
    # for i,df in enumerate(cFileList):
    #     if df is not None:
    #         csv_data=df.to_csv(index=False)
    #         cfile_base64 = b64encode(csv_data.encode('utf-8')).decode('utf-8')
    #         c_str = "data:text/csv;base64," + cfile_base64
    #         cFileList[i]=c_str
    ####################################################################################

    # Error checking
        # if all cFile in cFileList is None
    if all(map(lambda cFile: cFile == None, cFileList)):
        response_data["cfile"]= None
        response_data["status"]="Error"
        response_data["message"]="No file"
    else:
        response_data["cfile"]= cFileList    
        response_data["status"]="Succeeded"

    response = jsonify(response_data)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route("/history", methods=["POST"])
def history():
    date = request.form.get("date")

    response_data = {}

    # Temporary csv files
    # Can remove after inserting functions ###############
    cFileList=[None, None, None, None]
    for i,csv_file_path in enumerate(['./test100.csv', './test200.csv', './test100.csv']):
        with open(csv_file_path, 'rb') as file:
            csv_data = file.read()
            cfile_base64 = b64encode(csv_data).decode('utf-8')
        c_str = "data:text/csv;base64," + cfile_base64
        cFileList[i]=c_str
    ######################################################

    ############## Include this chunk of code after inserting function ################
    # cFileList, msg = GET_DATAFRAMES_FROM_DATE_FUNCTION(date) #insert your function here
    # for i,df in enumerate(cFileList):
    #     if df is not None:
    #         csv_data=df.to_csv(index=False)
    #         cfile_base64 = b64encode(csv_data.encode('utf-8')).decode('utf-8')
    #         c_str = "data:text/csv;base64," + cfile_base64
    #         cFileList[i]=c_str
    ####################################################################################

    # Error checking
        # if all cFile in cFileList is None
    if all(map(lambda cFile: cFile == None, cFileList)):
        response_data["cfile"]= None
        response_data["status"]="Error"
        response_data["message"]="No records found for the chosen date"
    else:
        response_data["cfile"]= cFileList
        response_data['status']='Succeeded'

    response = jsonify(response_data)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route("/get_calender_status", methods=["GET"])
def get_calender_status():
    response_data = {}

    ## TEMP DATAFRAME ####    
    # Can remove after inserting functions ##############################
    data = {
        'date': [
            str(date.today()),
            str(date.today() - timedelta(days=1)),
            str(date.today() - timedelta(days=2)),
            str(date.today() - timedelta(days=3)),
        ],
        'flag': [
            '1',
            '0',
            '1',
            '2',
        ]
    }
    df_dates = pd.DataFrame.from_dict(data)
    ###################################################################

    ############## Include this chunk of code after inserting function ################
    # df_dates = GET_CALENDER_STATUS_FUNCTION() #insert your function here
    ####################################################################################

    response_data['data'] = df_dates.to_json(orient='split', date_format='iso')

    response = jsonify(response_data)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

#for the CCDC Holding Setting：
@app.route("/system_Settings", methods=["POST"])
def system_setting():
    settingValues= request.form
    temp = json.dumps(settingValues)
    CodeDict = json.loads(temp)
    IBCode = CodeDict['IBCode']  
    ISIN = CodeDict['ISIN']
    configFile = 'config_test.json'
    with open(configFile, 'r') as file:
        data = json.load(file)

    data[IBCode] = ISIN

    # Write the updated dictionary back to the JSON file
    with open(configFile, 'w') as file:
        json.dump(data, file, indent=4)
    response_data = {"status":"updated"}
    response = jsonify(response_data)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

#for the Path Setting for ReconcileAll：
@app.route("/path_Settings", methods=["POST"])
def path_setting():
    settingValues= request.form
    temp = json.dumps(settingValues)
    CodeDict = json.loads(temp)
    folderPath = CodeDict['folderPath']
    configFile = 'file_path.txt'

    # Validate folderPath exists
    if path.isdir(folderPath):
        with open(configFile, 'w') as file:
            file.write(folderPath)
        response_data = {"status":"updated"}
    else:
        response_data = {"status":"error", "error": "Invalid file path"}
    
    response = jsonify(response_data)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

#for placeholder1
@app.route("/placeholder1", methods=["POST"])
def placeholder1():
    settingValues= request.form
    temp = json.dumps(settingValues)
    CodeDict = json.loads(temp)
    Code = CodeDict['Code']  
    Number = CodeDict['Number']
    configFile = 'placeholder1.json'
    with open(configFile, 'r') as file:
        data = json.load(file)

    data[Code] = Number

    # Write the updated dictionary back to the JSON file
    with open(configFile, 'w') as file:
        json.dump(data, file, indent=4)
    response_data = {"status":"updated"}
    response = jsonify(response_data)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

#for placeholder2
@app.route("/placeholder2", methods=["POST"])
def placeholder2():
    settingValues= request.form
    temp = json.dumps(settingValues)
    CodeDict = json.loads(temp)
    Code = CodeDict['Code']  
    Number = CodeDict['Number']
    configFile = 'placeholder2.json'
    with open(configFile, 'r') as file:
        data = json.load(file)

    data[Code] = Number

    # Write the updated dictionary back to the JSON file
    with open(configFile, 'w') as file:
        json.dump(data, file, indent=4)
    response_data = {"status":"updated"}
    response = jsonify(response_data)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

# Dispatch the file received directly according to its mimetype.
# Return:
#   NamedTemporaryFile, with its content filled with a decrypted version of the file received from the frontend.
def decryption_dispatcher(uploaded_file, password):
    if uploaded_file.mimetype == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" or uploaded_file.mimetype == "application/vnd.ms-excel":
        return get_decrypted_xlsx(uploaded_file, password)
    elif uploaded_file.mimetype == "application/pdf":
        return get_decrypted_pdf(uploaded_file, password)
    elif uploaded_file.mimetype == "text/plain" or uploaded_file.mimetype == "text/csv":
        return convert_uploaded_file_to_temporary_file_object(uploaded_file)
    else:
        # Should never reach here
        raise RuntimeError("The uploaded file is of an unknown type.")

# Create a NamedTemporaryFile with the FileStorage object received directly via Flask's uploaded files.
# Return:
#   NamedTemporaryFile, which can be manipulated in the same fashion as Python file objects.
def convert_uploaded_file_to_temporary_file_object(uploaded_file):
    tmp_uploaded_file = NamedTemporaryFile()
    tmp_uploaded_file.write(uploaded_file.read())
    tmp_uploaded_file.flush()
    tmp_uploaded_file.seek(0)
    return tmp_uploaded_file

# Decrypts .xlsx files with the password.
# This should be assumed to be done in place, so the original NamedTemporaryFile will be mutated. 
# If the file is unprotected, it will return the file as is, with the file pointer seeked back to the start.
# This is implemented with a third party library `msoffcrypto-tool`.
# Return:
#   NamedTemporaryFile, which has been decrypted if necessary, or NamedTemporaryFile with
#   the file pointer seeked to 0.
def get_decrypted_xlsx(uploaded_file, password):
    tmp_uploaded_file = convert_uploaded_file_to_temporary_file_object(uploaded_file)

    decrypted_file = NamedTemporaryFile()
    try:
        office_file = msoffcrypto.OfficeFile(tmp_uploaded_file)
        office_file.load_key(password=password)
        office_file.decrypt(decrypted_file)
    except (msoffcrypto.exceptions.FileFormatError, msoffcrypto.exceptions.ParseError) as e:
        # msoffcrypto only tells us that the file is not encrypted via an exception
        tmp_uploaded_file.seek(0)
        return tmp_uploaded_file
    except (msoffcrypto.exceptions.DecryptionError, msoffcrypto.exceptions.InvalidKeyError) as e:
        raise e
    decrypted_file.seek(0)
    return decrypted_file

# Decrypts .pdf files with the password.
# This should be assumed to be done in place, so the original NamedTemporaryFile will be mutated. 
# If the file is unprotected, it will return the file as is, with the file pointer seeked back to the start.
# This is implemented with a third party library `pikepdf`.
# Return:
#   NamedTemporaryFile, which has been decrypted if necessary, or NamedTemporaryFile with
#   the file pointer seeked to 0.
def get_decrypted_pdf(uploaded_file, password):
    decrypted_file = NamedTemporaryFile()
    try:
        tmp_uploaded_file = convert_uploaded_file_to_temporary_file_object(uploaded_file)
        tmp_pdf = pikepdf.open(tmp_uploaded_file, password=password)
        tmp_pdf.save(decrypted_file)
        decrypted_file.seek(0)
    except pikepdf._core.PasswordError as e:
        raise e
    return decrypted_file

# Based on the number of uploaded files, return a list of decrypted files.
def get_decrypted_files(uploaded_files, passwords, length):
    if length <= 0:
        # Invalid length
        return

    decrypted_files = []

    for i in range(length):
        curr_decrypted_file_pw = passwords[i]
        curr_decrypted_uploaded_file = uploaded_files[str(i)]
        curr_file = decryption_dispatcher(curr_decrypted_uploaded_file, password=curr_decrypted_file_pw)
        decrypted_files.append(curr_file)
    
    return decrypted_files

#===============================================================    
# uncomment the below lines if we want to use it for production
# then instead of flask run use python app.py in command line to start wsgi server
#===============================================================

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000)
