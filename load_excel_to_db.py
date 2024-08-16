from pg_functions import excel_to_table
file_path = 'bsr.xlsx'
sheet_name = 'BSR Data'  
schema = 'analysis'
table_name = 'bsr_data' 
excel_to_table(file_path,sheet_name,schema,table_name)