import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
from dash.dependencies import Output, Input
import pathlib
from app import app

### OLD ###
## read data from file
#data = pd.read_csv(r"D:/Work/Repository/Visual Studio Code/Python/DHBW/Data Visualization/Exercises/ee_showcase_multipage/data/sales_ernesto_co_03.csv", sep=";")
###########

# read data from relative path
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data").resolve()
data = pd.read_csv(DATA_PATH.joinpath("data_01.csv"))

# # manipulate data for better insight & usability
# data["Verkaufsdatum"] = pd.to_datetime(data["Verkaufsdatum"], format="%Y%m%d")
# data["Gesamtumsatz"] = data["Verkaufspreis"] * data["Verkaufte Menge"]
# data["Planumsatz"] = data["Empfohlener Verkaufspreis"] * data["Verkaufte Menge (PLAN)"]
# data = data.replace({"Filiale" :   {100001 : "Ernesto & Friends",
#                                         100002 : "Kaffee2Go",
#                                         100010 : "GourmetCoffee",
#                                         100145 : "Coffee, Coffee, Coffee",
#                                         100146 : "Ernesto's Espresso"},
#                         "Produkt" : {1 : "Espresso",
#                                      2 : "Espresso extra forte",
#                                      3 : "Cappuccino",
#                                      5 : "Cappuccino forte",
#                                      8 : "Latte Macchiato",
#                                      10 : "Latte Macchiato forte",
#                                      15 : "Wasser",
#                                      20 : "Orangensaft",
#                                      21 : "Ananassaft",
#                                      50 : "Fitness Bagel",
#                                      51 : "Frühstücks Bagel",
#                                      52 : "Frischkäse Bagel",
#                                      60 : "Cookie",
#                                      64 : "Muffin Himbeere",
#                                      65 : "Muffin Jogurt"},
#                         "Lieferant" :   {5000000001 : "Gourmet Kaffee-Lieferant UNO",
#                                          5000000002 : "Kaffeespezialist No. 1",
#                                          5000000004 : "Arabica Express",
#                                          5000000005 : "Kaffeelieferant Heidelberg",
#                                          5000000006 : "Bohnenbringer GmbH",
#                                          5000000009 : "Black Gold Logistics"}})

# # create dataset for pie chart
# #dataPie = data[["Filiale", "Verkaufte Menge", "Gesamtumsatz"]]
# #dataPie = dataPie.groupby("Filiale")[["Gesamtumsatz", "Verkaufte Menge"]].sum().reset_index()
# dataPie = data[["Produkt des Monats", "Filiale", "Verkaufsdatum", "Verkaufte Menge", "Gesamtumsatz"]]
# dataPie = dataPie.groupby(["Produkt des Monats", "Filiale" ,"Verkaufsdatum"])[["Gesamtumsatz", "Verkaufte Menge"]].sum().reset_index()
    
# # create dataset for bar chart
# #dataBar = data[["Produktkategorie", "Verkaufte Menge", "Gesamtumsatz"]]
# #dataBar = dataBar.groupby("Produktkategorie")[["Gesamtumsatz", "Verkaufte Menge"]].sum().reset_index()
# dataBar = data[["Produktkategorie", "Filiale", "Verkaufsdatum", "Verkaufte Menge", "Gesamtumsatz"]]
# dataBar = dataBar.groupby(["Produktkategorie", "Filiale", "Verkaufsdatum"])[["Gesamtumsatz", "Verkaufte Menge"]].sum().reset_index()

# # create dataset for line chart
# dataLine = data[["Verkaufsdatum", "Filiale", "Verkaufte Menge", "Verkaufte Menge (PLAN)", "Gesamtumsatz", "Planumsatz"]]
# dataLine = dataLine.groupby(["Filiale", "Verkaufsdatum"])[["Verkaufte Menge", "Verkaufte Menge (PLAN)", "Gesamtumsatz", "Planumsatz"]].sum().reset_index()

# # create filter element for key figure switch
# chart_measure = pd.DataFrame({"Filter":["Total Revenue", "Total Volume"]})

# # define initial values
# initial_store = "Kaffee2Go"


# # app = dash.Dash(__name__)

# # app.title = "Ernesto Espresso Sales Dashboard"

# layout = html.Div(
#     children = [
#         # Header definition

#         # navigation block
#         html.Div(
#             children=[
#                 html.Div(
#                     children=[
#                         html.Div(children="Store", className="menu-title"),
#                         dcc.Dropdown(
#                             id="store-filter",
#                             options=[
#                                 {"label": store, "value": store}
#                                 for store in np.sort(data.Filiale.unique())
#                             ],
#                             value=initial_store,
#                             searchable=False,
#                             clearable=False,
#                             className="dropdown"
#                         )
#                     ]
#                 ),
#                 html.Div(
#                     children=[
#                         html.Div(children="Selling Date Range", className="menu-title"),
#                         dcc.DatePickerRange(
#                             id="date-range2",
#                             min_date_allowed=data.Verkaufsdatum.min().date(),
#                             max_date_allowed=data.Verkaufsdatum.max().date(),
#                             start_date=data.Verkaufsdatum.min().date(),
#                             end_date=data.Verkaufsdatum.max().date(),
#                         )
#                     ]
#                 )
#             ],
#             className="menu"
#         ),
#         # chart definition
#         html.Div(
#             children=[
#                 html.Div(
#                     children=
#                     [
#                         dcc.Graph(
#                             id="pie-chart2",
#                             className="card1"
#                         ),
#                         dcc.Graph(
#                             id="bar-chart2",
#                             className="card2"
#                         )
#                     ],
#                 ),
#                 html.Div(
#                     dcc.Graph(
#                         id="line-chart2",
#                         className="card3"
#                     )
#                 )
#             ],
#             className="content"
#         )
#     ]

