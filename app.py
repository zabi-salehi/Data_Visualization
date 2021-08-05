import dash

# initiate dash class, incl. meta tags for mobile responsiveness
app = dash.Dash(__name__, 
    suppress_callback_exceptions=True, 
    meta_tags=[
        {
            "name": "viewport",
            "content": "width=device-width, initial-scale=1.0"
        }
    ]
)

app.title = "here goes the title"

server = app.server