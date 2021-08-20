import plotly.graph_objects as go

fig = go.Figure()
fig.add_trace(go.Indicator(
    mode = "number",
    value = 400,
    number = {'prefix': ""},
    delta = {'position': "top", 'reference': 320},
    title = {'text': 'Ordered spend 2019'},
    domain = {'row':0, 'column': 0}))

fig.add_trace(go.Indicator(
    mode = "number",
    value = 400,
    number = {'prefix': ""},
    delta = {'position': "top", 'reference': 320},
    title = {'text': 'Ordered spend 2020'},
    domain = {'row':1, 'column': 0}))



fig.update_layout(
    grid = {'rows':2, 'columns': 1},
    paper_bgcolor = "lightgray")

fig.show()