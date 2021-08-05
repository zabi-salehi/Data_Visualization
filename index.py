import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Connect to the main file app.py
from app import app
from app import server

# connect all app pages to the application
from apps import global_view, store_view

# application layout definition
app.layout = html.Div(
    [
        html.Div(
            children=[
                html.Img(
                    src=app.get_asset_url("logo.png"),
                    style={
                        "height": "50px",
                        "width": "50px",
                        "textAlign": "center",
                        "vertical-align": "top",
                        "padding": "2px",
                        "margin-left": "0px"
                    }
                ),
                html.Div(
                    children=[
                        html.H1(
                            "Ernesto Espresso", 
                            className="header-title"
                        ),
                        html.P(
                            children=
                            [
                                "A global Corporate Sales Analytics Dashboard for all",
                                html.Br(),
                                "Ernesto Espresso stores in germany"
                            ], 
                            className="header-description"
                            
                        )
                    ], 
                    style={"display": "inline-block"}
                ),
                html.Div(
                    [
                        dcc.Link("Global View", id="button-1", href="/apps/global_view", className="active"),
                        dcc.Link("Local View",id="button-2" ,href="/apps/store_view", className="button")
                    ],
                    className="header-links",
                    #style={"display": "inline-block"}
                ),
                dcc.Location(id="url", refresh=False, pathname="/apps/global_view"),
            ],
            className="header"
        ),
        html.Div(id="page-content", children=[])
    ]
)

@app.callback(
    [
        Output(component_id="page-content", component_property="children"),
        Output(component_id="button-1", component_property="className"),
        Output(component_id="button-2", component_property="className")
    ],
    [Input(component_id="url", component_property="pathname")]
)
def return_page(pathname):
    if pathname == "/apps/global_view":
        return global_view.layout, "active", "button"
    if pathname == "/apps/store_view":
        return store_view.layout, "button", "active"
    else:
        return "Page Error 404! This page does not exist."

if __name__ == "__main__":
    app.run_server(debug=True)
