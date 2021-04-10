import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
import plotly.express as px

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#fff',
    'text': '#000',
    'background_graph': '#eaeaea',
}

# MAIN DATAFRAME
games_df = pd.read_csv('games.csv')
games_df = games_df.loc[(games_df['Year_of_Release'] >= 2000)].dropna()
games_df['Year_of_Release'] = games_df['Year_of_Release'].astype(int)

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(  # Dashboard Title
        children='Games Dasboard',
        style={'textAlign': 'left', 'color': colors['text'], 'margin-bottom': '10px', }
    ),
    html.P(
        'Explore the gaming industry by metrics such as: Genres, Ratings, Games by Platform and Year, Dependence of Genres on Player and Critics Reviews. Just select the genres and ratings you are interested in.',
        style={'margin': '0.5em', 'width': '50%', }  # Dashboard Desc
    ),
    html.Div(style={'width': '100%', 'height': '0.5px', 'background-color': '#e5e5e5', 'margin-bottom': '20px'}),
    # Simple line

    html.Div(style={'width': '50%', 'display': 'flex', 'flex-direction': 'row'}, children=[  # Dropdown fields
        html.Label('Genre:', style={'padding': '5px'}),
        dcc.Dropdown(style={'width': '100%'},  # genre multiple choise list
                     id='genre_dropdown',
                     options=[
                         {'label': i, 'value': i} for i in games_df.Genre.unique()  # genres from dataframe
                     ],
                     placeholder='Select game genres',
                     multi=True,
                     searchable=True,
                     value = games_df.Genre.unique()
                     ),
        html.Label('Rating:', style={'padding': '5px'}),
        dcc.Dropdown(style={'width': '100%'},  # rating multiple choise list
                     id='rating_dropdown',
                     options=[
                         {'label': i, 'value': i} for i in games_df.Rating.unique()  # genres from dataframe
                     ],
                     placeholder='Select game ratings',
                     multi=True,
                     value = games_df.Rating.unique(),
                     ),
    ]),

    html.Br(),

    html.Div(style={'width': '10%', 'display': 'flex', 'flex-direction': 'row'}, children=[
        html.Label('Games Volume:', style={'margin': '0.5em', }),
        html.Div(id='games_volume_selected', style={'padding': '5px', 'font-size': '14pt'}),  # games volume
        html.Div(id='rating_volume_selected', style={'padding': '5px', 'font-size': '14pt'}),  # rating volume
    ]),

    html.Div(style={'display': 'flex', 'flex-direction': 'row'}, children=[
        dcc.Graph(style={'width': '50%'},  # graph
                  id='game_graph',
                  ),
        dcc.Graph(style={'width': '50%'},  # graph
                  id='scores_graph',
                  )
    ]),

    html.Label('Release Dates:', style={'padding': '5px'}),
    dcc.RangeSlider(
        min=0,
        max=10,
        step=None,
        marks={
            0: '0 °F',
            3: '3 °F',
            5: '5 °F',
            7.65: '7.65 °F',
            10: '10 °F'
        },
        value=[3, 7.65]
    )
])


@app.callback(
    Output('rating_volume_selected', 'children'),
    [Input('genre_dropdown', 'value'),
     Input('rating_dropdown', 'value')]
)
def display_volume(genre_dropdown, rating_dropdown):
    if not rating_dropdown and not genre_dropdown:
        cn_df = len(games_df)
    elif not rating_dropdown or not genre_dropdown:
        cn_df = len(games_df.loc[(games_df.Rating.isin(list(rating_dropdown))) | (games_df.Genre.isin(list(genre_dropdown)))])
    else:
        cn_df = len(games_df.loc[(games_df.Rating.isin(list(rating_dropdown))) & (games_df.Genre.isin(list(genre_dropdown)))])
    return cn_df

@app.callback(
    [Output('game_graph', 'figure'),
     Output('scores_graph', 'figure')],
    [Input('genre_dropdown', 'value'),
     Input('rating_dropdown', 'value')]
)
def display_figures(genre_dropdown, rating_dropdown):
    if not rating_dropdown and not genre_dropdown:
        cn_df_f = games_df
    elif not rating_dropdown or not genre_dropdown:
        cn_df_f = games_df.loc[(games_df.Rating.isin(list(rating_dropdown))) | (games_df.Genre.isin(list(genre_dropdown)))]
    else:
        cn_df_f = games_df.loc[(games_df.Rating.isin(list(rating_dropdown))) & (games_df.Genre.isin(list(genre_dropdown)))]
    print(len(cn_df_f))
    platform_year_df = cn_df_f.groupby(["Platform", "Year_of_Release"], as_index=False).size()
    pl_ye_fig = px.area(platform_year_df, x='Year_of_Release', y='size', color='Platform', \
                        title="Games Volume by Platform and Year")
    sc_gn_fig = px.scatter(cn_df_f, x="User_Score", y="Critic_Score", color="Genre", \
                           title="Scores by Gengers")
    return pl_ye_fig, sc_gn_fig

if __name__ == '__main__':
    app.run_server(debug=True)
