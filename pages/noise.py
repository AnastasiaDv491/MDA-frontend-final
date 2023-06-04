
from dash import html, register_page  
from graph import build_graph_div, buildFilters
from dash import dcc

graph = build_graph_div()
filters = buildFilters()
register_page(
    __name__,
    name='Noise',
    top_nav=True,
    path='/noise'
)


def layout():
    layout = html.Div([
        dcc.Store(id='local', storage_type='local'),

        html.H2(children="Noise Levels",
        className = 'graph_header'),
        html.Br(),
        filters,
        graph,

    ],className="page-content")
    return layout

