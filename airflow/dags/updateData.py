import boto3
import csv
import os
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
#from great_expectations_provider.operators.great_expectations import GreatExpectationsOperator
#from great_expectations.core.batch import BatchRequest
#from great_expectations.data_context.types.base import (
#    DataContextConfig,
#    CheckpointConfig
#)

goes_bucket = "noaa-goes18"
nexrad_bucket = "noaa-nexrad-level2"
des_bucket = "damg7245-ass1"

# Define DAG arguments
default_args = {
    'owner': 'Harsh Shah',
    'depends_on_past': False,
    'start_date': datetime(2023, 3, 1)
}
aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')

#aws_access_key_id="AKIAWFZMBX3F2BMPDVXS",aws_secret_access_key="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"


s3 = boto3.client('s3',region_name = 'us-east-1',aws_access_key_id = aws_access_key_id,aws_secret_access_key = aws_secret_access_key)


# Define scraper function
def GOES_scrap_load():
    goes18_dict = {
        'id': [],
        'product': [],
        'year': [],
        'day': [],
        'hour': []
    }
    prefix = 'ABI-L1b-RadC/'
    delimiter = '/'

    id=1
    result = s3.list_objects(Bucket=goes_bucket,
                            Prefix= 'ABI-L1b-RadC/', Delimiter='/')
    for o in result.get('CommonPrefixes'):
        path = o.get('Prefix').split('/')
        prefix_new = prefix + path[-2] + "/"
        sub_folder = s3.list_objects(
            Bucket=goes_bucket, Prefix=prefix_new, Delimiter=delimiter)
        if sub_folder is not None:  # Check if sub_folder is not None
            for p in sub_folder.get('CommonPrefixes'):
                sub_path = p.get('Prefix').split('/')
                prefix_new2 = prefix_new + sub_path[-2] + "/"
                sub_sub_folder = s3.list_objects(
                    Bucket=goes_bucket, Prefix=prefix_new2, Delimiter=delimiter)
                if sub_sub_folder is not None:
                    for q in sub_sub_folder.get('CommonPrefixes'):
                        sub_sub_path = q.get('Prefix').split('/')
                        sub_sub_path = sub_sub_path[:-1]
                        goes18_dict['id'].append(id)
                        goes18_dict['product'].append(sub_sub_path[0])
                        goes18_dict['year'].append(sub_sub_path[1])
                        goes18_dict['day'].append(sub_sub_path[2])
                        goes18_dict['hour'].append(sub_sub_path[3])
                        id+=1

    df = pd.DataFrame(goes18_dict)

    # Connect to SQLite3 database
    conn = sqlite3.connect('meta_data.db')
    c = conn.cursor()

    # Create table for metadata
    c.execute('''CREATE TABLE IF NOT EXISTS GEOS
                (id integer, product integer, year integer, day integer, hour integer)''')


    # insert the DataFrame into a new table named 'metadata_goes18'
    df.to_sql('GEOS', conn, if_exists='replace', index=False)

    # Commit changes and close database connection
    conn.commit()
    conn.close()


# Define scraper function
def NEXRAD_scrap_load():
    NEXRAD_dict = {
        'id': [],
        'year': [],
        'month': [],
        'day': [],
        'station':[]
    }
    years = ['2022','2023']
    id=1
    delimiter = '/'

    for y in years:
        prefix= y+'/'
        result = s3.list_objects(Bucket=nexrad_bucket,
                                Prefix=prefix, Delimiter='/')

        for o in result.get('CommonPrefixes'):
            path = o.get('Prefix').split('/')
            prefix_new = prefix + path[-2] + "/"
            sub_folder = s3.list_objects(
                Bucket=nexrad_bucket, Prefix=prefix_new, Delimiter='/')
            if sub_folder is not None:  # Check if sub_folder is not None
                for p in sub_folder.get('CommonPrefixes'):
                    sub_path = p.get('Prefix').split('/')
                    prefix_new2 = prefix_new + sub_path[-2] + "/"
                    sub_sub_folder = s3.list_objects(
                        Bucket=nexrad_bucket, Prefix=prefix_new2, Delimiter='/')
                    if sub_sub_folder is not None:
                        for q in sub_sub_folder.get('CommonPrefixes'):
                            sub_sub_path = q.get('Prefix').split('/')
                            sub_sub_path = sub_sub_path[:-1]
                            NEXRAD_dict['id'].append(id)
                            NEXRAD_dict['year'].append(sub_sub_path[0])
                            NEXRAD_dict['month'].append(sub_sub_path[1])
                            NEXRAD_dict['day'].append(sub_sub_path[2])
                            NEXRAD_dict['station'].append(sub_sub_path[3])
                            id+=1

    df = pd.DataFrame(NEXRAD_dict)

    # Connect to SQLite3 database
    conn = sqlite3.connect('meta_data.db')
    c = conn.cursor()

    # Create table for metadata
    c.execute('''CREATE TABLE IF NOT EXISTS Nexrad
                (id integer, year integer, month integer, day integer, station text)''')

    # insert the DataFrame into a new table named 'nexrad'
    df.to_sql('Nexrad', conn, if_exists='replace', index=False)

    # Commit changes and close database connection
    conn.commit()
    conn.close()



