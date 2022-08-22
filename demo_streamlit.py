


# import the streamlit library
import streamlit as st
import csv
import os
import pandas as pd
import json as json
from datetime import date

current_date = date.today()

#Read CSV File
def read_CSV(file, json_file):
    csv_rows = []
    INSERtstmt_Original = ''
    RtnINSERtstmt = ''
    with open(file, encoding="utf8") as csvfile:
        reader = csv.DictReader(csvfile)
        field = reader.fieldnames
        for row in reader:
            csv_rows.extend([{field[i]:row[field[i]] for i in range(len(field))}])
        convert_write_json(csv_rows, json_file)
        RtnINSERtstmt = Generate_insert_script(json_file)
        INSERtstmt_Original=INSERtstmt_Original + " \n "+RtnINSERtstmt
    jf = r'E:\mig_{}.sql'.format(json_file)
    f= open( jf,"w+",encoding="utf8")
    f.write(INSERtstmt_Original)
    f.close()


    
#Convert csv data into json
def convert_write_json(data, json_file):
    with open(json_file, "w" ,encoding="utf8") as f:
        f.write(json.dumps(data, sort_keys=False, indent=4, separators=(',', ': '))) #for pretty


#Convent Json to MySQL
def Generate_insert_script(json_file):
    TABLE_NAME = "`mig_{}`".format(json_file)

    sqlstatement = ''
    
    INSERtstmt = ''
    with open (json_file,'r') as f:
        jsondata = json.loads(f.read().replace("'",''))
        
    for jsonval in jsondata:
        keylist = "("
        valuelist = "("
        firstPair = True
        for key, value in jsonval.items():
            if not firstPair:
                keylist += ", "
                valuelist += ", "
            firstPair = False


            if  isinstance(value, str):
                valuelist += "'" + value + "'"
                decoded = False
            if  isinstance(key, str):
                keylist += "`" + key + "`"
                decoded = False
            else:
                valuelist += unicode_or_str.decode(value)
                decoded = True
                keylist += unicode_or_str.decode(key)
                decoded = True
                
        keylist += ")"
        valuelist += ")"
        sqlstatement +=  valuelist + ",\n"
    sqlstatement = sqlstatement[:-1]
    
    INSERtstmt= "INSERT INTO " + TABLE_NAME + " " + keylist + " VALUES "+'\n' +sqlstatement[:-1] +';'
    return INSERtstmt

	
uploaded_files = st.file_uploader("Choose a XLSX file", accept_multiple_files=True)
for uploaded_file in uploaded_files:
	bytes_data = uploaded_file.read()
	st.write("filename:", uploaded_file.name)
	
	
	df = pd.DataFrame()
	#xlfname = r"E:\Loadsheet\Flora Express_Loadsheet_v1.7.xlsx"
	xl = pd.ExcelFile(bytes_data)
	for sheet in xl.sheet_names:
		df_tmp = xl.parse(sheet)
		#print(sheet)
		csvfile = sheet+'.csv'
		json_file = sheet
		
		#print(csvfile)
		df_tmp = df.append(df_tmp, ignore_index=True)
		df_tmp.to_csv(csvfile, index=False)
		read_CSV(csvfile,json_file)

    
if os.path.exists(r'E:\Loadsheet\Insert Script\mig_Parameter.sql'):
    os.remove(r'E:\Loadsheet\Insert Script\mig_Parameter.sql')
	
	
 #------------------------------ db ------------------------------#

st.snow()
