import algaestat
import os
import pandas as pd

# path to your cred file
cred_dir = '~/cred'
cred_filepath = os.path.join(cred_dir, 'aws_cred.json')
q = algaestat.QueryDB(cred_filepath=cred_filepath)
# pull data from January 17, 2024 from pond 9
start_date = f'2024-01-17 00:00:01'
end_date = f'2024-01-18 00:00:01'
# our pond names are SPW{pondnumber)
pond_name = 'SPW9'
# this is the table where the downsampled data resides
table_name = 'miprobe_ds'
df_miprobe = q.query_table_range(start=start_date,
                                 end=end_date,
                                 **algaestat.get_tableinfo(table_name=table_name,
                                                           identifier_name=pond_name,
                                                           q=q))
print('converting timestamp')
# convert the timestamp column as needed
df_miprobe['Timestamp'] = pd.to_datetime(df_miprobe['Timestamp'])
# print data table result if needed
print(df_miprobe)
# export to csv if needed
df_miprobe.to_csv('~/SPW9_2024_01_17_ds.csv', index=False)

