import dash_html_components as html
import pandas as pd
import dash
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_table
import base64
svg_file = "demo.svg"
encoded = base64.b64encode(open(svg_file,'rb').read()) 
svg = 'data:image/svg+xml;base64,{}'.format(encoded.decode()) 


df = pd.read_csv('88season.csv')
df['team'] = df['team'].replace("Celtics", "Cripples")
df_team = df.groupby('team').sum()
df_team['num_games'] = df.groupby('team')['game_id'].nunique()
for x in df_team.columns[1:14]:
    df_team[x] = (df_team[x]/df_team['num_games']).round(2)
df_team_avg = df_team[df_team.columns[1:14]].reset_index()
per36 = df.columns[3:16].tolist()
adv_df = pd.read_csv('88advanced.csv')

important_cols = ['Player'] + df.columns[2:16].tolist()


def getPer36(df):
    for x in per36:
        df[x] = ((df[x]/df['MIN'])*36).round(2)
    return df


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = 'DASL Stats'

app.layout = html.Div(children=[
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

index_page = html.Div(children=[
    html.Div(className='topnav', children=[
        html.Img(src=svg),
        dcc.Link('Per 36 stats', href='/per36'),
        dcc.Link('Advanced Stats', href='/advanced'),
        dcc.Link('League Leaders', href='/league_leaders')
    ])
]),


per36_layout = html.Div(children=[
    html.Div(className='topnav', children=[
        html.Img(src=svg),
        dcc.Link('Per 36 stats', href='/per36'),
        dcc.Link('Advanced Stats', href='/advanced'),
        dcc.Link('League Leaders', href='/league_leaders')
    ]),
    html.H4(children='Per 36 Stats'),
    dcc.Dropdown(
        id='team-select',
        style={
            'color': 'black',
            'width': '50%',
            'fontSize': '20px',
        },
        options=[
            {'label': team, 'value': team}
            for team in sorted(df['team'].unique())
        ]
    ),
    dash_table.DataTable(
        id='table',
        sort_action='native',
        style_table={'width': '80%'},
        style_header={'backgroundColor': 'rgb(30, 30, 30)',
                        'color': 'white'},
        style_cell_conditional=[
            {
                'if': {'column_id': c},
                'textAlign': 'left'
            } for c in ['Date', 'Region']
        ],
    style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
            }
        ],
    style_cell={'fontFamily': 'cursive'}
    ),
])

advanced_layout = html.Div(children=[
    html.Div(className='topnav', children=[
        html.Img(src=svg),
        dcc.Link('Per 36 stats', href='/per36'),
        dcc.Link('Advanced Stats', href='/advanced'),
        dcc.Link('League Leaders', href='/league_leaders')
    ]),
    html.H4(children='Advanced Stats'),
    dcc.Dropdown(
        id='adv-team-select',
        style={
            'color': 'black',
            'width': '50%',
            'fontSize': '20px',
        },
        options=[
            {'label': team, 'value': team}
            for team in sorted(df['team'].unique())
        ]
    ),
    dash_table.DataTable(
        id='advanced-table',
        sort_action='native',
        style_table={
            'width': '80%',
            'borderRadius': '25px',
        },
        style_header={'backgroundColor': 'rgb(30, 30, 30)',
                        'color': 'white'},
        style_cell_conditional=[
            {
                'if': {'column_id': c},
                'textAlign': 'left'
            } for c in ['Date', 'Region']
        ],
    style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
            }
        ],
    style_cell={'fontFamily': 'cursive'}
    ),
])

