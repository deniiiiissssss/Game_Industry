import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
import plotly.express as px

#MAIN DATAFRAME
games_df = pd.read_csv('games.csv')
games_df = games_df.loc[(games_df['Year_of_Release']>=2000)].dropna()\
    .rename(columns={'User_Score':'User Score','Critic_Score':'Critic Score'})

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

    html.Div(style={'width':'50%','display':'flex','flex-direction':'row'},children=[

        html.Label('Genre:',style={'padding':'5px'}),
        dcc.Dropdown(style={'width':'100%'}, #genre multiple choise list
            id='genre_dropdown',
            options=[
                {'label': i, 'value': i} for i in games_df.Genre.unique()
                    #genres from dataframe
                ],
            placeholder='Select game genres',
            multi=True,
            searchable=True,
            value=games_df.Genre.unique()[0],
        ),
        html.Div(id='genre_selected'),

        html.Label('Rating:',style={'padding':'5px'}),
        dcc.Dropdown(style={'width':'100%'}, #rating multiple choise list
            id='rating_dropdown',
            options=[
                {'label': i, 'value': i} for i in games_df.Rating.unique()
            ],
            placeholder='Select game ratings',
            multi=True,
            searchable=True,
            value=games_df.Rating.unique()[0],
        ),
        html.Div(id='rating_selected'),

    ]),

    html.Br(),

    html.Div(style={'width':'10%','display':'flex','flex-direction':'row'},children=[
        html.Label('Games Volume:',style={'margin':'0.5em',}),
        html.Div(id='games_volume_selected',style={'padding':'5px','font-size':'14pt'}), #games volume
    ]),

    html.Div(style={'display':'flex','flex-direction':'row'},children=[
    dcc.Graph(figure=platform_year_fig, style={'width':'50%'}, #graph
        id='game_graph',
    ),

    dcc.Graph(figure=scores_genres_fig,style={'width':'50%'}, #graph
            id='scores_graph',
        )
    ]),

    html.Label('Release Dates:',style={'padding':'5px'}),
    dcc.DatePickerRange(
        id="gade_range",
        start_date_placeholder_text='Start Date',
        end_date_placeholder_text='End Date',
        calendar_orientation='horizontal',
        with_portal=True,
    ),
])



platform_year_df = games_df.groupby(["Platform", "Year_of_Release"]).size().reset_index(name="Volume")

platform_year_fig = px.area(platform_year_df, x='Year_of_Release', y='Volume', color='Platform',\
              title="Games Volume by Platform and Year")


scores_genres_fig = px.scatter(games_df, x="User Score", y="Critic Score", color="Genre",\
                               title="Scores by Gengers")

@app.callback(
    Output(component_id='games_volume_selected', component_property='children'),
    Input(component_id='genre_dropdown', component_property='value'),
    Input(component_id='rating_dropdown', component_property='value'))
def display(genre_dropdown, rating_dropdown):
    if genre_dropdown == None or rating_dropdown == None:
        return 0
    else:
        print(genre_dropdown,rating_dropdown)
        return '{}'.format(len(games_df.loc[(games_df['Genre'].isin(list(genre_dropdown))) | (games_df['Rating'].isin(list(rating_dropdown)))]))


if __name__ == '__main__':
    app.run_server(debug=True)