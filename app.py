from dash import Dash, dcc, html, Input, Output, callback
import data_wrangling as dw
import plotly.express as px
#import statsmodels

# import data
df = dw.getJoinedNutritionCancerData()
df2 = dw.getJoinedNutritionCancerSiteData()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

app.layout = html.Div([
    html.H1('Project Data Science'),
    html.H2('Nutrition and Cancer Dashboard'),
    dcc.Tabs([
        dcc.Tab(label='Population stratification', children=[
            html.Div('Cancer site'),
            dcc.Dropdown(df2['Cancer Sites'].unique(),
                         'All Cancer Sites Combined',
                         id='dropdown-selection-site'
                         ),
            html.Div('Year'),
            dcc.Dropdown(df2['Year'].unique(),
                         2017,
                         id='dropdown-selection-year'
                         ),
            html.Div('Stratification categoy'),
            dcc.Dropdown(df2['StratificationCategory1'].unique(),
                         'Total',
                         id='dropdown-selection-strat'
                         ),
            dcc.Checklist(
                ['Show labels'],
                ['Show labels'],
                id='checkbox2'
            ),
            dcc.Graph(id='stratification-graph-content')
            ]),
        dcc.Tab(label='Cancer sites', children=[
            html.Div('Year'),
            dcc.Dropdown(df2['Year'].unique(),
                         2017,
                         id='dropdown-selection-year2'
                         ),
            dcc.Checklist(
                ['Show labels'],
                ['Show labels'],
                id='checkbox3'
            ),
            html.Div('Cancer sites shown'),
            dcc.Checklist(
                df2[df2['StratificationCategory1'] == "Total"].groupby('Cancer Sites')['Age-Adjusted Rate'].mean().sort_values(ascending=False).index.tolist(),
                ['Digestive System', 'Respiratory System', 'Lung and Bronchus'],
                inline=True,
                id='checklist_sites'
            ),
            dcc.Graph(id='cancersites-graph-content')
            ])
        ])
    ])


@callback(
    Output('stratification-graph-content', 'figure'),
    Input('dropdown-selection-site', 'value'),
    Input('dropdown-selection-year', 'value'),
    Input('dropdown-selection-strat', 'value'),
    Input('checkbox2', 'value')
)
def update_stratification_graph(dropdown_site, dropdown_year, dropdown_strat, checkbox_value):
    dff2 = df2[df2['Cancer Sites'] == dropdown_site]
    dff2 = dff2[dff2['Year'] == dropdown_year]
    dff2 = dff2[dff2['StratificationCategory1'] == dropdown_strat]
    fig = px.scatter(dff2,
                     x='Data_Value',
                     y='Age-Adjusted Rate',
                     color='Question',
                     color_discrete_map={
                         "Percent of adults who report consuming fruit less than one time daily": "red",
                         "Percent of adults who report consuming vegetables less than one time daily": "blue",
                     },
                     text='StateAbbr' if checkbox_value == ["Show labels"] else None,
                     facet_col='Stratification1', facet_col_wrap=3,
                     hover_data=list(dff2.columns),
                     trendline="ols"
                     )
    fig.update_traces(textposition='top center')
    return fig


@callback(
    Output('cancersites-graph-content', 'figure'),
    Input('dropdown-selection-year2', 'value'),
    Input('checkbox3', 'value'),
    Input('checklist_sites', 'value')
)
def update_cancersites_graph(dropdown_year, checkbox_value, checklist_sites_value):
    dff2 = df2[df2['Year'] == dropdown_year]
    dff2 = dff2[dff2['StratificationCategory1'] == "Total"]
    dff2 = dff2[dff2['Cancer Sites'].isin(checklist_sites_value)]
    fig = px.scatter(dff2,
                     x='Data_Value',
                     y='Age-Adjusted Rate',
                     color='Question',
                     color_discrete_map={
                         "Percent of adults who report consuming fruit less than one time daily": "red",
                         "Percent of adults who report consuming vegetables less than one time daily": "blue",
                     },
                     text='StateAbbr' if checkbox_value == ["Show labels"] else None,
                     facet_col='Cancer Sites', facet_col_wrap=4,
                     hover_data=list(dff2.columns),
                     trendline="ols"
                     )
    fig.update_traces(textposition='top center')
    return fig


if __name__ == '__main__':
    app.run(debug=True)