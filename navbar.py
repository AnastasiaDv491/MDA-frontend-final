from dash import html
import dash_bootstrap_components as dbc

# Icons: https://fontawesome.com/search
def create_navbar():
    navbar = dbc.NavbarSimple(
        children=[
            html.Div(children=[
                dbc.NavItem(children = [
                        dbc.NavLink(
                                    [
                                    html.I(className="fa-brands fa-github"),  # Font Awesome Icon
                                    " Front End"  # Text beside icon
                                ],
                                href="https://github.com/AnastasiaDv491/MDA-frontend-final",
                                target="_blank"
                            ),
                        dbc.NavLink(
                        [
                            html.I(className="fa-brands fa-github"),  # Font Awesome Icon
                            " Back End "  # Text beside icon
                        ],
                        href="https://github.com/AnastasiaDv491/Modern-Data-Analytics-Backend",
                        target="_blank"
                    )
                ]),
          

            ]),
        html.Div(children=[
            dbc.NavbarBrand("Home", href="/"),
            dbc.NavbarBrand("Noise", href="/noise"),
            dbc.NavbarBrand("Tonight", href="/tonight"),
            dbc.NavbarBrand("Map", href="/map")
            ])
        
        ])

    return navbar
