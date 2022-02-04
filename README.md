# NOAA-Weather-Requests

This is a GUI program written in Python 3 that can be used to send a web API request to 
NOAA Climate Data Online Web Database and displays data in a display window. 

To make a web request user needs to select a day range and enter a weather station ID number.
Acceptable date format is YYYY-MM-DD. Station number is send as e.g. GHCND:USW00014768 for
Rochester, NY. Station numbers can also be selected from a drop-down menu that automatically 
find associated station ID numbers.

If data for selected date range and stations are not available, then an error message is displayed.

To start the program execute python noaa_weather.py on command line.

NOAA_TOKEN.txt file must be placed in the same directory for the program to work.
