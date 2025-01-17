from garmin_initialisation import garmin_initilise
import pandas as pd
from datetime import datetime, timedelta

class DataPull():

    def __init__(self):
        self.garmin = garmin_initilise()
        self.DATE_1 = datetime.strptime("2024-09-10", "%Y-%m-%d")
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
    
    def test(self):
        
        print(self.dates)

    
# beans = DataPull()
# beans.test()
