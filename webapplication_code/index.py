#loading all the needed libraries
import dash
import dash_core_components as dcc
from dash import html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

# from app import server
from app import app
# import all pages in the apps
from apps import home
server = app.server
# building the navigation bar
dropdown = dbc.DropdownMenu(
    children=[
        dbc.DropdownMenuItem("Home", href="/home"),
        
    ],
    nav = True,
    in_navbar = True,
    label = "Menu",
    align_end = True,
)

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # code for initial column in the navigation bar
                dbc.Row(
                    [
                        dbc.Col(dbc.NavbarBrand("Tomato leaf disease detection", className="ml-2")),
                        
                    ],
                    align="center",
                ),
                href="/home",
            ),
          
        ]
    ),
    color="dark",
    dark=True,
    className="mb-4",
)
#this is the function for navigation bar
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

for i in [2]:
    app.callback(
        Output(f"navbar-collapse{i}", "is_open"),
        [Input(f"navbar-toggler{i}", "n_clicks")],
        [State(f"navbar-collapse{i}", "is_open")],
    )(toggle_navbar_collapse)

# embedding the navigation bar
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content')
])

#for dynamic functionality of the code
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
        return home.layout

if __name__ == '__main__':
    app.run_server(port = 8079, debug=True)