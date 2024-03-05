# AlgaeStat
Python tools for Algae Cultivation Data

## Supported Instrumentation
YSI, Burge Environmental MiProbe, Hobolink Weather Station, Custom CSV's

# Installation
- Install with pip.
```shell
# path if algaestat was cloned to ~/GitHub directory.
gh repo clone davidpipelines/algaestat
cd ~/GitHub/
pip install ./algaestat

```
# Directions:
## Downloading Data
1. First Initialize the database with your credentials.
### Example WS credential file named aws_cred.json
```json
{
	"region_name": "location i.e us-east-1",
	"aws_access_key_id": "accesskey from AWS Administrator",
	"aws_secret_access_key": "Secret key from you AWS Administrator"
}
```
### Code to initialize your database class
```python

import algaestat
import os
# path to your cred file
cred_dir = '~/cred'
cred_filepath = os.path.join(cred_dir,'aws_cred.json')
q = algaestat.QueryDB(cred_filepath=cred_filepath)
```
2. Add a query to download the data over date ranges and export to csv (as needed)
```python 

import algaestat
import os
import pandas as pd

# path to your cred file
cred_dir = '~/cred'
cred_filepath = os.path.join(cred_dir,'aws_cred.json')
q = algaestat.QueryDB(cred_filepath=cred_filepath)
# pull data from January 17, 2024 from pond 9
# Dates should be in form 'YYYY-MM-DD HH:MM:SS'
start_date = '2024-01-17 00:00:01'
end_date = '2024-01-18 00:00:01'
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
```