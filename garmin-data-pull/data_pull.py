from garmin_initialisation import garmin_initilise
import pandas as pd

class DataPull():

    def __init__(self):
        self.garmin = garmin_initilise()
        self.DATE_1 = "2024-12-29"
        self.DATE_2 = "2025-01-14"

        self.data = {}

        self.DAILY_STEPS = False
    
    def daily_steps(self):

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
