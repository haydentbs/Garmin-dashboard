from garmin_initialisation import garmin_initilise
import pandas as pd
from datetime import datetime, timedelta

class DataPull():

    def __init__(self):
        self.garmin = garmin_initilise()
        self.DATE_1 = datetime.strptime("2024-01-16", "%Y-%m-%d")
        self.DATE_2 = datetime.strptime("2025-01-16", "%Y-%m-%d")
        self.dates = self.split_dates()

        self.data = {}

        self.DAILY_STEPS = False


    def split_dates(self):
        delta = self.DATE_2 - self.DATE_1
        print(f"Number of days: {delta.days}")

        delta = self.DATE_2 - self.DATE_1
        dates = []
        if delta.days > 27:
            dates.append(self.DATE_2)

            date_temp = self.DATE_2

            while date_temp - timedelta(days=27) > self.DATE_1:
                date_temp = date_temp - timedelta(days=27)
                dates.append(date_temp)

            dates.append(self.DATE_1)

        else:
            dates = [self.DATE_2, self.DATE_1]

        return dates

    
    def daily_steps(self):

        if len(self.dates) > 2:
            temp_data = pd.DataFrame(self.garmin.get_daily_steps(self.dates[1], self.dates[0]))
            for i in range(len(self.dates)-2):
                new_data = pd.DataFrame(self.garmin.get_daily_steps(self.dates[i+2], self.dates[i+1]-timedelta(days=1)))
                temp_data = pd.concat([temp_data, new_data], ignore_index=True)
            self.data['daily_steps'] = temp_data
        else:
            self.data['daily_steps'] = pd.DataFrame(self.garmin.get_daily_steps(self.DATE_1, self.DATE_2))

        self.DAILY_STEPS = True

        self.data['daily_steps'] = self.data['daily_steps'].rename(columns={
            'calendarDate': 'date',
            'totalSteps': 'total_steps',
            'totalDistance': 'distance',
            'stepGoal': 'step_goal'
        })

        columns = ['date', 'total_steps', 'distance', 'step_goal']

        self.data['daily_steps'] = self.data['daily_steps'][columns]

        self.data['daily_steps'].to_csv('steps.csv',index=False)

        return self.data['daily_steps']
    
    def activity_list(self):

        def extract_type_key(activity_dict):
            # Handle string dictionaries
            if isinstance(activity_dict, str):
                activity_dict = eval(activity_dict)
            # Extract typeKey
            return activity_dict['typeKey']
        
        if len(self.dates) > 2:
            temp_data = pd.DataFrame(self.garmin.get_activities_by_date(self.dates[1], self.dates[0]))
            for i in range(len(self.dates)-2):
                new_data = pd.DataFrame(self.garmin.get_activities_by_date(self.dates[i+2], self.dates[i+1]-timedelta(days=1)))
                temp_data = pd.concat([temp_data, new_data], ignore_index=True)
            self.data['activity_list'] = temp_data
        else:
            self.data['activity_list'] = pd.DataFrame(self.garmin.get_activities_by_date(self.DATE_1, self.DATE_2))
        
        self.ACTVITIES_LIST = True

        self.data['activity_list']['activityTypeName'] = self.data['activity_list']['activityType'].apply(extract_type_key)
        def is_dict_or_dict_string(x):
            if isinstance(x, dict):
                return True
            if isinstance(x, str):
                try:
                    eval(x)
                    return True
                except:
                    return False
            return False

        dict_cols = self.data['activity_list'].map(is_dict_or_dict_string).any()
        dict_column_names = dict_cols[dict_cols].index
        print(dict_column_names)
        print(self.data['activity_list'].columns)
        self.data['activity_list'].drop(columns=dict_column_names, inplace=True)
        print(self.data['activity_list'].columns)
        self.data['activity_list']['date'] = pd.to_datetime(self.data['activity_list']['startTimeLocal']).dt.date


        self.data['activity_list'].to_csv('activity_list.csv')

        return self.data['activity_list']
    

    def get_user_details(self):

        return None

    

    
    def test(self):
        
        # df = pd.read_csv('activity.csv')
        # def is_dict_or_dict_string(x):
        #     if isinstance(x, dict):
        #         return True
        #     if isinstance(x, str):
        #         try:
        #             eval(x)
        #             return True
        #         except:
        #             return False
        #     return False

        # dict_cols = df.map(is_dict_or_dict_string).any()
        # dict_column_names = dict_cols[dict_cols].index

        # print("Columns containing dictionaries:", dict_column_names.tolist())
        # print(df.columns)
        # df.drop(columns=dict_column_names, inplace=True)
        # print(df.columns)
     return None


    
# beans = DataPull()
# beans.test()
