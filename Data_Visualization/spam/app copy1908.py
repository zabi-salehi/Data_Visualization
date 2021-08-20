import datetime
from datetime import date
from datetime import datetime as dt
import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from dash_html_components.Datalist import Datalist

# read data from file
data = pd.read_excel(r"data\data.xlsx")

#dropping some columns since unnecessaary
data.drop("Unnamed: 34", inplace=True, axis=1)
data.drop("Unnamed: 35", inplace=True, axis=1)
data.drop("Delivery deviation  in days", inplace=True, axis=1)

data["Delivery deviation in days"] = data["delivery date"] - data["supplier delivery date"]
data["Delivery deviation in days"] = data["Delivery deviation in days"].apply(lambda x: float(x.days))

conditions = [(data['Delivery deviation in days'] <= 0),
              (data['Delivery deviation in days'] >= 1) & (data['Delivery deviation in days'] <= 4),
              (data['Delivery deviation in days'] >= 5) & (data['Delivery deviation in days'] <= 10),
              (data['Delivery deviation in days'] > 10)]

values = ['in time', 'late: < 5 days', 'late: 5 to 10 days', 'late: > 10 days']
data['deviation indicator'] = np.select(conditions, values)

data['Year'] = data['Document Date'].dt.year
data['Month'] = data['Document Date'].dt.month
data['Year/Month'] = data['Document Date'].dt.year.astype(str) + '/' + data['Document Date'].dt.month.astype(str)

orderedSpend_year = data.groupby(["Year"])[["Net Value"]].sum().reset_index()

data_2019 = data[data["Year"] == 2019]
data_2020 = data[data["Year"] == 2020]

numbOrders_2019 = len(pd.unique(data_2019["Purchasing Doc."]))

numbOrders_2020 = len(pd.unique(data_2020["Purchasing Doc."]))

orderdSpend_month_2019 = data_2019.groupby(["Month"])[["Net Value"]].sum().reset_index()
orderdSpend_month_2020 = data_2020.groupby(["Month"])[["Net Value"]].sum().reset_index()

df2019_without_purchDoc_duplicates = data_2019.drop_duplicates(subset=['Purchasing Doc.'])
df2020_without_purchDoc_duplicates = data_2020.drop_duplicates(subset=['Purchasing Doc.'])

numbOrders_month_2019 = df2019_without_purchDoc_duplicates.groupby(
    ["Month"])[["Purchasing Doc."]].count().reset_index().rename(columns={"Purchasing Doc.": "numbOrders"})
numbOrders_month_2020 = df2020_without_purchDoc_duplicates.groupby(
    ["Month"])[["Purchasing Doc."]].count().reset_index().rename(columns={"Purchasing Doc.": "numbOrders"})

orderdSpend_purchOrg_2019 = data_2019.groupby(["Purchasing Org."])[["Net Value"]].sum().reset_index()
orderdSpend_purchOrg_2020 = data_2020.groupby(["Purchasing Org."])[["Net Value"]].sum().reset_index()
df2019_without_purchDoc_duplicates = data_2019.drop_duplicates(subset=['Purchasing Doc.'])
df2020_without_purchDoc_duplicates = data_2020.drop_duplicates(subset=['Purchasing Doc.'])

numbOrders_purchOrg_2019 = df2019_without_purchDoc_duplicates.groupby(
    ["Purchasing Org."])[["Purchasing Doc."]].count().reset_index().rename(columns={"Purchasing Doc.": "numbOrders"})
numbOrders_purchOrg_2020 = df2020_without_purchDoc_duplicates.groupby(
    ["Purchasing Org."])[["Purchasing Doc."]].count().reset_index().rename(columns={"Purchasing Doc.": "numbOrders"})
