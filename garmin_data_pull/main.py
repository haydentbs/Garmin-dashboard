from data_pull import DataPull
from database_insert import DatabaseHandler
import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv() 

def main():

#     db_config = {
#     'user': os.getenv('DB_USER'),
#     'password': os.getenv('DB_PASSWORD'),
#     'host': os.getenv('DB_HOST'),
#     'port': os.getenv('DB_PORT'),
#     'database': os.getenv('DB_NAME')
# }
    db_config = {
    'user': 'postgres',
    'password': 'garmin',
    'host': 'db',  # This matches the service name in docker-compose
    'port': '5432',
    'database': 'garmin'
    }
    
    if os.path.exists('steps.csv'):
        print('Valid csv path')
        data = {}
        data['daily_steps'] = pd.read_csv('steps.csv')
       
    else:
        Data = DataPull()
        Data.daily_steps() 
        data = Data.data
    # Data.daily_steps()
    # print(Data.data['daily_steps'])
    # print(data['daily_steps'].keys())

    Database = DatabaseHandler(db_config['database'], data, inside_container=True)
    # Database.test()
    Database.insert_data()

main()