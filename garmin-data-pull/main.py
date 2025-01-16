from data_pull import DataPull
from database_insert import DatabaseHandler
import os
import pandas as pd

def main():

    config = {
        'database': {
            'user': 'postgres',
            'password': 'garmin',
            'host': 'db',
            'port': '5432',
            'database': 'garmin'
        }
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
    print(data['daily_steps'].keys())

    Database = DatabaseHandler(config['database'], data, inside_container=False)
    # Database.test()
    Database.insert_data()

main()