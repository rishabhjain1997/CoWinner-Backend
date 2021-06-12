import os
import glob
from datetime import datetime, timedelta
from dateutil import tz
import sys


def yesterday_date(day_delta=1):
    """Function to fetch Indian format of the date of the current day in which job is running(IST timezone)"""
    india_tz = tz.gettz("Asia/Kolkata")
    now = datetime.now(tz=india_tz)
    today = str(now.date() - timedelta(days=day_delta))

    year, month, day = today.split('-')
    t1 = (day, month, year)
    indian_date = "-".join(t1)
    return indian_date


def remove_data(day_delta=1):
    yesterday = yesterday_date(day_delta)
    file_list = glob.glob(f'data/*{yesterday}.json')
    for file_path in file_list:
        try:
            os.remove(file_path)
        except OSError:
            print("Error while deleting file")


try:
    day_difference: int = int(sys.argv[1])
except IndexError:
    day_difference = 1

remove_data(day_difference)
