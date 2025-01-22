# Created by Terezia Jurasova

# Importing libraries for the prayer times and the date as well as for modifying the sound
import datetime
import time
import praytimes
import subprocess

# Abu Dhabi coordinates and timezone:
latitude = 24.466667
longitude = 54.366669
timezone = 4

# Setting the date as the current date
date = datetime.date.today()

# Retrieving the prayer times 
pt = praytimes.PrayTimes()

# Abu Dhabi Prayer times for the given date:
prayer_times = pt.getTimes(date, (latitude, longitude), timezone)

# Removing non prayer values from the library’s prayer times:
items_to_remove = ['imsak','sunrise','sunset','midnight']
for key in items_to_remove:
    prayer_times.pop(key, None)

# The five prayer times:
prayer_times = prayer_times.values()  

# Condition to mute the volume for five minutes during prayer times
while True:
    current_time = datetime.datetime.now().strftime("%H:%M")
    if current_time in prayer_times:
        subprocess.run(["amixer", "-D", "pulse", "sset", "Master", "mute"])
        time.sleep(300) # Sleep for 5 minutes
        subprocess.run(["amixer", "-D", "pulse", "sset", "Master", "unmute"])
        time.sleep(60) # Check the time for every minute
