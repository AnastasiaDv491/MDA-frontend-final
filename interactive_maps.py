
# Data: fakbars, events, mic_locations
import pandas as pd
import plotly.graph_objects as go
from io import StringIO 
import dash
from dash import Input, Output, dcc, html
import numpy as np
from dataload_AWS import AWS_instantiate

objects_AWS = AWS_instantiate.createAWSconnection() # Contains all objects from S3 bucket

events_data =["events_distances.csv", "Fakbars.csv", "mic_locations.xlsx"]
for file in objects_AWS:
    if file.key == "events_distances.csv":
        csv_file =file.get()['Body'].read().decode('utf-8')
        events_df= pd.read_csv(StringIO(csv_file))
        events_df.Respondents = events_df.Respondents.replace("na", np.nan).fillna(0)
        events_df.Respondents = events_df.Respondents.astype(float)
    elif file.key == "mic_locations.xlsx":
        mic_df= pd.read_excel(file.get()['Body'].read())
    elif file.key == "Fakbars.csv":
        csv_file =file.get()['Body'].read().decode('utf-8')
        fakbar_df= pd.read_csv(StringIO(csv_file))

# Create dropdown for map type

def buildDropdown():
    filter = html.Div(
    [
        dcc.Dropdown(
            options=["Scattermap", "Heatmap"],
            value='Scattermap', className = "page2-dropdown",
            id = "dropdownGraphs",
        ),
    
    ], 
    className="filters_parent"
    )
    return filter

mapbox_access_token = "pk.eyJ1IjoiYXRlcmxpZXIiLCJhIjoiY2xmOGoweGYzMDM1ODN4bzNqcjR4dXh1eSJ9.MOJuSulOVkeSuvbW3zbfrw"

def CreateGraph():
    div = html.Div(
        className = 'graph_div',
        children=[
            html.Br(),
            html.Br(),
            dcc.Graph(
                id="int-graph-id", 
            ),

        ]
    )
    return div

# Callback to get the data from storage into graph
@dash.callback(Output('int-graph-id', 'figure'), 
               Input('dropdownGraphs', 'value'))
def graph_update(value):

    if value == "Scattermap":
       
        fig = go.Figure()

        fig.add_trace(go.Scattermapbox(
                lat=events_df["Lat"],
                lon=events_df["Long"],
                mode='markers',
                marker=go.scattermapbox.Marker(
                    size=14,
                    color = "#3DB7E9"
                ),
                customdata=events_df['Event_name'],
                hovertemplate= '%{customdata}',
                text=['Leuven'],
                name = "Events"
            ))
        fig.add_trace(go.Scattermapbox(
                lat=mic_df["Lat"],
                lon=mic_df["Long"],
                mode='markers',
                marker=go.scattermapbox.Marker(
                    size=14,
                    color = "#E69F00"
                ),
                customdata=mic_df['Name'],
                hovertemplate= '%{customdata}',
                text=['Leuven'],
                name = "Microphones"
            ))

        fig.add_trace(go.Scattermapbox(
                lat=fakbar_df["Latitude"],
                lon=fakbar_df["Longitude"],
                mode='markers',
                marker=go.scattermapbox.Marker(
                    size=14,
                    color = "#F0E442"
                ),
                customdata=fakbar_df['Name'],
                hovertemplate= '%{customdata}',
                text=['Leuven'],
                name = "Fakbars"
            ))
        fig.update_layout(
            hovermode='closest',
            mapbox=dict(
                accesstoken=mapbox_access_token,
                bearing=0,
                center=go.layout.mapbox.Center(
                    lat=50.87959,
                    lon=4.70093
                ),
                pitch=0,
                zoom=13
            )
        )
    elif value == "Heatmap": 
        fig = go.Figure()

        fig.add_trace(go.Scattermapbox(
                lat=events_df["Lat"],
                lon=events_df["Long"],
                mode='markers',
                marker=go.scattermapbox.Marker(
                    size=events_df["Respondents"]/100,
                    color = "#359B73"
                ),
                customdata=np.stack((events_df['Event_name'], events_df['Respondents']), axis=-1),

                hovertemplate= '<i>Name</i>: %{customdata[0]}'+
                                '<br><b>Respondents</b>: %{customdata[1]}<br>',        
                name = "Events"
            )),
        fig.update_layout(
            hovermode='closest',
            mapbox=dict(
                accesstoken=mapbox_access_token,
                bearing=0,
                center=go.layout.mapbox.Center(
                    lat=50.87959,
                    lon=4.70093
                ),
                pitch=0,
                zoom=13
            )
        )
    return fig