# zum string umwandeln damit plotly die zahlen nicht als zahl sondern als eine Bezeichnung für Organistan erkennt
orderdSpend_purchOrg_2019["Purchasing Org."] = orderdSpend_purchOrg_2019["Purchasing Org."].apply(lambda x: 'PO: ' + str(x))
orderdSpend_purchOrg_2020["Purchasing Org."] = orderdSpend_purchOrg_2020["Purchasing Org."].apply(lambda x: 'PO: ' + str(x))
numbOrders_purchOrg_2019["Purchasing Org."] = numbOrders_purchOrg_2019["Purchasing Org."].apply(lambda x: 'PO: ' + str(x))
numbOrders_purchOrg_2020["Purchasing Org."] = numbOrders_purchOrg_2020["Purchasing Org."].apply(lambda x: 'PO: ' + str(x))



supplier_netValue = data.groupby(["Year",
                                "Supplier name"])[["Net Value"]].sum().reset_index().sort_values(by="Net Value",
                                                                                                ascending=False)
top10_2019 = data_2019.groupby(["Supplier name"])[["Net Value"
                                                ]].sum().reset_index().sort_values(by="Net Value",
                                                                                    ascending=False).head(10)
top10_2020 = data_2020.groupby(["Supplier name"])[["Net Value"
                                                ]].sum().reset_index().sort_values(by="Net Value",
                                                                                    ascending=False).head(10)

options_einkauforg = [
    {"label": "54", "value": "54"},
    {"label": "5200", "value": "5200"},
    {"label": "5210", "value": "5210"},
    {"label": "5310", "value": "5310"},
    {"label": "5320", "value": "5320"},
    {"label": "5400", "value": "5400"},
    {"label": "5410", "value": "5410"},
    {"label": "5420", "value": "5420"},
]
all_einkaufsorg = [option["value"] for option in options_einkauforg]

options_company_code = [
    {"label": "52", "value": "52"},
    {"label": "53", "value": "53"},
    {"label": "54", "value": "54"}
]

options_werke = [
    {"label": "51", "value": "51"},
    {"label": "61", "value": "61"},
    {"label": "62", "value": "62"},
    {"label": "77", "value": "77"},
    {"label": "78", "value": "78"},
    {"label": "3799", "value": "3799"},
    {"label": "5899", "value": "5899"},
    {"label": "6599", "value": "6599"},
    {"label": "9699", "value": "9699"}
]
all_werke = [option["value"] for option in options_werke]

