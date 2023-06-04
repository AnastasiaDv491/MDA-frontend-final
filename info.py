import numpy as np
import pandas as pd
import datetime

def get_event_info(number, events_df):
    if len(events_df) < number + 1:
        name = "No event"
        time = " "
        adress = " "
        respondent = " "
    else:
        name = events_df['Event_name'].iloc[number]
        name = name.rsplit(" ")
        if len(name) > 2: 
             name = name[0] + " " + name[1] + " ..."
        elif len(name) == 2:
            name = name[0] + " " + name[1]
        elif len(name) == 1:
            name = name[0]
        
        adress = events_df['Address'].iloc[number]
        respondent = int(events_df['Respondents'].iloc[number])
        respondent = str(respondent) + " Respondents"
         time = pd.to_datetime(events_df['Time'].iloc[number])
        time = time.strftime('%H:%M')
      
    result = { "name" : name,
        "time" : time,
        "adress" : adress,
        "respondent" : respondent}
    return(result)

def get_weather_info(weather_df):
    dwtemp = weather_df["LC_DWPTEMP"]
    RH = weather_df["LC_HUMIDITY"]
    temp = dwtemp + (100-RH)/5     #from dewpoint temperature to temperature
    temp = np.round(np.mean(temp),2)
    temp = "Average temperature " + str(temp) + " °C"

    wind = np.mean(weather_df["LC_WINDSPEED"])
    wind = np.round(3.6*wind, 2)                        #from m/s to km/h
    wind = "Average windspeed " + str(wind) + " km/h"

    result = {"temp": temp,
    "wind":wind}

    return(result)