def database_to_csv():

    conn = sqlite3.connect('example.db')

    cur = conn.cursor()
    cur.execute("SELECT * FROM GEOS")
    rows = cur.fetchall()

    goes_csv_file = 'goes18.csv'
    with open(goes_csv_file, 'w', newline='') as file:

        # Create a CSV writer object
        writer = csv.writer(file)
        writer.writerow([i[0] for i in cur.description])
        for row in rows:
            writer.writerow(row)
    
    cur.execute("SELECT * FROM Nexrad")
    rows = cur.fetchall()

    nexrad_csv_file = 'nexrad.csv'
    with open(nexrad_csv_file, 'w', newline='') as file:

        # Create a CSV writer object
        writer = csv.writer(file)
        writer.writerow([i[0] for i in cur.description])
        for row in rows:
            writer.writerow(row)
    

    conn.close()









# Define DAG
scrapper_dag = DAG(
    'metadata_scraper',
    default_args=default_args,
    description='Scrape data from an S3 bucket and upload database',
    schedule_interval='0 0 * * *'
)
# Define DAG tasks
scrape_task1 = PythonOperator(
    task_id='scrape_goes_data',
    python_callable=GOES_scrap_load,
    dag=scrapper_dag
)

scrape_task2 = PythonOperator(
    task_id='scrape_nexrad_data',
    python_callable=NEXRAD_scrap_load,
    dag=scrapper_dag
)

db2csv_dag = DAG(
    'database_to_csv',
    default_args=default_args,
    description='export database file to csv',
    schedule_interval=None
)

db2csv_task = PythonOperator(
    task_id='export_to_csv',
    python_callable=database_to_csv,
    dag=db2csv_dag
)
scrape_task1 >> scrape_task2 

## GREAT EXPECTATIONS USING AIRFLOW -
""""
great_expectations_dag = DAG(
    'my_great_expectations_dag', 
    default_args=default_args, 
    schedule_interval=timedelta(days=1)
    )
#ge_root_dir=os.path.join(os.path.dirname(__file__),"..","great-expectation/great-expectation")
ge_task1 = GreatExpectationsOperator(
    task_id="goes18_run_data_validation",
    data_context_root_dir=ge_root_dir,
    checkpoint_name="goes18_check_point.yml",
    dag=great_expectations_dag
)
ge_task2 = GreatExpectationsOperator(
    task_id="nexrad_run_data_validation",
    data_context_root_dir=ge_root_dir,
    checkpoint_name="nexrad_checkpoint.yml",
    dag=great_expectations_dag
)
ge_task3 = GreatExpectationsOperator(
    task_id="great_expectations_config",
    data_context_config="great_expectations.yml",
    checkpoint_config="goes18_check_point.yml",
    dag=great_expectations_dag
)
ge_task4 = GreatExpectationsOperator(
    task_id="great_expectations_config",
    data_context_config="great_expectations.yml",
    checkpoint_config="nexrad_checkpoint.yml",
    dag=great_expectations_dag
)
ge_task1 >> ge_task2 >> ge_task3 >> ge_task4
"""