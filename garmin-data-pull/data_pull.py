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

        return self.data['daily_steps']
