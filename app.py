import datetime
from datetime import date

import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from dash_html_components.Datalist import Datalist

# read data from file
data = pd.read_excel("data//data.xlsx")

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

# orderedSpend_numbOrders_year = data.groupby(["Year"])[["Net Value", "ORDERED Quantity"]].sum().reset_index()
orderedSpend_numbOrders_year = data.groupby(["Year", "Purchasing Org.", "Company Code", "Plant",
                                             "Material Group"])[["Net Value", "ORDERED Quantity"]].sum().reset_index()

Netvalue = [orderedSpend_numbOrders_year["Net Value"].iloc[0], orderedSpend_numbOrders_year["Net Value"].iloc[1]]
orderd_quantity = [
    orderedSpend_numbOrders_year["ORDERED Quantity"].iloc[0], orderedSpend_numbOrders_year["ORDERED Quantity"].iloc[1]
]

orderedSpend_numbOrders_year_month = data.groupby(["Month"])[["Net Value", "ORDERED Quantity"]].sum().reset_index()

orderedSpend_numbOrders_year_PurchOrg = data.groupby(["Purchasing Org."])[["Net Value",
                                                                           "ORDERED Quantity"]].sum().reset_index()

supplier_netValue = data.groupby(["Year",
                                  "Supplier name"])[["Net Value"]].sum().reset_index().sort_values(by="Net Value",
                                                                                                   ascending=False)
top_10_2019 = supplier_netValue[supplier_netValue["Year"] == 2019].head(10)
top_10_2020 = supplier_netValue[supplier_netValue["Year"] == 2020].head(10)

# create filter element for key figure switch
# chart_measure = pd.DataFrame({"Filter": ["Total Revenue", "Total Volume"]})  # was genau macht das?

app = dash.Dash(__name__)

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
            html.P(children=[
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
    ],
             className="menu"),
    # chart definition
    html.Div(children=[
        html.Div(children=[
            dcc.Graph(id="year-bar-chart", className="card1"),
            dcc.Graph(id="month-line-chart", className="card2")
        ], ),
        html.Div(dcc.Graph(id="PurchasingOrg-bar-chart", className="card3"))
    ],
             className="content")
])


@app.callback(
    [
        Output("year-bar-chart", "figure"),
        Output("month-line-chart", "figure"),
        Output("PurchasingOrg-bar-chart", "figure")
    ],
    [Input("measure-filter", "value")],
)
def update_charts(selected_measure):

    # print(maskPie)

    filtered_dataPie = dataPie.loc[maskPie, :]
    filtered_dataBar = dataBar.loc[maskBar, :]
    filtered_dataLine = dataLine.loc[maskLine, :]
    filtered_dataPie = filtered_dataPie.groupby("Filiale")[["Gesamtumsatz", "Verkaufte Menge",
                                                            "Verkaufsdatum"]].sum().reset_index()
    filtered_dataPie = filtered_dataPie.sort_values(by=["Gesamtumsatz"])
    filtered_dataBar = filtered_dataBar.groupby("Produktkategorie")[[
        "Gesamtumsatz", "Verkaufte Menge", "Verkaufsdatum"
    ]].sum().reset_index()

    format_mapping = {'Gesamtumsatz': '{:,.2f}', 'Verkaufte Menge': '{:,.0f}'}
    for key, value in format_mapping.items():
        filtered_dataBar[key] = filtered_dataBar[key].map(value.format)

    format_mapping = {
        'Gesamtumsatz': '{:,.2f}',
        'Planumsatz': '{:,.2f}',
        'Verkaufte Menge': '{:,.0f}',
        'Verkaufte Menge (PLAN)': '{:,.0f}'
    }
    for key, value in format_mapping.items():
        filtered_dataLine[key] = filtered_dataLine[key].map(value.format)

    if selected_measure == "Gesamtumsatz":
        selected_measure_plan = "Planumsatz"
        name_line = "Revenue"
        name_line_plan = "Planned Revenue"
    else:
        selected_measure_plan = "Verkaufte Menge (PLAN)"
        name_line = "Volume"
        name_line_plan = "Planned Volume"

    pie_chart_figure = {
        "data": [{
            "labels": filtered_dataPie["Filiale"],
            "values": filtered_dataPie[selected_measure],
            "type": "pie",
            "sort": True,
            "direction": "clockwise",
            "marker": {
                "colors": ["#512f1533", "#512f1566", "#512f1599", "#512f15cc", "#512f15ff"]
            }
        }],
        "layout": {
            "title": "Sales by Store",
            "showlegend": False,
            "paper_bgcolor": "#00000000",
            "plot_bgcolor": "#00000000"
        }
    }

    bar_chart_figure = {
        "data": [{
            "x": filtered_dataBar["Produktkategorie"],
            "y": filtered_dataBar[selected_measure],
            "type": "bar",
            "marker": {
                "color": "#512f15"
            },
            "text": filtered_dataBar[selected_measure],
            "textposition": "auto"
        }],
        "layout": {
            "title": "Sales by Product Category",
            "showlegend": False,
            "paper_bgcolor": "#00000000",
            "plot_bgcolor": "#00000000",
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

    line_chart_figure = {
        "data": [{
            "x": filtered_dataLine["Verkaufsdatum"],
            "y": filtered_dataLine[selected_measure],
            "type": "line",
            "name": name_line,
            "line": {
                "width": 4
            },
            "marker": {
                "color": "#512f15"
            },
        }, {
            "x": filtered_dataLine["Verkaufsdatum"],
            "y": filtered_dataLine[selected_measure_plan],
            "type": "line",
            "name": name_line_plan,
            "line": {
                "width": 4
            },
            "marker": {
                "color": "#6c7744"
            },
        }],
        "layout": {
            "title": "Sales by Selling Date",
            "showlegend": False,
            "paper_bgcolor": "#00000000",
            "plot_bgcolor": "#00000000",
        }
    }

    return pie_chart_figure, bar_chart_figure, line_chart_figure


if __name__ == "__main__":
    app.run_server(debug=True)