def datenbasis_anpassen(**kwargs):
    global data
    data_temp = data.copy()

    if kwargs["einkaufsorg"]:
        einkaufsorg = kwargs["einkaufsorg"]
        benoetigte_einkaufsorg = [i for i in all_einkaufsorg if i in einkaufsorg]
        print(benoetigte_einkaufsorg)
        data = data[data["Purchasing Org."]==benoetigte_einkaufsorg]
        print(data)

    if kwargs["werke"]:
        werke = kwargs["werke"]
        benoetigte_werke = [i for i in all_werke if i in werke]
        print(benoetigte_werke)
        data = data[data["Purchasing Org."]==benoetigte_werke]
        print(data)

    orderedSpend_year = data.groupby(["Year"])[["Net Value"]].sum().reset_index()

    data_2019 = data[data["Year"] == 2019]
    data_2020 = data[data["Year"] == 2020]

    numbOrders_2019 = len(pd.unique(data_2019["Purchasing Doc."]))

    numbOrders_2020 = len(pd.unique(data_2020["Purchasing Doc."]))

    orderdSpend_month_2019 = data_2019.groupby(["Month"])[["Net Value"]].sum().reset_index()
    orderdSpend_month_2020 = data_2020.groupby(["Month"])[["Net Value"]].sum().reset_index()

    df2019_without_purchDoc_duplicates = data_2019.drop_duplicates(subset=['Purchasing Doc.'])
    df2020_without_purchDoc_duplicates = data_2020.drop_duplicates(subset=['Purchasing Doc.'])

    numbOrders_month_2019 = df2019_without_purchDoc_duplicates.groupby(
        ["Month"])[["Purchasing Doc."]].count().reset_index().rename(columns={"Purchasing Doc.": "numbOrders"})
    numbOrders_month_2020 = df2020_without_purchDoc_duplicates.groupby(
        ["Month"])[["Purchasing Doc."]].count().reset_index().rename(columns={"Purchasing Doc.": "numbOrders"})

    orderdSpend_purchOrg_2019 = data_2019.groupby(["Purchasing Org."])[["Net Value"]].sum().reset_index()
    orderdSpend_purchOrg_2020 = data_2020.groupby(["Purchasing Org."])[["Net Value"]].sum().reset_index()
    df2019_without_purchDoc_duplicates = data_2019.drop_duplicates(subset=['Purchasing Doc.'])
    df2020_without_purchDoc_duplicates = data_2020.drop_duplicates(subset=['Purchasing Doc.'])

    numbOrders_purchOrg_2019 = df2019_without_purchDoc_duplicates.groupby(
        ["Purchasing Org."])[["Purchasing Doc."]].count().reset_index().rename(columns={"Purchasing Doc.": "numbOrders"})
    numbOrders_purchOrg_2020 = df2020_without_purchDoc_duplicates.groupby(
        ["Purchasing Org."])[["Purchasing Doc."]].count().reset_index().rename(columns={"Purchasing Doc.": "numbOrders"})
    # zum string umwandeln damit plotly die zahlen nicht als zahl sondern als eine Bezeichnung für Organistan erkennt
    orderdSpend_purchOrg_2019["Purchasing Org."] = orderdSpend_purchOrg_2019["Purchasing Org."].apply(lambda x: 'PO: ' + str(x))
    orderdSpend_purchOrg_2020["Purchasing Org."] = orderdSpend_purchOrg_2020["Purchasing Org."].apply(lambda x: 'PO: ' + str(x))
    numbOrders_purchOrg_2019["Purchasing Org."] = numbOrders_purchOrg_2019["Purchasing Org."].apply(lambda x: 'PO: ' + str(x))
    numbOrders_purchOrg_2020["Purchasing Org."] = numbOrders_purchOrg_2020["Purchasing Org."].apply(lambda x: 'PO: ' + str(x))



    supplier_netValue = data.groupby(["Year",
                                    "Supplier name"])[["Net Value"]].sum().reset_index().sort_values(by="Net Value",
                                                                                                    ascending=False)
    top10_2019 = data_2019.groupby(["Supplier name"])[["Net Value"
                                                    ]].sum().reset_index().sort_values(by="Net Value",
                                                                                        ascending=False).head(10)
    top10_2020 = data_2020.groupby(["Supplier name"])[["Net Value"
                                                    ]].sum().reset_index().sort_values(by="Net Value",
                                                                                        ascending=False).head(10)

    update_charts()
# create filter element for key figure switch
# chart_measure = pd.DataFrame({"Filter": ["Total Revenue", "Total Volume"]})  # was genau macht das?

app = dash.Dash(__name__)

colors = { # Farben können an den Styleguide angepasst werden und werden für alle Diagramme übernommen
    'text1' : '#ff0000', # Farbe für normale Schrift
    'text2' : '#0B610B', # Variation der Schriftfarbe
    # Farbe für Hintergründe des Plots
    'plot_bgcolor' : '#e3e4da', # um papercolor herum außerhalb des plots
    'paper_bgcolor' : '#d3d3d3',# Farbe für Hintergründe des Paperbackground (vor plot background)
    'color_text_in_plots': '#ffffff' # Farbe für die Texte im Plot
}


app.title = "Supplier Mangement Dashboard"

