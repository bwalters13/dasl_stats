import dash_html_components as html
import pandas as pd
import dash
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_table
import base64
import numpy as np
import math

season = 94
svg_file = "demo.svg"
encoded = base64.b64encode(open(svg_file,'rb').read())
svg = 'data:image/svg+xml;base64,{}'.format(encoded.decode())

header_style= {'backgroundColor': '#DCDCDC', 'color': 'orange', 'font-family': 'futura'}

team_colors = {
    '76ers': ['rgb(0, 107, 182)', 'rgb(237, 23, 76)'],
    'Bucks': ['rgb(0, 148, 41)', 'rgb(247, 165, 0)'],
    'Bullets': ['rgb(227,24,55)', 'rgb(0,43,92)'],
    'Bulls': ['rgb(206, 17, 65)', 'black'],
    'Cavaliers': ['rgb(220, 59, 52)', 'rgb(4, 34, 92)'],
    'Celtics': ['rgb(0, 122, 51)', 'rgb(139, 111, 78)'],
    'Clippers': ['rgb(200,16,46)', 'rgb(29,66,148)'],
    'Grizzlies': ['rgb(0, 178, 169)', 'rgb(228, 60, 64)'],
    'Hawks': ['rgb(200, 16, 46)', 'rgb(228, 60, 64)'],
    'Heat': ['rgb(152, 0, 46)', 'rgb(249, 160, 27)'],
    'Hornets': ['rgb(0, 119, 139)', 'rgb(40, 0, 113)'],
    'Jazz': ['rgb(117, 59, 189)', 'rgb(0, 169, 224)'],
    'Kings': ['rgb(84,46,145)', 'rgb(196,206,212)'],
    'Knicks': ['rgb(245, 132, 38)', 'rgb(0, 107, 182)'],
    'Lakers': ['rgb(85, 37, 130)', 'rgb(253, 185, 39)'],
    'Magic': ['rgb(0, 125, 197)', 'rgb(196, 206, 211)'],
    'Mavericks': ['rgb(0, 40, 85)', 'rgb(0, 132, 61)'],
    'Nets': ['rgb(0,42,96)', 'rgb(205,16,65)'],
    'Nuggets': ['rgb(4, 30, 66)', 'rgb(157, 34, 53)'],
    'Pacers': ['rgb(253, 187, 48)', 'rgb(0, 45, 98)'],
    'Pistons': ['rgb(213,0,50)', 'rgb(0,61,165)'] ,
    'Raptors': ['rgb(117, 59, 189)', 'rgb(186, 12, 47)'],
    'Rockets': ['rgb(186,12,47)', 'black'],
    'Spurs': ['rgb(138, 141, 143)', 'black'],
    'Suns': ['rgb(255, 105, 0)', 'rgb(95, 37, 159)'],
    'SuperSonics': ['rgb(0,101,58)', 'rgb(255,194,32)'],
    'Timberwolves': ['rgb(35, 97, 146)', 'rgb(0, 132, 61)'],
    'Trailblazers': ['rgb(224, 58, 62)', 'black'],
    'Warriors': ['rgb(4, 30, 66)', 'rgb(190, 58, 52)']
}


df = pd.read_csv(f'{season}season.csv')
df_team = df.groupby('team').sum()
df_team['num_games'] = df.groupby('team')['game_id'].nunique()
for x in df_team.columns[1:14]:
    df_team[x] = (df_team[x]/df_team['num_games']).round(2)
df_team_avg = df_team[df_team.columns[1:14]].reset_index()
per36 = df.columns[3:16].tolist()
adv_df = pd.read_csv(f'{season}advanced.csv')
min_limit = math.ceil(adv_df['MIN_player'].describe()['25%']/10)*10

important_cols = ['Player'] + df.columns[2:16].tolist()
important_cols.insert(4, 'FG%')
important_cols.insert(7, '3P%')
important_cols.insert(10, 'FT%')



def getPer36(df):
    for x in per36:
        df[x] = ((df[x]/df['MIN'])*36).round(2)
    df['FG%'] = ((df['FG']/df['FGA'])*100).round(2)
    df['3P%'] = ((df['3P']/df['3PA'])*100).round(2)
    df['FT%'] = ((df['FT']/df['FTA'])*100).round(2)

    return df


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = 'DASL Stats'

header = html.Div(className='topnav', children=[
        html.Img(src=svg),
        dcc.Link('Per 36 Stats', href='/per36'),            
        dcc.Link('Advanced Stats', href='/advanced'),
        dcc.Link('League Leaders', href='/league_leaders'),
        dcc.Link('Glossary', href='/glossary'),
        html.H6("Updated through Day {}".format(df['day'].max()))
    ]
    )

