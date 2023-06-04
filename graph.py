import dash
from dash import Input, Output, dcc, html, State
import plotly.express as px
import plotly.graph_objects as go
import re
import pandas as pd
from dash.exceptions import PreventUpdate
import pandas as pd
from io import StringIO 
from dataload_AWS import AWS_instantiate
import dash_bootstrap_components as dbc


objects_AWS = AWS_instantiate.createAWSconnection() # Contains all objects from S3 bucket

# Get the location names for dropdown filter
locations_list =[]

for file in objects_AWS:
   locations_list.append(file.key)

reg_pattern = re.compile(r'night_(.*).csv$')
locations_clean = [ m.group(1) for m in (reg_pattern.search(location) for location in locations_list) if m ]

# Create filters
def buildFilters():
    filters = html.Div(
    [
        dcc.Dropdown(
            options=[{'label': x, 'value': x} for x in locations_clean],
            value='calverie', className = "page2-dropdown",
            id = "dropdownLocations",
        ),
     
        dcc.DatePickerSingle(
            id='my-date-picker-single',
            min_date_allowed="2022-07-01",
            max_date_allowed="2022-12-31",
            initial_visible_month="2022-09-06",
            date="2022-09-06",
        )
    
    ], 
    className="filters_parent"
    )
    return filters
    
# Create storage of selected data from filters
def build_graph_div():
    div = html.Div(
        className = 'graph_div',
        children=[
            dcc.Store(id='memory-output'),

            html.Br(),
            html.Br(),
            dbc.Alert("Observed data is missing!", color="danger", 
                               id = "missing_data_alert",
                               is_open = False),
            dcc.Graph(
                id="graph-id",
            ),
        ]
    )
    return div

# Callback to load the data from filters into storage
@dash.callback(Output('memory-output', 'data'), 
               Input('dropdownLocations', 'value'),
               Input('my-date-picker-single', 'date'))
def filterLocations(location_selected, date):
    for obj in objects_AWS:
        if location_selected in obj.key:
            csv_string =obj.get()['Body'].read().decode('utf-8')
            df_selected = pd.read_csv(StringIO(csv_string))
   
    df_selected['result_timestamp'] = pd.to_datetime(df_selected['result_timestamp'], errors='coerce')
    df_selected['Date'] = pd.to_datetime(df_selected['Date'], errors='coerce', format="%d-%m-%Y")
    df_selected["Date"] = df_selected["Date"].dt.strftime("%Y-%m-%d")
    
    
    df_selected = df_selected[df_selected["Date"]== date ]
    df_selected["result_timestamp"] = df_selected["result_timestamp"].dt.strftime("%H:%M")
    return df_selected.to_dict("records")

@dash.callback(Output("missing_data_alert", "is_open"),
               Input("memory-output", "data"),
               [State("missing_data_alert", "is_open")])

def buildAlert(df_selected, is_open):
    df_selected = pd.DataFrame(df_selected)
    if len(df_selected.laeq.value_counts()) <= 0:
        is_open = True
        return is_open
    else: 
        is_open = False
        return is_open

# Callback to get the data from storage into graph
@dash.callback(Output('graph-id', 'figure'), 
               Input('memory-output', 'data'))
def graph_update(df_selected):

    if df_selected is None:
        raise PreventUpdate
    else:
    # filtering based on the slide and dropdown selection
        df_selected = pd.DataFrame(df_selected)

        if df_selected.empty:
            html.H6("Data is missing")
            fig = go.Figure()
      
        else:
            fig = go.Figure()
            # Add traces
            fig.add_trace(go.Scatter(x=df_selected["result_timestamp"], y=df_selected["laeq"],
                                mode='markers',
                                marker= dict(color="#3DB7E9"),
                                name='Observed'))
            fig.add_trace(go.Scatter(x=df_selected["result_timestamp"], y=df_selected["y_pred"],
                                mode='lines+markers',
                                line=dict(color="#F0E442"),
                                name='Predictions (Mixed Models)'))
            fig.add_trace(go.Scatter(x=df_selected["result_timestamp"], y=df_selected["y_pred_gbr"],
                        mode='lines+markers',
                        line=dict(color="#D55E00"),
                        name='Predictions (Gradient Boosting)'))
            fig.add_trace(go.Scatter(x=df_selected["result_timestamp"], y=df_selected["y_pred_rf"],
                        mode='lines+markers',
                        line=dict(color="#359B73"),
                        name='Predictions (Random Forest)'))
    return fig


