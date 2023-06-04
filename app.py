import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from navbar import create_navbar # importing navbar code
from dash import dcc, html
import os

NAVBAR = create_navbar()
# To use Font Awesome Icons
FA621 = "https://use.fontawesome.com/releases/v6.2.1/css/all.css"


app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    # Use external themes 
    external_stylesheets=[
        dbc.themes.LUX,  # Dash Themes CSS
        FA621,  # Font Awesome Icons CSS
    ],
    use_pages=True,  # New in Dash 2.7 - Allows us to register pages
     pages_folder= os.path.join(os.path.dirname(__name__), "pages"), #letting the server know where to find pages
     meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ],
)

app.layout = dcc.Loading(  # <- Wrap App with Loading Component
    id='loading_page_content',
    children=[
        html.Div(
            [
                NAVBAR,
                dash.page_container, 

            ],
            id = "main_container"
        )
    ],
    color='primary', 
    fullscreen=True  
)

server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)