app.layout = html.Div(children=[
    # Header definition
    html.Div(children=[
        html.Img(src=app.get_asset_url("logo.png"),
                 style={
                     "height": "50px",
                     "width": "50px",
                     "textAlign": "center",
                     "vertical-align": "top",
                     "padding": "2px"
                 }),
        html.Div(children=[
            html.H1("Supplier Management", className="header-title"),
            html.H2(children=[
                "A Dashboard to monitor supplier performance",
            ], className="header-description")
        ],
                 style={"display": "inline-block"}),
    ],
             className="header"),
    # navigation block
    html.Div(children=[
        html.Div(children=[
            html.Div(children="Measure", className="menu-title"),
            dcc.Dropdown(id="measure-filter",
                         options=[{
                             "label": "Company code ",
                             "value": "Company Code"
                         }, {
                             "label": "Purchasing Org.",
                             "value": "Purchasing Organisation"
                         }, {
                             "label": "Plant",
                             "value": "Plant"
                         }, {
                             "label": "Material Group",
                             "value": "Material Group"
                         }],
                         value="Purchasing Org.",
                         searchable=False,
                         clearable=False,
                         className="dropdown")
        ]),

      
        html.Div(children = [
            html.Div(children = 'Net Value or Number of Orders', className ="menu-title"),
            dcc.Dropdown(
                id = 'os-nof',
                options=[
                    {"label": "Net Value", "value": "net_value"},
                    {"label": "Number of orders", "value": "number_of_orders"},
                ],
                value="net_value",
                searchable = True,
                className="dropdown"

            )
        ]
        ),
        html.Div(children=[
            html.Div(children="Daterange", className ="menu-title"),
            dcc.DatePickerRange(
                id='date_range',
                min_date_allowed = dt(2019,1,1),
                max_date_allowed = dt(2020,6,30),
                initial_visible_month = dt(2019,1,1),
                end_date = dt(2020,6,30)
            )
        ])
        # html.Div(children=[
        #     html.Div(children="Date", className="menu-title"),
        #     dcc.Dropdown(id="date",
        #                  options=[{
        #                      "label": "2020",
        #                      "value": "2020"
        #                  }, {
        #                      "label": "2019",
        #                      "value": "2019"
        #                  }],
        #                  value="2020",
        #                  searchable=False,
        #                  clearable=False,
        #                  className="dropdown"),
        # ])
    ],
             className="menu"),
    # html.Br(),
    # html.Br(),
    html.H3("Filterbar", className ="filterbar-title"),
    html.Br(),
    # filterblock unter navigationblock
    html.Div(children=[
        
        html.Div(children="Filter for Purchasing Organisation", className ='filter-title'),
        html.Div(
            [
            dcc.Checklist(
                id="all-einkaufsorg-checklist",
                options=[{"label": "All", "value": "All"}],
                value=["All"],
                labelStyle={"display": "inline-block"},
            ),
            dcc.Checklist(
                id="einkaufsorg-checklist",
                options=options_einkauforg,
                value=[],
                labelStyle={"display": "inline-block"},
            ),
            ], className = "dropdown"
        ),

        html.Div(children = [
            html.Div(children= "Filter for Company Code", className ='filter-title'),
            dcc.Dropdown(
                id = 'company_code_dropdown',
                options =   options_company_code,
                value=['52', '53', '54'],
                searchable = True,
                multi = True,
                className="dropdown",
                persistence_type = "local"

            ), 
            
        ], className = "dropdown"
        ),

        html.Div(children="Filter for plants", className ='filter-title'),
        html.Div(
            [
            dcc.Checklist(
                id="all-werke-checklist",
                options=[{"label": "All", "value": "All"}],
                value=["All"],
                labelStyle={"display": "inline-block"},
            ),
            dcc.Checklist(
                id="werke-checklist",
                options=options_werke,
                value=[],
                labelStyle={"display": "inline-block"},
            ),
            ], className = "dropdown"
        ),







    ], className = 'filter-menu'
    ),
    # chart definition
    html.Div(children=[
        html.Div(children=[
            dcc.Graph(id= "numeric-point-chart", className = "card1"),
            dcc.Graph(id="year-bar-chart", className="card2"),
        
        ]
        ),
        html.Div(dcc.Graph(id="month-line-chart", className="card3")),

        html.Div(children=[
            dcc.Graph(id="top10_2020", className = "card4"),
            dcc.Graph(id="top10_2019", className="card5")
        ], )
    ],
             className="content")
])


