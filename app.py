import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px

#df = pd.read_csv('games.csv')
#fig = px.area(df, x="year", y="pop", color="continent",line_group="country")

games_df = pd.read_csv('games.csv')
games_df = games_df.loc[(games_df['Year_of_Release']>=2000)].dropna()

platform_year_df = pd.DataFrame(games_df.groupby('Platform')['Year_of_Release'].value_counts()).rename(columns={'Year_of_Release':'Counts'}).reset_index()

fig = px.area(platform_year_df, x="Year_of_Release", y="Counts", color="Platform",line_group="Platform")



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#fff',
    'text': '#000',
    'background_graph':'#eaeaea',
}

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1( #Dashboard Title
        children='Games Dasboard',
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

    html.Div(style={'width':'10%','display':'flex','flex-direction':'row'},children=[
        html.Label('Game Volume:',style={'margin':'0.5em',}),
        html.B('25',style={'padding':'5px','font-size':'14pt'}), #game volume text
    ]),

    html.Div(style={'display':'flex','flex-direction':'row'},children=[
    dcc.Graph(figure=fig, style={'width':'50%'}, #graph
        id='game_graph',
    ),
    dcc.Graph(style={'width':'50%'}, #graph
            id='game_graph_2',
            figure={ #Scatter plot Scores by Gengers
                'data': [
                    {'x': [1,2], 'y': [1,2,3,4], 'type': 'line', 'name': 'SF'},
                    {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'line', 'name': u'Montréal'},
                ],
                'layout': {
                    'plot_bgcolor': colors['background_graph'],
                    'paper_bgcolor': colors['background'],
                    'title': 'Scores by Genres',
                }
            }
        )
    ]),

    html.Label('Release Dates:',style={'padding':'5px',}),
    dcc.DatePickerRange(
        start_date_placeholder_text="Start Date",
        end_date_placeholder_text="End Date",
        calendar_orientation='horizontal',
        with_portal=True,
    ),
])


if __name__ == '__main__':
    app.run_server(debug=True)