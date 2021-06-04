import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output


import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from itertools import cycle

# colors, Set1 - color palette
palette = cycle(px.colors.qualitative.Set1)

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

    html.Div(style={'width': '70%', 'display': 'flex', 'flex-direction': 'row'}, children=[  # Dropdown fields
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
                         {'label': i, 'value': i} for i in games_df.Rating.unique()  # ratings from dataframe
                     ],
                     placeholder='Select game ratings',
                     multi=True,
                     value = games_df.Rating.unique(),
                     ),
        html.Label('Platform:', style={'padding': '5px'}),
        dcc.Dropdown(style={'width': '100%'},  # genre multiple choise list
                     id='platform_dropdown',
                     options=[
                         {'label': i, 'value': i} for i in games_df.Platform.unique()  # platforms from dataframe
                     ],
                     placeholder='Select platforms',
                     multi=True,
                     searchable=True,
                     value = games_df.Platform.unique()
                     ),
    ]),

    html.Br(),

    html.Div(style={'width': '10%', 'display': 'flex', 'flex-direction': 'row'}, children=[
        html.Label('Games Volume:', style={'margin': '0.5em', }),
        html.Div(id='games_volume_selected', style={'padding': '5px', 'font-size': '14pt'}),  # games volume
    ]),

    html.Div(style={'display': 'flex', 'flex-direction': 'row'}, children=[
        dcc.Graph(style={'width': '50%'},  # graph
                  id='game_graph',
                  ),
        dcc.Graph(style={'width': '50%'},  # graph
                  id='scores_graph',
                  )
    ]),
    html.Div(style={'width':'80%','margin':'auto'},id='game_table')

    #html.Label('Release Dates:', style={'padding': '5px'}),
    # dcc.RangeSlider(
    #     max=len(games_df['Year_of_Release'].sort_values().unique()),
    #     step=None,
    #     marks=[{'label': i, 'value': i} for i in games_df['Year_of_Release'].astype(int).sort_values().unique()],
    # )
])


@app.callback(
    [Output('games_volume_selected', 'children'),
     Output('game_graph', 'figure'),
     Output('scores_graph', 'figure'),
     Output('game_table', 'children')],
    [Input('genre_dropdown', 'value'),
     Input('rating_dropdown', 'value'),
     Input('platform_dropdown','value')]
)
def display_data(genre_dropdown, rating_dropdown,platform_dropdown):
    if not rating_dropdown and not genre_dropdown and not platform_dropdown:
        cn_df_f = games_df
        #print('1')
    elif not rating_dropdown or not genre_dropdown or not platform_dropdown:
        #print('2')
        cn_df_f = games_df.loc[(games_df.Rating.isin(list(rating_dropdown))) | (games_df.Genre.isin(list(genre_dropdown))) | (games_df.Platform.isin(list(platform_dropdown)))]
    else:
        #print('3')
        cn_df_f = games_df.loc[(games_df.Rating.isin(list(rating_dropdown))) & (games_df.Genre.isin(list(genre_dropdown))) &  (games_df.Platform.isin(list(platform_dropdown)))]

    fig = go.Figure()

    dff = cn_df_f.groupby(["Year_of_Release", "Platform"], as_index=False).size()
    platform_year_df = dff.pivot(index='Platform', columns='Year_of_Release', values='size').fillna(0) #corellation between Platfroms and Years of Release
    x = list(platform_year_df.columns) #x for platform graph
    for i in range(len(platform_year_df.index)): #Adding traces as Platforms for graph
        fig.add_trace(go.Scatter(
            name=platform_year_df.index[i],
            x=x,
            y=list(platform_year_df.iloc[i]),
            mode='lines',
            line=dict(width=1.5, color=next(palette)),
            stackgroup=i,
        ))
    pl_ye_fig = fig.update_layout(
        title='Platforms by Years',
        showlegend=True,
        xaxis_type='category'
    )
    #print(cn_df_f)
    sc_gn_fig = px.scatter(cn_df_f,
                           x="User_Score",
                           y="Critic_Score",
                           color="Genre",
                           hover_data=['Name'],
                           title="Scores by Genres")
    gm_table = dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in cn_df_f.columns],
        data=cn_df_f.to_dict('records'),
    )
    return len(cn_df_f), pl_ye_fig, sc_gn_fig, gm_table


if __name__ == '__main__':
    app.run_server(debug=True)
