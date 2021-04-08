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
            'padding':'0.2em',
        }
    ),

    html.P('Explore the gaming industry by metrics such as: Genres, Ratings, Games by Platform and Year, Dependence of Genres on Player and Critics Reviews. Just choose the genres and ratings you are interested in.',
        style={ #Dashboard Desc
            'margin':'0.5em',
            'width':'50%',
        }
    ),
        dcc.Dropdown( #genre multiple choise list
                    id='genre_dropdown',
                    options=[
                        {'label': 'New York City', 'value': 'NYC'},
                        {'label': 'Montreal', 'value': 'MTL'},
                        {'label': 'San Francisco', 'value': 'SF'}
                    ],
                    value='Choose game genres',
                multi=True
                ),
        dcc.Dropdown( #rating multiple choise list
                    id='rating_dropdown',
                    options=[
                        {'label': 'New York City', 'value': 'NYC'},
                        {'label': 'Montreal', 'value': 'MTL'},
                        {'label': 'San Francisco', 'value': 'SF'}
                    ],
                    value='Choose game ratings',
                multi=True
                ),
    html.Br(),
    html.P('Game Volume:',
            style={
                'margin':'0.5em',
                'width':'50%',
            }
        ),
    html.H4('25',style={'margin':'0.5em'}), #game volume text

    dcc.Graph( #graph
        id='game_graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'plot_bgcolor': colors['background_graph'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                }
            }
        }
    ),
    dcc.Graph( #graph of
            id='game_graph_2',
            figure={
                'data': [
                    {'x': [1, 2, 3,4,5,6,7,8,9,0], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                    {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
                ],
                'layout': {
                    'plot_bgcolor': colors['background_graph'],
                    'paper_bgcolor': colors['background'],
                }
            }
        ),
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