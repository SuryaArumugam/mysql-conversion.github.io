import os
import pandas as pd
import streamlit as st


def sql_file(data,sheet,create_path):
    table_name = '`{}`'.format(sheet)
  
    column_name = ''
    for col in data.columns:
        column_name += "`{}`,".format(col)
    column_name = column_name[:-1]
    column_values = "({})".format(column_name)


    row_name = "("+''
    for ro in data.values:
        strng = str(ro)
        s = "("
        
        for j in ro:  
            row_name +="'{}',".format(str(j))

        row_name = row_name[:-1]
        e = "),"
        row_name = row_name.replace('NULL','NULL') 
        row_name += e+'\n'
        row_name += s
    
    sql_script = 'INSERT INTO'+' '+table_name+' '+column_values+' '+'values\n'+''+row_name[:-3] +';'

        
    jf = r'{}\{}.sql'.format(create_path,sheet)
    f= open( jf,"w+",encoding="utf8")
    f.write(sql_script.getbuffer)
    #st.success(json_file+' '+'Script Successfully created')
    f.close()

 

uploaded_files = st.file_uploader("Choose a XLSX file", accept_multiple_files=True)
for uploaded_file in uploaded_files:
	bytes_data = uploaded_file.read()
	xl_name = uploaded_file.name.split('.')[0]
	st.write("filename:", xl_name) 


	df = pd.DataFrame()
	parent_dir = "D:/"
	path = os.path.join(parent_dir, xl_name)
	create_path = os.mkdir(path)

	xl = pd.ExcelFile(bytes_data)
	for sheet in xl.sheet_names:
		df_tmp = xl.parse(sheet)
		sql_file(df_tmp,sheet,create_path)
