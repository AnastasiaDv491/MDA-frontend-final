from dash import html, register_page 
import pandas as pd
from io import StringIO
import numpy as np
import datetime
from dataload_AWS import AWS_instantiate
from info import get_event_info, get_weather_info

register_page(
    __name__,
    name='Tonight',
    top_nav=True,
    path='/tonight'
)
today = datetime.datetime(2022, 10, 17)

d1 = datetime.datetime(2022, 1, 31)
d2 =  datetime.datetime(2022, 2, 14)
d3 = datetime.datetime(2022, 3, 31)
d4 = datetime.datetime(2022, 4, 19)
d5 = datetime.datetime(2022, 5, 28)
d6 = datetime.datetime(2022, 6, 1)
d7 = datetime.datetime(2022, 8 , 15)
d8 = datetime.datetime(2022, 9, 5)
d9 = datetime.datetime(2022, 12, 23)

if today <= d1 or d5 < today < d6 :
    season = "Season: Exams "
elif d1 < today < d2 or d3 < today <= d4 or d6 <= today < d7 or today >= d9 :
    season = "Season: Holiday"
elif d2 <= today <= d3 or d4 < today <= d5 or d8 <= today < d9:
    season = "Season: Party"
elif d7 <= today <= d8:
    season = "Season: Retakes"

today_title = str(today.date())
today_title = today_title.rsplit("-")
today_title = today_title[2] + "/" + today_title[1] + "/" + today_title[0]

objects_AWS = AWS_instantiate.createAWSconnection() # Contains all objects from S3 bucket

for file in objects_AWS:
    if file.key == "events_distances.csv":
        csv_file =file.get()['Body'].read().decode('utf-8')
        events_df= pd.read_csv(StringIO(csv_file))
        events_df['Date'] = pd.to_datetime(events_df['Date'], errors='coerce')
        events_df = events_df[events_df["Date"] ==today.strftime("%d/%m/%Y")].sort_values(by= "Respondents", ascending=True)

        events_df.Respondents = events_df.Respondents.replace("na", np.nan).fillna(0)
        events_df.Respondents = events_df.Respondents.astype(float)
                
    elif file.key == "weather_data.csv":
        csv_file =file.get()['Body'].read().decode('utf-8')
        weather_df= pd.read_csv(StringIO(csv_file))
        weather_df['DATEUTC'] = pd.to_datetime(weather_df['DATEUTC'], errors='coerce')
        weather_df = weather_df[weather_df['DATEUTC'] ==today.strftime("%d/%m/%Y")]
        
def layout():
    layout = html.Div(children = [
        
        html.H2(children="Tonight in Leuven",
        className = 'graph_header'),

        html.P(children = today_title, className = 'graph_subheader'),
        
        html.Div([
            html.Div([ 
                html.Div([
                               
                    html.Div([
                     html.Img(src="assets/temperature.jpg", 
                        alt="Thermometer", height = 150, width = 150),

                    html.Br(),

                    html.Center(html.P(get_weather_info(weather_df)['temp'], style={"color": "#56b4e9", "font-size":"15px"})),
                    ], style={'display': 'flex', 'flex-direction': 'column'}),
            
                    html.Div([
                        html.Img(src="assets/wind.png", 
                        alt="Cloud with wind", height = 150, width = 150, style = {'margin-left': '3em'} ),

                        html.Br(),

                        html.Center(html.P(get_weather_info(weather_df)['wind'], style={"color": "#56b4e9", "font-size":"15px", 'margin-left': '3em'}))
                    ], style={'display': 'flex', 'flex-direction': 'column'}),

                ], style={'display': 'flex', 'flex-direction': 'row'}),
             

                html.Div([
                    html.Div([
                        html.P(get_event_info(0, events_df )["adress"], className="event-type"),
                        html.P(get_event_info(0, events_df)["name"], className="event-name"),
                        html.Div([html.P(get_event_info(0, events_df)["time"]), 
                                  html.P(get_event_info(0, events_df)["respondent"])], 
                                  className="event-meta-grid")
                    ],className="today-children-grid"),
                    html.Div([
                        html.P(get_event_info(1, events_df)["adress"], className="event-type"),
                        html.P(get_event_info(1, events_df)["name"], className="event-name"),
                        html.Div([html.P(get_event_info(1, events_df)["time"]), 
                                  html.P(get_event_info(1, events_df)["respondent"])], 
                                  className="event-meta-grid")
                    ],className="today-children-grid"),
                    html.Div([
                        html.P(get_event_info(2, events_df)["adress"], className="event-type"),
                        html.P(get_event_info(2, events_df)["name"], className="event-name"),
                        html.Div([html.P(get_event_info(2, events_df)["time"]), 
                                  html.P(get_event_info(2, events_df)["respondent"])], 
                                  className="event-meta-grid")
                    ],className="today-children-grid"),
                     html.Div([
                        html.P(get_event_info(3, events_df)["adress"], className="event-type"),
                        html.P(get_event_info(3, events_df)["name"], className="event-name"),
                        html.Div([html.P(get_event_info(3, events_df)["time"]), 
                                  html.P(get_event_info(3, events_df)["respondent"])], 
                                  className="event-meta-grid")
                    ],className="today-children-grid"),
                ], className="today-parent-grid")
        

            ], style={'display': 'flex', 'flex-direction': 'row', 'margin-bottom': '2em'}, className = "flex-parent"),

            html.Div([season], style ={'margin-left': '5em', 'font-weight': 'bold', "color": "#244ba6", "font-size":"18px"})
    

        ], style = {'display': 'flex', 'flex-direction': 'column' }),

    ],className="page-content")
    return layout