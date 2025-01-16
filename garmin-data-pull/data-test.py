import garminconnect

from getpass import getpass
import os

email = os.getenv("GARMIN_EMAIL")
password = os.getenv("GARMIN_PASSWORD")

garmin = garminconnect.Garmin(email, password)
garmin.login()

print('Display Name: ', garmin.display_name)

import os

GARTH_HOME = os.getenv("GARTH_HOME", "~/.garth")
garmin.garth.dump(GARTH_HOME)

from datetime import date, timedelta

yesterday = date.today() - timedelta(days=4)
yesterday = yesterday.isoformat()
yesterday

print(garmin.get_steps_data(yesterday)[:2])