@app.callback(
    [
        Output("numeric-point-chart", "figure"),
        Output("year-bar-chart", "figure"),
        Output("month-line-chart", "figure"),
        Output("top10_2020", "figure"),
        Output("top10_2019", "figure"),
    ],
    [Input("os-nof", "value")],
)

def update_charts(selected_value):

    if selected_value == "net_value":

        # numeric point chart (Aufgaben 1+2)
        fig = go.Figure()

        fig.add_trace(go.Indicator(
            mode = "number",
            value = float(orderedSpend_year[orderedSpend_year["Year"]==2019]["Net Value"]),
            number = {'prefix': ""},
            delta = {'position': "top", 'reference': 320},
            title = {'text': 'Ordered spend 2019'},
            domain = {'row':0, 'column': 0}))

        fig.add_trace(go.Indicator(
            mode = "number",
            value = float(orderedSpend_year[orderedSpend_year["Year"]==2020]["Net Value"]),
            number = {'prefix': ""},
            delta = {'position': "top", 'reference': 320},
            title = {'text': 'Ordered spend 2020'},
            domain = {'row':1, 'column': 0}))

        fig.update_layout(
            grid = {'rows':2, 'columns': 1},
            paper_bgcolor = colors["paper_bgcolor"],
           # plot_bgcolor = colors["plot_bgcolor"]
            )

        # bar chart 1: Aufgabe 4
        bar_chart_figure1 = {
            'data': [
                {
                    'x': orderdSpend_purchOrg_2020["Purchasing Org."],
                    'y': orderdSpend_purchOrg_2020["Net Value"],
                    'type': 'bar',
                    'name': '2020'
                },
                {
                    'x': orderdSpend_purchOrg_2019["Purchasing Org."],
                    'y': orderdSpend_purchOrg_2019["Net Value"],
                    'type': 'bar',
                    'name': '2019'
                },
            ],
            "layout": {
                "title": "Ordered spend per purchasing Org. according to 'Net Value'",
                "showlegend": True,
                "paper_bgcolor": colors["paper_bgcolor"],
                "plot_bgcolor": colors["plot_bgcolor"]
            }
        }

        # line chart: Aufgabe 3
        line_chart_figure = {
            "data": [
                {
                    "x": orderdSpend_month_2019["Month"],
                    "y": orderdSpend_month_2019["Net Value"],
                    "type": "line",
                    # "name": name_line,
                    "line": {
                        "width": 4
                    },
                    "marker": {
                        "color": "#512f15"
                    },
                },
                {
                    "x": orderdSpend_month_2020["Month"],
                    "y": orderdSpend_month_2020["Net Value"],
                    "type": "line",
                    # "name": name_line_plan,
                    "line": {
                        "width": 4
                    },
                    "marker": {
                        "color": "#6c7744"
                    },
                }
            ],
            "layout": {
                "title": "Net Value per Month",
                "showlegend": False,
                "paper_bgcolor": colors["paper_bgcolor"],
                "plot_bgcolor": colors["plot_bgcolor"]
            }
        }

    elif selected_value == "number_of_orders":

        fig = go.Figure()

        fig.add_trace(go.Indicator(
            mode = "number",
            value = numbOrders_2019,
            number = {'prefix': ""},
            delta = {'position': "top", 'reference': 320},
            title = {'text': 'Ordered spend 2019'},
            domain = {'row':0, 'column': 0}))

        fig.add_trace(go.Indicator(
            mode = "number",
            value = numbOrders_2020,
            number = {'prefix': ""},
            delta = {'position': "top", 'reference': 320},
            title = {'text': 'Ordered spend 2020'},
            domain = {'row':1, 'column': 0}))

        fig.update_layout(
            grid = {'rows':2, 'columns': 1},
            paper_bgcolor = colors["paper_bgcolor"]
        
            #plot_bgcolor = colors["plot_bgcolor"])
        )


        bar_chart_figure1 = {
            'data': [
                {
                    'x': numbOrders_purchOrg_2020["Purchasing Org."],
                    'y': numbOrders_2020,
                    'type': 'bar',
                    'name': '2020'
                },
                {
                    'x': orderdSpend_purchOrg_2019["Purchasing Org."],
                    'y': numbOrders_2019,
                    'type': 'bar',
                    'name': '2019'
                },
            ],
            "layout": {
                "title": "Ordered spend per purchasing Org. according to Number of Orders",
                "showlegend": True,
                "paper_bgcolor": colors["paper_bgcolor"],
                "plot_bgcolor": colors["plot_bgcolor"]
            }
        }

        line_chart_figure = {
            "data": [
                {
                    "x": numbOrders_month_2020["Month"],
                    "y": numbOrders_month_2020["numbOrders"],
                    "type": "line",
                    # "name": name_line,
                    "line": {
                        "width": 4
                    },
                    "marker": {
                        "color": "#512f15"
                    },
                },
                {
                    "x": numbOrders_month_2019["Month"],
                    "y": numbOrders_month_2019["numbOrders"],
                    "type": "line",
                    # "name": name_line_plan,
                    "line": {
                        "width": 4
                    },
                    "marker": {
                        "color": "#6c7744"
                    },
                }
            ],
            "layout": {
                "title": "Number of Orders per Month",
                "showlegend": False,
                "paper_bgcolor": colors["paper_bgcolor"],
                "plot_bgcolor": colors["plot_bgcolor"]
            }
        }
    else: 
        line_chart_figure = None
        bar_chart_figure1 = None
        fig = None

    # bar chart 2: Aufgabe 5, Teil 1: 2019

    bar_chart_figure2 = {
        "data": [{
            "x": top10_2019["Supplier name"],
            "y": top10_2019["Net Value"],
            "type": "bar",
            "marker": {
                "color": "#512f15"
            }
            # "text": filtered_dataBar[selected_measure],
            # "textposition": "auto"
        }],
        "layout": {
            "title": "Net Value by Supplier 2019",
            "showlegend": False,
            "paper_bgcolor": colors["paper_bgcolor"],
            "plot_bgcolor": colors["plot_bgcolor"],
            "xaxis": {
                "showgrid": False
            },
            "yaxis": {
                "showgrid": False,
                "visible": False,
                "showticklabels": False
            }
        }
    }

    # bar chart 4: Aufgabe 5, Teil 2: 2020

    bar_chart_figure4 = {"data": [{
            "x": top10_2020["Supplier name"],
            "y": top10_2020["Net Value"],
            "type": "bar",
            "marker": {
                "color": "#512f15"
            }
            # "text": filtered_dataBar[selected_measure],
            # "textposition": "auto"
        }],
        "layout": {
            "title": "Net Value by Supplier 2020",
            "showlegend": False,
            "paper_bgcolor": colors["paper_bgcolor"],
            "plot_bgcolor": colors["plot_bgcolor"],
            "xaxis": {
                "showgrid": False
            },
            "yaxis": {
                "showgrid": False,
                "visible": False,
                "showticklabels": False
            }
        }
    }

    numeric_chart_figure = fig

    return  numeric_chart_figure, bar_chart_figure1, line_chart_figure, bar_chart_figure2, bar_chart_figure4

