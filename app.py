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
    html.Div('Stratification category'),
    dcc.Dropdown(df.StratificationCategory1.unique(),
                 'Total',
                 id='dropdown-selection'
    ),
    dcc.Checklist(
        ['Show labels'],
        ['Show labels'],
        id='checkbox'
    ),
    html.Div(id='display-value'),
    dcc.Graph(id='graph-content')
])


@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value'),
    Input('checkbox', 'value')
)
def update_graph(dropdown_value, checkbox_value):
    dff = df[df.StratificationCategory1 == dropdown_value]
    fig = px.scatter(dff,
                      x='Data_Value',
                      y='Age-adjusted Death Rate',
                      color='Question',
                      facet_col='Stratification1', facet_col_wrap=3,
                      text='StateAbbr' if checkbox_value == ["Show labels"] else None,
                      hover_data=list(dff.columns),
                      trendline="ols"
                      )
    fig.update_traces(textposition='top center')
    return fig


if __name__ == '__main__':
    app.run(debug=True)