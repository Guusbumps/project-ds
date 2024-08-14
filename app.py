from dash import Dash, dcc, html, Input, Output, callback
import data_wrangling as dw
import plotly.express as px
#import statsmodels

# import data
df = dw.getJoinedNutritionCancerData()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

app.layout = html.Div([
    html.H1('Project Data Science'),
    html.H2('Nutrition and Cancer Dashboard'),
    html.Br(),
    html.Div('Year'),
    dcc.Dropdown(df.Year.unique(),
                 2017,
                 id='dropdown-selection'
    ),
    html.Div(id='display-value'),
    dcc.Graph(id='graph-content')
])


@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value')
)
def update_graph(value):
    dff = df[df.Year == value]
    return px.scatter(dff,
                      x='Data_Value',
                      y='Age-adjusted Death Rate',
                      color='Question',
                      hover_data=list(dff.columns),
                      trendline="ols"
                      )


if __name__ == '__main__':
    app.run(debug=True)