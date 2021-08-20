import datetime
from datetime import date
from datetime import datetime as dt
from re import M
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
    {'label': 'All', 'value': 'All'},
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
    {'label': 'All', 'value': 'All'},
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

options_material_group = [{'label': 'All', 'value': 'All'}, {'label': '4017', 'value': '4017'}, {'label': '4245', 'value': '4245'}, {'label': '4047', 'value': '4047'}, {'label': '4015', 'value': '4015'}, {'label': 'C14A', 'value': 'C14A'}, {'label': 'C2AA', 'value': 'C2AA'}, {'label': '3526', 'value': '3526'}, {'label': '3381', 'value': '3381'}, {'label': '3295', 'value': '3295'}, {'label': 'C18K', 'value': 'C18K'}, {'label': 'C13D', 'value': 'C13D'}, {'label': 'C12B', 'value': 'C12B'}, {'label': 'C12E', 'value': 'C12E'}, {'label': 'C12K', 'value': 'C12K'}, {'label': 'C17A', 'value': 'C17A'}, {'label': 'C18L', 'value': 'C18L'}, {'label': 'C12C', 'value': 'C12C'}, {'label': '4073', 'value': '4073'}, {'label': '4072', 'value': '4072'}, {'label': 'C21A', 'value': 'C21A'}, {'label': '3521', 'value': '3521'}, {'label': '3171', 'value': '3171'}, {'label': '9998', 'value': '9998'}, {'label': '3522', 'value': '3522'}, {'label': '3499', 'value': '3499'}, {'label': 'C18C', 'value': 'C18C'}, {'label': 'C12G', 'value': 'C12G'}, {'label': 'C12A', 'value': 'C12A'}, {'label': 'C3DA', 'value': 'C3DA'}, {'label': 'C12F', 'value': 'C12F'}, {'label': '3491', 'value': '3491'}, {'label': 'C26A', 'value': 'C26A'}, {'label': 'Q224', 'value': 'Q224'}, {'label': 'C3AA', 'value': 'C3AA'}, {'label': 'C18P', 'value': 'C18P'}, {'label': '2611', 'value': '2611'}, {'label': 'C35A', 'value': 'C35A'}, {'label': '4269', 'value': '4269'}, {'label': 'C13J', 'value': 'C13J'}, {'label': 'C48A', 'value': 'C48A'}, {'label': 'C45E', 'value': 'C45E'}, {'label': '2645', 'value': '2645'}, {'label': '2522', 'value': '2522'}, {'label': 'C15A', 'value': 'C15A'}, {'label': 'C2GA', 'value': 'C2GA'}, {'label': 'C112', 'value': 'C112'}, {'label': 'C31A', 'value': 'C31A'}, {'label': '3523', 'value': '3523'}, {'label': '4233', 'value': '4233'}, {'label': 'C45M', 'value': 'C45M'}, {'label': '2616', 'value': '2616'}, {'label': 'C41P', 'value': 'C41P'}, {'label': 'C45F', 'value': 'C45F'}, {'label': 'C13H', 'value': 'C13H'}, {'label': 'C18M', 'value': 'C18M'}, {'label': 'C12H', 'value': 'C12H'}, {'label': 'D70A', 'value': 'D70A'}, {'label': 'C3EA', 'value': 'C3EA'}, {'label': '3493', 'value': '3493'}, {'label': 'C41S', 'value': 'C41S'}, {'label': 'C12D', 'value': 'C12D'}, {'label': '5211', 'value': '5211'}, {'label': 'C2EA', 'value': 'C2EA'}, {'label': 'C3CA', 'value': 'C3CA'}, {'label': 'C2KA', 'value': 'C2KA'}, {'label': 'C50A', 'value': 'C50A'}, {'label': 'C111', 'value': 'C111'}, {'label': 'C2BA', 'value': 'C2BA'}, {'label': '4071', 'value': '4071'}, {'label': 'D41A', 'value': 'D41A'}, {'label': '3525', 'value': '3525'}, {'label': 'C41B', 'value': 'C41B'}, {'label': 'M726', 'value': 'M726'}, {'label': 'D111', 'value': 'D111'}, {'label': 'C29A', 'value': 'C29A'}, {'label': 'C18B', 'value': 'C18B'}, {'label': 'C13N', 'value': 'C13N'}, {'label': 'H200', 'value': 'H200'}, {'label': '2021', 'value': '2021'}, {'label': 'D23E', 'value': 'D23E'}, {'label': 'C13S', 'value': 'C13S'}, {'label': 'C18G', 'value': 'C18G'}, {'label': '3395', 'value': '3395'}, {'label': '4272', 'value': '4272'}, {'label': 'C41D', 'value': 'C41D'}, {'label': 'C41N', 'value': 'C41N'}, {'label': '3524', 'value': '3524'}, {'label': 'C18J', 'value': 'C18J'}, {'label': 'C13A', 'value': 'C13A'}, {'label': 'C18D', 'value': 'C18D'}, {'label': 'C13B', 'value': 'C13B'}, {'label': 'C41L', 'value': 'C41L'}, {'label': 'D35A', 'value': 'D35A'}, {'label': 'PC10', 'value': 'PC10'}, {'label': 'C41H', 'value': 'C41H'}, {'label': 'C15C', 'value': 'C15C'}, {'label': 'D25B', 'value': 'D25B'}, {'label': 'C39A', 'value': 'C39A'}, {'label': 'C13Q', 'value': 'C13Q'}, {'label': '5155', 'value': '5155'}, {'label': 'C41A', 'value': 'C41A'}, {'label': 'C41K', 'value': 'C41K'}, {'label': '2161', 'value': '2161'}, {'label': '5121', 'value': '5121'}, {'label': 'C2HA', 'value': 'C2HA'}, {'label': 'GD10', 'value': 'GD10'}, {'label': '4229', 'value': '4229'}, {'label': 'C41M', 'value': 'C41M'}, {'label': '4039', 'value': '4039'}, {'label': '2113', 'value': '2113'}, {'label': 'C13L', 'value': 'C13L'}, {'label': '2167', 'value': '2167'}, {'label': 'D23D', 'value': 'D23D'}, {'label': '2551', 'value': '2551'}, {'label': 'C44A', 'value': 'C44A'}, {'label': 'C41C', 'value': 'C41C'}, {'label': 'E22F', 'value': 'E22F'}, {'label': '4241', 'value': '4241'}, {'label': 'D80B', 'value': 'D80B'}, {'label': 'C18A', 'value': 'C18A'}, {'label': 'C45J', 'value': 'C45J'}, {'label': 'C47A', 'value': 'C47A'}, {'label': 'M720', 'value': 'M720'}, {'label': 'C60A', 'value': 'C60A'}, {'label': '4483', 'value': '4483'}, {'label': 'C2FT', 'value': 'C2FT'}, {'label': 'M722', 'value': 'M722'}, {'label': '2613', 'value': '2613'}, {'label': '4257', 'value': '4257'}, {'label': '4213', 'value': '4213'}, {'label': 'C41F', 'value': 'C41F'}, {'label': '4235', 'value': '4235'}, {'label': '2631', 'value': '2631'}, {'label': '3494', 'value': '3494'}, {'label': '4001', 'value': '4001'}, {'label': '2131', 'value': '2131'}, {'label': 'C17B', 'value': 'C17B'}, {'label': 'D120', 'value': 'D120'}, {'label': '5199', 'value': '5199'}, {'label': '5191', 'value': '5191'}, {'label': '2211', 'value': '2211'}, {'label': 'D70C', 'value': 'D70C'}, {'label': '4215', 'value': '4215'}, {'label': 'D23B', 'value': 'D23B'}, {'label': '4053', 'value': '4053'}, {'label': 'C22A', 'value': 'C22A'}, {'label': '4059', 'value': '4059'}, {'label': '2641', 'value': '2641'}, {'label': '4225', 'value': '4225'}, {'label': '5061', 'value': '5061'}, {'label': '3165', 'value': '3165'}, {'label': '4021', 'value': '4021'}, {'label': 'D70F', 'value': 'D70F'}, {'label': '2627', 'value': '2627'}, {'label': '3423', 'value': '3423'}, {'label': 'C41E', 'value': 'C41E'}, {'label': '4237', 'value': '4237'}, {'label': 'E31A', 'value': 'E31A'}, {'label': '4027', 'value': '4027'}, {'label': '2624', 'value': '2624'}, {'label': '4203', 'value': '4203'}, {'label': '4051', 'value': '4051'}, {'label': 'D23A', 'value': 'D23A'}, {'label': '4248', 'value': '4248'}]

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
    #navigation block
    # html.Div(children=[
        
      
    #     html.Div(children = [
    #         html.Div(children = 'Net Value or Number of Orders', className ="menu-title"),
    #         dcc.Dropdown(
    #             id = 'os-nof',
    #             options=[
    #                 {"label": "Net Value", "value": "net_value"},
    #                 {"label": "Number of orders", "value": "number_of_orders"},
    #             ],
    #             value="net_value",
    #             searchable = True,
    #             className="dropdown"

    #         )
    #     ]
    #     # ),
    #     # html.Div(children=[
    #     #     html.Div(children="Daterange", className ="menu-title"),
    #     #     dcc.DatePickerRange(
    #     #         id='date_range',
    #     #         min_date_allowed = dt(2019,1,1),
    #     #         max_date_allowed = dt(2020,6,30),
    #     #         initial_visible_month = dt(2019,1,1),
    #     #         end_date = dt(2020,6,30)
    #     #     )
    #     # ])
    # ],
    #          className="menu"),
    html.Div(children= [
        html.H3("Performance Indicators:", className ="pi-title"),
        html.H3("Filterbar:", className ="filterbar-title")
    ], className = "menu-title"),
    # filterblock unter navigationblock
    html.Div(children=[
        html.Div(children = [

            html.Div(children = 'Net Value or Number of Orders', className ="filter-title"),
            dcc.Dropdown(
                id = 'os-nof',
                options=[
                    {"label": "Net Value", "value": "net_value"},
                    {"label": "Number of orders", "value": "number_of_orders"},
                ],
                value="net_value",
                searchable = True,
        ) 
        ],  className = "dropdown"
        ),
        html.Div(children = [
            html.Div(children="Filter for Purchasing Org.", className ='filter-title'),
            dcc.Dropdown(
                id = 'purchasing_organisation_dropdown',
                options =   options_einkauforg,
                value=['All'],
                searchable = True,
                multi = True,
                className="dropdown",
                persistence_type = "local"
            )], className = 'dropdown'),
        # ], className = "dropdown"
        #     [
        #     dcc.Checklist(
        #         id="all-einkaufsorg-checklist",
        #         options=[{"label": "All", "value": "All"}],
        #         value=["All"],
        #         labelStyle={"display": "inline-block"},
        #     ),
        #     dcc.Checklist(
        #         id="einkaufsorg-checklist",
        #         options=options_einkauforg,
        #         value=[],
        #         labelStyle={"display": "inline-block"},
        #     ),
        #     ], className = "dropdown"
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

        html.Div(children = [
            html.Div(children= "Filter for Material Group", className ='filter-title'),
            dcc.Dropdown(
                id = 'material_group_dropdown',
                options =   options_material_group,
                value="All",
                searchable = True,
                multi = True,
                className="dropdown",
                persistence_type = "local"
            ),     
        ], className = "dropdown"
        ),
        html.Div(children = [
            html.Div(children="Filter for plants", className ='filter-title'),
            dcc.Dropdown(
                id = 'plants_dropdown',
                options = options_werke,
                value=['All'],
                searchable = True,
                multi = True,
                className="dropdown",
                persistence_type = "local"
            ),
        ], className='dropdown'
        )
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
    [Input("os-nof", "value"),
    Input("company_code_dropdown", "value"),
    Input("material_group_dropdown", "value"),
    Input("purchasing_organisation_dropdown", "value"),
    Input("plants_dropdown", "value")
    ],

)

def update_charts(os_nof_value, cc_value, mg_value, po_value, pl_value):

    # Anpassung der Daten je nach Auswahl

    ctx = dash.callback_context
    global data
    data_temp = data.copy()
    all_cc = ['52','53','54']
    benoetigte_cc = [int(i) for i in all_cc if i in cc_value]

    data_temp = data[data["Company Code"].isin(benoetigte_cc)]


    
    if "All" not in mg_value:

        all_mg = ['4017', '4245', '4047', '4015', 'C14A', 'C2AA', '3526', '3381',
        '3295', 'C18K', 'C13D', 'C12B', 'C12E', 'C12K', 'C17A', 'C18L',
        'C12C', '4073', '4072', 'C21A', '3521', '3171', '9998', '3522',
        '3499', 'C18C', 'C12G', 'C12A', 'C3DA', 'C12F', '3491', 'C26A',
        'Q224', 'C3AA', 'C18P', '2611', 'C35A', '4269', 'C13J', 'C48A',
        'C45E', '2645', '2522', 'C15A', 'C2GA', 'C112', 'C31A', '3523',
        '4233', 'C45M', '2616', 'C41P', 'C45F', 'C13H', 'C18M', 'C12H',
        'D70A', 'C3EA', '3493', 'C41S', 'C12D', '5211', 'C2EA', 'C3CA',
        'C2KA', 'C50A', 'C111', 'C2BA', '4071', 'D41A', '3525', 'C41B',
        'M726', 'D111', 'C29A', 'C18B', 'C13N', 'H200', '2021', 'D23E',
        'C13S', 'C18G', '3395', '4272', 'C41D', 'C41N', '3524', 'C18J',
        'C13A', 'C18D', 'C13B', 'C41L', 'D35A', 'PC10', 'C41H', 'C15C',
        'D25B', 'C39A', 'C13Q', '5155', 'C41A', 'C41K', '2161', '5121',
        'C2HA', 'GD10', '4229', 'C41M', '4039', '2113', 'C13L', '2167',
        'D23D', '2551', 'C44A', 'C41C', 'E22F', '4241', 'D80B', 'C18A',
        'C45J', 'C47A', 'M720', 'C60A', '4483', 'C2FT', 'M722', '2613',
        '4257', '4213', 'C41F', '4235', '2631', '3494', '4001', '2131',
        'C17B', 'D120', '5199', '5191', '2211', 'D70C', '4215', 'D23B',
        '4053', 'C22A', '4059', '2641', '4225', '5061', '3165', '4021',
        'D70F', '2627', '3423', 'C41E', '4237', 'E31A', '4027', '2624',
        '4203', '4051', 'D23A', '4248']

        benoetigte_mg = [i for i in all_mg if i in mg_value]

        data_temp = data_temp[data_temp["Material Group"].isin(benoetigte_mg)]

    if "All" not in pl_value:
        all_pl = ['51', '5899', '61', '77', '78', '62', '3799', '9699', '6599']
        benoetigte_pl = [int(i) for i in all_pl if i in pl_value]
        data_temp = data_temp[data_temp["Plant"].isin(benoetigte_pl)]

        
        


    if "All" not in po_value:
        all_po = ['5200', '5210', '5400', '5410', '5420', '5310', '5320', '54']
        benoetigte_po = [int(i) for i in all_po if i in po_value]
        data_temp = data_temp[data_temp["Purchasing Org."].isin(benoetigte_po)]

    

    # Datenvorbereitung:

    orderedSpend_year = data_temp.groupby(["Year"])[["Net Value"]].sum().reset_index()

    data_2019 = data_temp[data_temp["Year"] == 2019]
    data_2020 = data_temp[data_temp["Year"] == 2020]

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



    supplier_netValue = data_temp.groupby(["Year",
                                    "Supplier name"])[["Net Value"]].sum().reset_index().sort_values(by="Net Value",
                                                                                                    ascending=False)
    top10_2019 = data_2019.groupby(["Supplier name"])[["Net Value"
                                                    ]].sum().reset_index().sort_values(by="Net Value",
                                                                                        ascending=False).head(10)
    top10_2020 = data_2020.groupby(["Supplier name"])[["Net Value"
                                                    ]].sum().reset_index().sort_values(by="Net Value",
                                                                                        ascending=False).head(10)

    # temp = ctx.triggered

    # print(ctx.triggered)

    # if temp[0]['prop_id'] == 'os-nof.value':
    #     numeric_chart_figure, bar_chart_figure1, line_chart_figure, bar_chart_figure2, bar_chart_figure4 = update_chart_os_nof(temp[0]['value'])

    # elif temp[0]['prop_id'] == 'company_code_dropdown.value':
    #     numeric_chart_figure, bar_chart_figure1, line_chart_figure, bar_chart_figure2, bar_chart_figure4 = update_chart_cc(temp[0]['value'])
    
    # elif temp[0]['prop_id'] == 'material_group_dropdown.value':
    #     numeric_chart_figure, bar_chart_figure1, line_chart_figure, bar_chart_figure2, bar_chart_figure4 = update_chart_mg(temp[0]['value'])
    
    #else:
    #   numeric_chart_figure, bar_chart_figure1, line_chart_figure, bar_chart_figure2, bar_chart_figure4 = None, None, None, None, None 
    
    if data_temp.empty:
         # Fehlermeldung reinschreiben
        # plot_bgcolor = colors["plot_bgcolor"]
            
        if os_nof_value == "Net Value":
            
            fig = go.Figure()

            fig.add_trace(go.Indicator(
                mode = "number",
                
                value = 0,
                number = {'prefix': ""},
                delta = {'position': "top", 'reference': 320},
                title = {'text': 'Ordered spend 2019'},
                domain = {'row':0, 'column': 0}))

            fig.add_trace(go.Indicator(
                mode = "number",
                value = 0,
                number = {'prefix': ""},
                delta = {'position': "top", 'reference': 320},
                title = {'text': 'Ordered spend 2020'},
                domain = {'row':1, 'column': 0}))

            fig.update_layout(
                grid = {'rows':2, 'columns': 1},
                paper_bgcolor = colors["paper_bgcolor"],)

            bar_chart_figure1 = {
                'data': [
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
                ],
                "layout": {
                    "title": "Net Value per Month",
                    "showlegend": False,
                    "paper_bgcolor": colors["paper_bgcolor"],
                    "plot_bgcolor": colors["plot_bgcolor"]
                }
            }

        else:
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
                ],
                "layout": {
                    "title": "Number of Orders per Month",
                    "showlegend": False,
                    "paper_bgcolor": colors["paper_bgcolor"],
                    "plot_bgcolor": colors["plot_bgcolor"]
                }
            }

        # bar chart 2: Aufgabe 5, Teil 1: 2019

        bar_chart_figure2 = {
            "data": [],
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

        bar_chart_figure4 = {"data": [],
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

    else:

        if os_nof_value == "net_value":

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

        else:

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


if __name__ == "__main__":
    app.run_server(debug=True)
