from google.cloud import storage
from google.oauth2 import service_account
import os
import psycopg2
import time
import pandas as pd
from io import StringIO
import ast

def download_blob_into_memory(bucket_name,prefix,localdb_table_name):
    """Downloads a blob into memory."""

    storage_client = storage.Client(credentials=credentials)
    bucket = storage_client.bucket(bucket_name)
    blobs = bucket.list_blobs(prefix=prefix)
    sum_data = str()
    start_index=0
    blob_name = []
    
    # print(blobs)
    # collect blob file names
    for blob in blobs:
        print(blob)
        blob_name_str = str(blob.name)
        blob_name.append(blob_name_str)
    # blob_name_str[blob_name_str.find('/')+1:])
    print(blob_name)
    # Insert only 3 months ago
    # for i in range(len(blob_name)-3,len(blob_name)):
    blobs = bucket.list_blobs(prefix=prefix)
    for blob in blobs:
        # if str(blob.name) in blob_name[len(blob_name)-3:]:
        if str(blob.name) in blob_name:
            print(blob.name)
            data = blob.download_as_string()
            data_decode = data.decode()
            if start_index == 0:
                start_index = data_decode.find('\n')
            if sum_data == '':
                sum_data = data_decode[start_index:]
            else: 
                sum_data = sum_data.strip('\n') + data_decode[start_index:]
        print(sum_data)
    print(blob_name)
    print(sum_data[:].strip('\n'))
    sum_data_file = StringIO(sum_data.strip('\n'))
    with conn, conn.cursor() as cursor:
        conn.cursor().copy_from(sum_data_file, localdb_table_name, sep='\t')

# start here

t0 = time.time()

#create credentials variable to access cloud storage
credentials = service_account.Credentials.from_service_account_file(
    filename=os.environ['GOOGLE_APPLICATION_CREDENTIALS'],
    scopes=['https://www.googleapis.com/auth/cloud-platform'])

#connection variable
conn = psycopg2.connect(
        host=os.environ['localhost'],
        user=os.environ['user'],
        password=os.environ['password'],
        dbname=os.environ['dbname'],
        port=int(os.environ['port'])
    )

#delete four months before today
with conn, conn.cursor() as cursor:
    # cursor.execute('''DELETE FROM test_production where cast(concat(year, '-',monthno, '-','1') as DATE) >=(current_date - interval '8 months')and cast(concat(year, '-',monthno, '-','1') as DATE) <=(current_date)''')
#     cursor.execute('''select case 
# 	when cast(monthno as integer) <10 then cast(concat(year,'0',monthno) as text) 
# 	when cast(monthno as integer) >=10 then cast(concat(year,'',monthno) as text)
# 	end as date
# from test_production''')
    cursor.execute('''DELETE FROM test_production''')
    cursor.execute('''DELETE FROM test_importproduct''')
    cursor.execute('''DELETE FROM test_industry''')
    cursor.execute('''DELETE FROM test_ingredient''')


for project in ast.literal_eval(os.environ['projects_list']):
    print(project[0])
    print(project[1])
    download_blob_into_memory(os.environ['bucket_name'],project[0],project[1])

print("Import successfully")

t1 = time.time()
total = t1-t0
# print excution time
print(f'The execution time is {total} second')