ll_layout = html.Div(children=[
    html.Div(className='topnav', children=[
        html.Img(src=svg),
        dcc.Link('Per 36 stats', href='/per36'),
        dcc.Link('Advanced Stats', href='/advanced'),
        dcc.Link('League Leaders', href='/league_leaders')
    ]),
    html.H3("Select Minutes Qualifier"),
    dcc.Slider(
        className="slider",
        id="qualifier",
        min=0,
        max= int(adv_df["MIN_player"].max())+1,
        step=20,
        marks={ i:str(i) for i in range(0, int(adv_df["MIN_player"].max())+1, 100)},
        value=100,
    ), 
    html.H2("True Shooting Leaders"),
    dash_table.DataTable(
        id='test',
        columns=[{'name': i, 'id': i} for i in ['Player','team','TS%']],
        style_cell={'minWidth': '40px', 'width': '40px', 'maxWidth': '40px', 'whitespace': 'normal'},
        style_table={
            'width': "50%",
            'margin': 'auto'
        }
    ),
    html.Br(),
    html.H2("Usage Leaders"),
    dash_table.DataTable(
        id='usage-table',
        columns=[{'name': i, 'id': i} for i in ['Player','team','Usage']],
        style_cell={'minWidth': '40px', 'width': '40px', 'maxWidth': '40px', 'whitespace': 'normal'},
        style_table={
            'width': "50%",
            'margin': 'auto'
        }
    ),
    html.Br(),
    html.H2("Floor Percentage Leaders"),
    dash_table.DataTable(
        id='floor-table',
        columns=[{'name': i, 'id': i} for i in ['Player','team','Floor Percentage']],
        style_cell={'minWidth': '40px', 'width': '40px', 'maxWidth': '40px', 'whitespace': 'normal'},
        style_table={
            'width': "50%",
            'margin': 'auto'
        }
    ),
    html.Br(),
    html.H2("Scoring Possessions Leaders"),
    dash_table.DataTable(
        id='sposs-table',
        columns=[{'name': i, 'id': i} for i in ['Player','team','Scoring Possessions']],
        style_cell={'minWidth': '40px', 'width': '40px', 'maxWidth': '40px', 'whitespace': 'normal'},
        style_table={
            'width': "50%",
            'margin': 'auto'
        }
    ),
    html.Br(),
    html.H2("Possessions Leaders"),
    dash_table.DataTable(
        id='poss-table',
        columns=[{'name': i, 'id': i} for i in ['Player','team','Possessions']],
        style_cell={'minWidth': '80px', 'width': '80px', 'maxWidth': '80px', 'whitespace': 'normal'},
        style_table={
            'width': "50%",
            'margin': 'auto'
        }
    ),
])

@app.callback(
    Output('poss-table', 'data'),
    Input('qualifier', 'value')
)
def get_usage_leaders(min_tsa):
    return adv_df.loc[adv_df['MIN_player'] >= min_tsa, ['Player','team','Possessions']].sort_values('Possessions', ascending=False)[:10].to_dict('records')

@app.callback(
    Output('sposs-table', 'data'),
    Input('qualifier', 'value')
)
def get_usage_leaders(min_tsa):
    return adv_df.loc[adv_df['MIN_player'] >= min_tsa, ['Player','team','Scoring Possessions']].sort_values('Scoring Possessions', ascending=False)[:10].to_dict('records')

@app.callback(
    Output('floor-table', 'data'),
    Input('qualifier', 'value')
)
def get_usage_leaders(min_tsa):
    return adv_df.loc[adv_df['MIN_player'] >= min_tsa, ['Player','team','Floor Percentage']].sort_values('Floor Percentage', ascending=False)[:10].to_dict('records')


@app.callback(
    Output('usage-table', 'data'),
    Input('qualifier', 'value')
)
def get_usage_leaders(min_tsa):
    return adv_df.loc[adv_df['MIN_player'] >= min_tsa, ['Player','team','Usage']].sort_values('Usage', ascending=False)[:10].to_dict('records')

@app.callback(
    Output('test', 'data'),
    Input('qualifier', 'value')
)
def get_df_qual(min_tsa):
    val = "You have selected " + str(min_tsa)
    return adv_df.loc[adv_df['MIN_player'] >= min_tsa, ['Player','team','TS%']].sort_values('TS%', ascending=False)[:10].to_dict('records')

@app.callback(
    Output('advanced-table', 'columns'),
    Output('advanced-table', 'data'),
    Input('adv-team-select', 'value')
)
def get_df(team):
    data = adv_df[adv_df.team == team]
    cols = [{"name": i, "id": i} for i in adv_df.columns if i != 'team']
    return cols, data.to_dict('records')


@app.callback(
    Output('table', 'columns'),
    Output('table', 'data'),
    Input('team-select', 'value')
)
def get_df(team):
    data = df[df.team == team].groupby('Player').sum().reset_index()
    data = getPer36(data)
    cols = [{"name": i, "id": i} for i in important_cols]
    return cols, data[important_cols].to_dict('records')

@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname == '/per36':
        return per36_layout
    elif pathname == '/advanced':
        return advanced_layout
    elif pathname == '/league_leaders':
        return ll_layout
    else:
        return index_page

if __name__ == '__main__':
    app.run_server(debug=True)
