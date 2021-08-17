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
orderdSpend_purchOrg_2019["Purchasing Org."] = orderdSpend_purchOrg_2019["Purchasing Org."].apply(lambda x: str(x))
orderdSpend_purchOrg_2020["Purchasing Org."] = orderdSpend_purchOrg_2020["Purchasing Org."].apply(lambda x: str(x))
numbOrders_purchOrg_2019["Purchasing Org."] = numbOrders_purchOrg_2019["Purchasing Org."].apply(lambda x: str(x))
numbOrders_purchOrg_2020["Purchasing Org."] = numbOrders_purchOrg_2020["Purchasing Org."].apply(lambda x: str(x))

supplier_netValue = data.groupby(["Year",
                                  "Supplier name"])[["Net Value"]].sum().reset_index().sort_values(by="Net Value",
                                                                                                   ascending=False)
top10_2019 = data_2019.groupby(["Supplier name"])[["Net Value"
                                                   ]].sum().reset_index().sort_values(by="Net Value",
                                                                                      ascending=False).head(10)
top10_2020 = data_2020.groupby(["Supplier name"])[["Net Value"
                                                   ]].sum().reset_index().sort_values(by="Net Value",
                                                                                      ascending=False).head(10)
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
        html.Div(children=[
            html.Div(children="Date", className="menu-title"),
            dcc.Dropdown(id="date",
                         options=[{
                             "label": "2020",
                             "value": "2020"
                         }, {
                             "label": "2019",
                             "value": "2019"
                         }],
                         value="Year",
                         searchable=False,
                         clearable=False,
                         className="dropdown"),
        ])
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

    bar_chart_figure1 = {
        'data': [
            {
                'x': orderdSpend_purchOrg_2020["Purchasing Org."],
                'y': orderdSpend_purchOrg_2020["Net Value"],
                'type': 'bar',
                'name': 'SF'
            },
            {
                'x': orderdSpend_purchOrg_2019["Purchasing Org."],
                'y': orderdSpend_purchOrg_2019["Net Value"],
                'type': 'bar',
                'name': u'Montréal'
            },
        ],
        "layout": {
            "title": "Sales by Store",
            "showlegend": False,
            "paper_bgcolor": "#00000000",
            "plot_bgcolor": "#00000000"
        }
    }

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
            "title": "Sales by Selling Date",
            "showlegend": False,
            "paper_bgcolor": "#00000000",
            "plot_bgcolor": "#00000000",
        }
    }

    return line_chart_figure


if __name__ == "__main__":
    app.run_server(debug=True)