# )

# @app.callback(
#     [
#         Output("pie-chart2", "figure"), 
#         Output("bar-chart2", "figure"), 
#         Output("line-chart2", "figure")
#     ],
#     [
#         Input("store-filter", "value"),
#         Input("date-range2", "start_date"),
#         Input("date-range2", "end_date")
#     ],

# )

# def update_charts2(selected_store, start_date, end_date):
    
#     maskPie = (
#         (dataPie.Filiale == selected_store)
#         & (dataPie.Verkaufsdatum >= start_date)
#         & (dataPie.Verkaufsdatum <= end_date)
#     )
#     maskBar = (
#         (dataBar.Filiale == selected_store)
#         & (dataBar.Verkaufsdatum >= start_date)
#         & (dataBar.Verkaufsdatum <= end_date)
#     )
#     maskLine = (
#         (dataLine.Verkaufsdatum >= start_date)
#         & (dataLine.Verkaufsdatum <= end_date)
#         & (dataBar.Filiale == selected_store)
#     )
    
#     filtered_dataPie = dataPie.loc[maskPie, :]
#     filtered_dataBar = dataBar.loc[maskBar, :]
#     filtered_dataLine = dataLine.loc[maskLine, :]
#     filtered_dataPie = filtered_dataPie.groupby("Produkt des Monats")[["Gesamtumsatz", "Verkaufte Menge", "Verkaufsdatum"]].sum().reset_index()
#     filtered_dataPie = filtered_dataPie.sort_values(by=["Gesamtumsatz"])
#     filtered_dataBar = filtered_dataBar.groupby("Produktkategorie")[["Gesamtumsatz", "Verkaufte Menge", "Verkaufsdatum"]].sum().reset_index()
#     filtered_dataLine = filtered_dataLine.groupby("Verkaufsdatum")[["Verkaufte Menge", "Verkaufte Menge (PLAN)", "Gesamtumsatz", "Planumsatz"]].sum().reset_index()

#     format_mapping={'Gesamtumsatz': '{:,.2f}', 'Verkaufte Menge': '{:,.0f}'}
#     for key, value in format_mapping.items():
#         filtered_dataBar[key] = filtered_dataBar[key].map(value.format)

#     format_mapping={'Gesamtumsatz': '{:,.2f}', 'Planumsatz': '{:,.2f}', 'Verkaufte Menge': '{:,.0f}', 'Verkaufte Menge (PLAN)': '{:,.0f}'}
#     for key, value in format_mapping.items():
#         filtered_dataLine[key] = filtered_dataLine[key].map(value.format)

#     # if selected_measure == "Gesamtumsatz":
#     #     selected_measure_plan = "Planumsatz"
#     #     name_line = "Revenue"
#     #     name_line_plan = "Planned Revenue"
#     # else:
#     #     selected_measure_plan = "Verkaufte Menge (PLAN)"
#     #     name_line = "Volume"
#     #     name_line_plan = "Planned Volume"

#     initial_store = selected_store

#     pie_chart_figure = {
#         "data": [
#             {
#                 "labels": filtered_dataPie["Produkt des Monats"],
#                 "values": filtered_dataPie["Gesamtumsatz"],
#                 "type": "pie",
#                 "sort": True,
#                 "direction": "clockwise",
#                 "marker": {
#                     "colors": [
#                         "#512f1566",
#                         "#512f15ff"
#                     ]
#                 }
#             }
#         ],
#         "layout": {
#             "title": "Sales by Product of the Month",
#             "showlegend": False,
#             "paper_bgcolor": "#00000000",
#             "plot_bgcolor": "#00000000"
#         }
#     }

#     bar_chart_figure = {
#         "data": [
#             {
#                 "x": filtered_dataBar["Produktkategorie"],
#                 "y": filtered_dataBar["Gesamtumsatz"],
#                 "type": "bar",
#                 "marker": {"color": "#512f15"},
#                 "text": filtered_dataBar["Gesamtumsatz"],
#                 "textposition": "auto"
#             }
#         ],
#         "layout": {
#             "title": "Sales by Product Category",
#             "showlegend": False,
#             "paper_bgcolor": "#00000000",
#             "plot_bgcolor": "#00000000",
#             "xaxis": {"showgrid": False},
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
#                 "x": filtered_dataLine["Verkaufsdatum"],
#                 "y": filtered_dataLine["Gesamtumsatz"],
#                 "type": "line",
#                 "name": "Gesamtumsatz",
#                 "line": {"width": 4},
#                 "marker": {"color": "#512f15"},
#             },
#             {
#                 "x": filtered_dataLine["Verkaufsdatum"],
#                 "y": filtered_dataLine["Planumsatz"],
#                 "type": "line",
#                 "name": "Planumsatz",
#                 "line": {"width": 4},
#                 "marker": {"color": "#6c7744"},
#             }
#         ],
#         "layout": {
#             "title": "Sales by Selling Date",
#             "showlegend": False,
#             "paper_bgcolor": "#00000000",
#             "plot_bgcolor": "#00000000",
#         }
#     }

#     return pie_chart_figure, bar_chart_figure, line_chart_figure



# if __name__ == "__main__":
#     app.run_server(debug=True)
