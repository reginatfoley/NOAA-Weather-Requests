#!/usr/bin/env python
# coding: utf-8

# #GUI program that can give a weather report for a given area on a specified day range

import requests
import time
from datetime import date, timedelta
import pandas as pd  
import tkinter as tk
from tkinter.ttk import *
from tkinter import scrolledtext
from tkinter.ttk import Combobox

NOAA_BASE_URL = "https://www.ncdc.noaa.gov/cdo-web/api/v2"

STATIONS = {'Eldora' : 'GHCND:USS0005J41S', 'Boulder' : 'GHCND:USC00050848', 'Copper Mountain' : 'GHCND:USS0006K24S',
             'Winter Park': 'GHCND:USC00059175', 'Steamboat Springs' : 'GHCND:USC00057936', 'Aspen' : 'GHCND:USW00093073',
             'Rochester' : "GHCND:USW00014768"}

TODAY = str(date.today())
WEEKAGO = str(date.today() - timedelta(days = 7))

#Open NOAA token
def NOAA_TOKEN():
    with open("NOAA_TOKEN.txt") as f:
        txt = f.read()
    return txt.strip()

# Send Web API
def send_request(STATION_ID, STARTDATE = TODAY, ENDDATE = TODAY):
    Mountain_GHCND_URL = NOAA_BASE_URL + "/data?datasetid=GHCND&stationid=" + STATION_ID + "&units=metric&startdate=" + STARTDATE + "&enddate=" + ENDDATE
    response = requests.get(Mountain_GHCND_URL, headers={"token":NOAA_TOKEN()})
    response_json = response.json()    
    
    # check if data is actually something useful (not empty)
    if not response_json:
        output = "Data for those days are not available."
        return output
    
    else:
        values = []
        for data in response_json['results']:
            #record = data['date'].split('T')[0], data['datatype'], data['value']
            record = {"Date": data['date'].split('T')[0], "Datatype": data['datatype'], "Value": data['value']}
            values.append(record)

        #Organize values:
        df = pd.DataFrame(values)
        #I tried formating the output, but the returned results are so crazy inconsistent that I gave up.
        
        return df
        
# Functions to handle keypress.
def handle_keypress(event):
    start_day = entry_start.get()
    end_day = entry_end.get()
    
    stations_entered = entry_stations.get()
    
    if stations_entered:
        station_IDS = stations_entered
        station_name = station_IDS
        
    elif stations.get():
        entry_stations.delete(0, tk.END) # Clear and reset station number field
        station_name = stations.get()
        station_IDS =  STATIONS[station_name]
        entry_stations.insert(0, station_IDS)
        
    else:
        results_box.insert(tk.END, "Select or enter weather station.")
    
    results = send_request(station_IDS, start_day, end_day)
    results_box.insert(tk.END, str(f"{station_name} : {results}\n"))
    entry_stations.delete(0, tk.END) # Clear and reset station number field
        
def clear_output(event):
    results_box.delete('1.0', tk.END) # Delete from position 0 till end
    entry_stations.delete('1.0', tk.END) # Clear and reset station number field
    
################################################################### 
# GUI:    
window = tk.Tk()
window.title("Daily weather summary.")
frame = tk.Frame(master=window, relief=tk.GROOVE, borderwidth=5)

label = tk.Label(master=window, text="Please enter a date range and select weather station number.", 
                 font=("Ariel", 20), fg="black", bg="#34A2FE", width=50, 
                 height=4, relief=tk.GROOVE).pack(fill=tk.X)

label_start = tk.Label(master=window, text="Start Day", font=("Arial", 14), 
                       width=50, height=2)
entry_start = tk.Entry(master=window, fg="black", bg="white", width=50)
label_end = tk.Label(master=window, text="End Day", font=("Arial", 14), 
                     width=50, height=2)
entry_end = tk.Entry(master=window, fg="black", bg="white", width=50)
label_stations = tk.Label(master=window, text="Weather Station Number(s)", 
                          font=("Arial", 14), width=50, height=2)
entry_stations = tk.Entry(master=window, fg="black", bg="white", width=50)
stations = Combobox(window, width=50)
#stations = Listbox(window, height=5, selectmode='multiple')
stations['values']= ['Select Station or enter station ID below', 'Rochester', 'Eldora', 'Aspen', 'Steamboat Springs', 'Winter Park', 
                     'Boulder', 'Copper Mountain']
stations.current(0)
results_box = scrolledtext.ScrolledText(window,width=40,height=10)

# Buttons:
button_send = tk.Button(master=window, text="Send Request", width=15, height=3,
              relief = tk.RAISED) #, command=handle_keypress
button_clear = tk.Button(master=window, text="Clear All", width=15, height=3)
button_send.bind("<Button-1>", handle_keypress)
button_clear.bind("<Button-1>", clear_output)

# Inserting default values:
entry_start.insert(0, WEEKAGO)
entry_end.insert(0, TODAY)
#entry_stations.insert(0, "GHCND:USW00014768")

entry_start.pack(fill=tk.X)
label_end.pack()
entry_end.pack(fill=tk.X)
label_stations.pack()
stations.pack()
entry_stations.pack(fill=tk.X)
results_box.pack(fill=tk.BOTH)
button_send.pack()
results_box.pack()
button_clear.pack()
#label_start.focus()

window.mainloop()



