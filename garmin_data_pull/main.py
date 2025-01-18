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
    Data = DataPull()

    if os.path.exists('steps.csv'):
        print('Valid steps csv path')
        Data.data['daily_steps'] = pd.read_csv('steps.csv')
    else:
        Data.daily_steps() 

    if os.path.exists('activity_list.csv'):
        print('Valid activity csv path')
        Data.data['activity_list'] = pd.read_csv('activity_list.csv')
    else:
        Data.activity_list()     
    # else:
    
    
    
    
    data = Data.data
    # Data.daily_steps()
    # print(Data.data['daily_steps'])
    # print(data['daily_steps'].keys())

    Database = DatabaseHandler(db_config, data, inside_container=True)
    # Database.test()
    Database.insert_data()

main()