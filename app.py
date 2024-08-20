from dash import Dash, dcc, html, Input, Output, callback
import data_wrangling as dw
import plotly.express as px

# import data
df_strat = dw.getJoinedNutritionCancerData()  # data for all cancer sites combined, stratified by Sex and Race/Ethnicity
df_sites = dw.getJoinedNutritionCancerSitesData()  # data per cancer site, for whole population

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

# define layout of dashboard
app.layout = html.Div([
    html.H2('Project Data Science - Nutrition and Cancer Dashboard'),
    html.Div('Guus Spenkelink - 2056061 - 2023/2024'),
    dcc.Tabs([
        dcc.Tab(label='Population stratification', children=[
            html.Div([
                html.Div([
                    html.Div('Year'),
                    dcc.Dropdown(df_strat['Year'].unique(),
                                 2017,
                                 id='dropdown-selection-year'
                                 )
                        ],
                    style={'width': '49%', 'display': 'inline-block'}
                ),
                html.Div([
                    html.Div('Stratification category'),
                    dcc.Dropdown(df_strat['StratificationCategory1'].unique(),
                                 'Total',
                                 id='dropdown-selection-strat'
                                 )
                    ],
                    style={'width': '49%', 'display': 'inline-block'}
                )],
            ),
            dcc.Checklist(
                ['Show labels'],
                ['Show labels'],
                id='checkbox2'
            ),
            dcc.Checklist(
                ['Fix Y-axis'],
                [],
                id='checkbox_yaxis1'
            ),
            dcc.Graph(id='stratification-graph-content')
            ]),
        dcc.Tab(label='Cancer sites', children=[
            html.Div('Year'),
            dcc.Dropdown(df_sites['Year'].unique(),
                         2017,
                         id='dropdown-selection-year2'
                         ),
            dcc.Checklist(
                ['Show labels'],
                [],
                id='checkbox3'
            ),
            dcc.Checklist(
                ['Fix Y-axis'],
                [],
                id='checkbox_yaxis2'
            ),
            html.Br(),
            html.Details([
                html.Summary(
                    html.B('Click here to select cancer sites, listed in descending order by associated death rate')
                ),
                dcc.Checklist(
                    df_sites[df_sites['StratificationCategory1'] == "Total"].groupby('Leading Cancer Sites')['Age-Adjusted Rate'].mean().sort_values(ascending=False).index.tolist(),
                    ['Lung and Bronchus', 'Prostate', 'Colon and Rectum'],
                    inline=True,
                    id='checklist_sites'
                ),
            ]),
            dcc.Graph(id='cancersites-graph-content')
            ])
        ])
    ])

# callbacks and update function for graph in first tab (population stratification, all cancer sites combined)
@callback(
    Output('stratification-graph-content', 'figure'),
    Input('dropdown-selection-year', 'value'),
    Input('dropdown-selection-strat', 'value'),
    Input('checkbox2', 'value'),
    Input('checkbox_yaxis1', 'value')
)
def update_stratification_graph(dropdown_year, dropdown_strat, checkbox_value, checkbox_yaxis_value):
    dff = df_strat[df_strat['Cancer Sites'] == "All Cancer Sites Combined"]
    dff = dff[dff['Year'] == dropdown_year]
    dff = dff[dff['StratificationCategory1'] == dropdown_strat]
    fig = px.scatter(dff,
                     x='Data_Value',
                     y='Age-Adjusted Rate',
                     color='Question',
                     color_discrete_map={
                         "Percent of adults who report consuming fruit less than one time daily": "red",
                         "Percent of adults who report consuming vegetables less than one time daily": "blue",
                     },
                     text='StateAbbr' if checkbox_value == ["Show labels"] else None,
                     facet_col='Stratification1', facet_col_wrap=3,
                     hover_data=list(dff.columns),
                     trendline="ols",
                     labels={
                         "Data_Value": "Percentage (see legend)",
                         "Age-Adjusted Rate": "Age-Adjusted Death Rate",
                         "Stratification1": "Stratification"
                     },
                     title='Death rate (per 100,000) caused by cancer per US state <br>versus fruit and vegetable consumption, all cancer sites combined'
                     )
    fig.update_traces(textposition='top center')
    if checkbox_yaxis_value != ['Fix Y-axis']:
        fig = fig.update_yaxes(matches=None, showticklabels=True)
    return fig


# callbacks and update function for graph in second tab (data per cancer site)
@callback(
    Output('cancersites-graph-content', 'figure'),
    Input('dropdown-selection-year2', 'value'),
    Input('checkbox3', 'value'),
    Input('checkbox_yaxis2', 'value'),
    Input('checklist_sites', 'value')
)
def update_cancersites_graph(dropdown_year, checkbox_value, checkbox_yaxis_value, checklist_sites_value):
    dff = df_sites[df_sites['Year'] == dropdown_year]
    dff = dff[dff['StratificationCategory1'] == "Total"]
    dff = dff[dff['Leading Cancer Sites'].isin(checklist_sites_value)]
    fig = px.scatter(dff,
                     x='Data_Value',
                     y='Age-Adjusted Rate',
                     color='Question',
                     color_discrete_map={
                         "Percent of adults who report consuming fruit less than one time daily": "red",
                         "Percent of adults who report consuming vegetables less than one time daily": "blue",
                     },
                     text='StateAbbr' if checkbox_value == ["Show labels"] else None,
                     facet_col='Leading Cancer Sites', facet_col_wrap=4,
                     hover_data=list(dff.columns),
                     trendline="ols",
                     labels={
                         "Data_Value": "Percentage (see legend)",
                         "Age-Adjusted Rate": "Age-Adjusted Death Rate",
                         "Leading Cancer Sites": "Cancer site"
                     },
                     title='Death rate (per 100,000) per (leading) cancer site per US state versus fruit and vegetable consumption'
                     )
    fig.update_traces(textposition='top center')
    if checkbox_yaxis_value != ['Fix Y-axis']:
        fig = fig.update_yaxes(matches=None, showticklabels=True)
    return fig


if __name__ == '__main__':
    app.run(debug=True)