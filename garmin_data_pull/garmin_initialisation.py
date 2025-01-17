import garminconnect

from getpass import getpass
import os

def garmin_initilise():
    email = os.getenv("GARMIN_EMAIL")
    password = os.getenv("GARMIN_PASSWORD")

    garmin = garminconnect.Garmin(email, password)
    garmin.login()

    GARTH_HOME = os.getenv("GARTH_HOME", "~/.garth")
    garmin.garth.dump(GARTH_HOME)

    return garmin