app.layout = html.Div(children=[
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

index_page = html.Div(children=[
    header
]),

glossary_layout = html.Div(className='glossary',
    children=[
        header,
        html.H1('GLOSSARY'),
        html.H4('Usage: '),
        html.P('Usage Percentage (available since the 1977-78 season in the NBA); the formula is 100 * ((FGA + 0.44 * FTA + TOV) * (Tm MP / 5)) / (MP * (Tm FGA + 0.44 * Tm FTA + Tm TOV)). Usage percentage is an estimate of the percentage of team plays used by a player while he was on the floor. '),
        html.H4('True Shooting Percentage (TS%):'),
        html.P("True Shooting Percentage; the formula is PTS / (2 * TSA). True shooting percentage is a measure of shooting efficiency that takes into account field goals, 3-point field goals, and free throws."),
        html.H4('True Shooting Attempts (TSA):'),
        html.P('TSA - True Shooting Attempts; the formula is FGA + 0.44 * FTA. '),
        html.H4('Possessions:'),
        html.P("A player's total possessions would be all of his scoring possessions, plus his missed field goals and free throws that weren't rebounded by his team, plus his turnovers. "),
        html.H4("Scoring Possessions:"),
        html.P("A player's scoring possessions would be his field goals that weren't assisted on, plus a certain percentage of his field goals that were assisted on, plus a certain percentage of his assists, plus his free throws made that represented a team scoring possession."),
        html.H4("Floor Percentage:"),
        html.P("Individual floor % is then just a player's scoring possessions divided by his total possessions. This statistic takes all areas of a player's offensive contribution, with the possible exception of his offensive rebounds (they are indirectly counted in the total possession formula). Many times, field goal percentages and free throw percentages are quoted as measures of a player's scoring efficiency. For guards, assist to turnover ratios are often quoted. Individual floor % sums it all up into one meaningful number."),

    ])


per36_layout = html.Div(children=[
    header,
    html.H4(children='Per 36 Stats', style={'color': 'orange', 'font-family': 'futura', 'text-align': 'center', 'font-weight': 'bold'}),
    dcc.Dropdown(
        id='team-select',
        style={
            'color': 'black',
            'width': '50%',
            'fontSize': '20px',
            'margin': 'auto',
        },
        options=[
            {'label': team, 'value': team}
            for team in sorted(df['team'].unique())
        ]
    ),
    dash_table.DataTable(
        id='table',
        sort_action='native',
        style_table={'width': '80%', 'margin': 'auto'},
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
    style_cell={'fontFamily': 'cursive',
    }
    ),
])

advanced_layout = html.Div(children=[
    header,
    html.H4(children='Advanced Stats', style={'color': 'orange', 'font-family': 'futura', 'text-align': 'center', 'font-weight': 'bold'}),
    dcc.Dropdown(
        id='adv-team-select',
        style={
            'color': 'black',
            'width': '50%',
            'fontSize': '20px',
            'margin': 'auto',
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
            'margin': 'auto',
        },
        
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
    header,
    html.H3("Select Minutes Qualifier"),
    dcc.Slider(
        className="slider",
        id="qualifier",
        min=0,
        max= int(adv_df["MIN_player"].max())+1,
        step=40,
        marks={ i:str(i) for i in range(0, int(adv_df["MIN_player"].max())+1, 200)},
        value=min_limit,
    ), 
    html.H2("True Shooting Leaders"),
    dash_table.DataTable(
        id='test',
        columns=[{'name': i, 'id': i} for i in ['Player','team','TS%']],
        style_cell={'minWidth': '40px', 'width': '40px', 'maxWidth': '40px', 'whitespace': 'normal'},
        style_table={
            'width': "50%",
            'margin': 'auto'
        },
        style_header=header_style,
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
        },
        style_header=header_style,
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
        },
        style_header=header_style,
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
        },
        style_header=header_style,
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
        }, 
        style_header=header_style,
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
    Output('advanced-table', 'style_header'),
    Input('adv-team-select', 'value')
)
def get_df(team):
    data = adv_df[adv_df.team == team]
    cols = [{"name": i, "id": i} for i in adv_df.columns[:-1] if i != 'team']
    rand_num = np.random.randint(0,2)
    other = np.abs(-1+rand_num)
    return cols, data.to_dict('records'), {'backgroundColor': team_colors[team][rand_num], 'color': team_colors[team][other]}


@app.callback(
    Output('table', 'columns'),
    Output('table', 'data'),
    Output('table', 'style_header'),
    Input('team-select', 'value')
)
def get_df(team):
    data = df.groupby('Player').sum().reset_index()
    data = data.merge(adv_df[['Player', 'team']])
    data = data[data.team == team]
    data = getPer36(data)
    cols = [{"name": i, "id": i} for i in important_cols]
    rand_num = np.random.randint(0,2)
    other = np.abs(-1+rand_num)
    return cols, data[important_cols].to_dict('records'), {'backgroundColor': team_colors[team][rand_num], 'color': team_colors[team][other]}

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
    elif pathname == '/glossary':
        return glossary_layout
    else:
        return index_page

if __name__ == '__main__':
    app.run_server(debug=True)