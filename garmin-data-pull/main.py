from data_pull import DataPull
from database_insert import DatabaseHandler

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
    Data = DataPull()
    # Data.daily_steps()
    # print(Data.data['daily_steps'])

    Database = DatabaseHandler(config['database'], Data.data, inside_container=False)
    Database.test()

main()