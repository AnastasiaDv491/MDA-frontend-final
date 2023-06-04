from dash import html, register_page  #, callback # If you need callbacks, import it here.
import dash_dangerously_set_inner_html


register_page(
    __name__, # calling page objects' self.name
    name='Home', # your own selected name of the page
    top_nav=True,
    path='/' # path to the page on the website
)

# dash.page_container gives this page back to app.py
def layout():
    layout = html.Div( children =[
        html.Div( children = [
            html.Img(src="assets/police.jpg", 
            alt="Logo of the Belgian police force", height = 200, width = 200), 
            html.Br(),
            html.Br(),
            html.H2(children="Noise in Leuven",
            className = 'graph_header'
                            ),
                            
            html.Br(),
            html.Br(),

            html.P(dash_dangerously_set_inner_html.DangerouslySetInnerHTML("This app provides law enforcement officers <br /> with an overview of student activities in Leuven <br /> and daily predictions of noise levels.")),
        ], className="home-page-logo-text"
            
        )
        
    ], className="page-content-home")
    return layout
