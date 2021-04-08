import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from datetime import datetime as dt


games_df = pd.read_csv('games.csv')
games_df = games_df.dropna()
games_df = games_df.loc[(games_df['Year_of_Release']>=2000)]

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#fff',
    'text': '#000',
    'background_graph':'#eaeaea',
}

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1( #Dashboard Title
        children='Games Dash',
        style={
            'textAlign': 'left',
            'color': colors['text'],
            'margin-bottom':'10px',
        }
    ),

    html.P('Explore the gaming industry by metrics such as: Genres, Ratings, Games by Platform and Year, Dependence of Genres on Player and Critics Reviews. Just select the genres and ratings you are interested in.',
        style={ #Dashboard Desc
            'margin':'0.5em',
            'width':'50%',
        }
    ),

    html.Div(style={'width':'100%','height':'0.5px','background-color':'#e5e5e5','margin-bottom':'20px'}),
    html.Div(style={'width':'20%','display':'flex','flex-direction':'row'},children=[
        html.Label('Genre:',style={'padding':'5px'}),
        dcc.Dropdown(style={'width':'250px'}, #genre multiple choise list
            id='genre_dropdown',
            options=[
                {'label': 'New York City', 'value': 'NYC'},
                    #genres from dataframe
                ],
            placeholder='Select game genres',
            multi=True
        ),

        html.Label('Rating:',style={'padding':'5px'}),
        dcc.Dropdown(style={'width':'250px'}, #rating multiple choise list
            id='rating_dropdown',
            options=[
                {'label': 'New York City', 'value': 'NYC'},
                    #ratings from dataframe
                ],
            placeholder='Select game ratings',
            multi=True
        )
    ]),

    html.Br(),
    html.Div(style={'display':'flex','flex-direction':'column'},children=[
    html.Label('Game Volume:',
                style={
                    'margin':'0.5em',
                    'width':'50%',
                }
            ),
    html.B('25',style={'padding':'5px','font-size':'16pt'}), #game volume text
    ]),

    html.Div(style={'display':'flex','flex-direction':'row'},children=[
    dcc.Graph(style={'width':'50%'}, #graph
        id='game_graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'plot_bgcolor': colors['background_graph'],
                'paper_bgcolor': colors['background'],
                'title':'Games by Year and Platforms',
            }
        }
    ),
    dcc.Graph(style={'width':'50%'}, #graph
            id='game_graph_2',
            figure={
                'data': [
                    {'x': [1, 2, 3,4,5,6,7,8,9,0], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                    {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
                ],
                'layout': {
                    'plot_bgcolor': colors['background_graph'],
                    'paper_bgcolor': colors['background'],
                    'title': 'Scores by Genres',
                }
            }
        )
    ]),
    dcc.DatePickerRange(
        id="date-picker-select",
        start_date=dt(2014, 1, 1),
        end_date=dt(2014, 1, 15),
        min_date_allowed=dt(2014, 1, 1),
        max_date_allowed=dt(2014, 12, 31),
        initial_visible_month=dt(2014, 1, 1),
    ),
])

if __name__ == '__main__':
    app.run_server(debug=True)