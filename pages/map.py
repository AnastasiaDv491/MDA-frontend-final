from dash import html, register_page  #, callback # If you need callbacks, import it here.
from interactive_maps import CreateGraph, buildDropdown

graph = CreateGraph()
dropdown = buildDropdown()

register_page(
    __name__, # calling page objects' self.name
    name='Map', # your own selected name of the page
    top_nav=True,
    path='/map' # path to the page on the website
)

# dash.page_container gives this page back to app.py
def layout():
    layout = html.Div( children =[
       html.H2(children="Map of Leuven",
        className = 'graph_header'),
        dropdown, 
        graph,
        ], className="page-content")
    return layout