@app.callback(
    Output("einkaufsorg-checklist", "value"),
    Output("all-einkaufsorg-checklist", "value"),
    Input("einkaufsorg-checklist", "value"),
    Input("all-einkaufsorg-checklist", "value"),
)
def sync_checklists(einkaufsorg_selected, all_selected):
    ctx = dash.callback_context
    input_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if input_id == "einkaufsorg-checklist":
        all_selected = ["All"] if set(einkaufsorg_selected) == set(all_einkaufsorg) else []
    else:
        einkaufsorg_selected = all_einkaufsorg if all_selected else []
    #print(cities_selected, all_selected)
    if all_selected == ["All"]:
        return einkaufsorg_selected, all_selected
    else:
        print(einkaufsorg_selected)
        datenbasis_anpassen(einkaufsorg = einkaufsorg_selected)
        return einkaufsorg_selected, all_selected

@app.callback(
    Output("werke-checklist", "value"),
    Output("all-werke-checklist", "value"),
    Input("werke-checklist", "value"),
    Input("all-werke-checklist", "value"),
)
def sync_checklists2(werke_selected, all_selected):
    ctx = dash.callback_context
    input_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if input_id == "werke-checklist":
        all_selected = ["All"] if set(werke_selected) == set(all_werke) else []
    else:
        werke_selected = all_werke if all_selected else []

    if all_selected == ["All"]:
        return werke_selected, all_selected
    else:
        datenbasis_anpassen(werke = werke_selected)
        return werke_selected, all_selected

# @app.callback(
#     [
#         Output("year-bar-chart", "figure"),
#         Output("month-line-chart", "figure"),
#         Output("PurchasingOrg-bar-chart", "figure")
#     ],
#     [Input("measure-filter", "value")],
# )
# def update_charts(selected_measure):



#     bar_chart_figure1 = {
#         'data': [
#             {
#                 'x': orderdSpend_purchOrg_2020["Purchasing Org."],
#                 'y': orderdSpend_purchOrg_2020["Net Value"],
#                 'type': 'bar',
#                 'name': '2020'
#             },
#             {
#                 'x': orderdSpend_purchOrg_2019["Purchasing Org."],
#                 'y': orderdSpend_purchOrg_2019["Net Value"],
#                 'type': 'bar',
#                 'name': '2019'
#             },
#         ],
#         "layout": {
#             "title": "Ordered spend per purchasing Org. according to 'Net Value'",
#             "showlegend": True,
#             "paper_bgcolor": "#00000000",
#             "plot_bgcolor": "#00000000"
#         }
#     }

#     bar_chart_figure2 = {
#         "data": [{
#             "x": top10_2019["Supplier name"],
#             "y": top10_2019["Net Value"],
#             "type": "bar",
#             "marker": {
#                 "color": "#512f15"
#             }
#             # "text": filtered_dataBar[selected_measure],
#             # "textposition": "auto"
#         }],
#         "layout": {
#             "title": "Sales by Product Category",
#             "showlegend": False,
#             "paper_bgcolor": "#00000000",
#             "plot_bgcolor": "#00000000",
#             "xaxis": {
#                 "showgrid": False
#             },
#             "yaxis": {
#                 "showgrid": False,
#                 "visible": False,
#                 "showticklabels": False
#             }
#         }
#     }

#     line_chart_figure = {
#         "data": [
#             {
#                 "x": orderdSpend_month_2019["Month"],
#                 "y": orderdSpend_month_2019["Net Value"],
#                 "type": "line",
#                 # "name": name_line,
#                 "line": {
#                     "width": 4
#                 },
#                 "marker": {
#                     "color": "#512f15"
#                 },
#             },
#             {
#                 "x": orderdSpend_month_2020["Month"],
#                 "y": orderdSpend_month_2020["Net Value"],
#                 "type": "line",
#                 # "name": name_line_plan,
#                 "line": {
#                     "width": 4
#                 },
#                 "marker": {
#                     "color": "#6c7744"
#                 },
#             }
#         ],
#         "layout": {
#             "title": "Sales by Selling Date",
#             "showlegend": False,
#             "paper_bgcolor": "#00000000",
#             "plot_bgcolor": "#00000000",
#         }
#     }

if __name__ == "__main__":
    app.run_server(debug=True)
