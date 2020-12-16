#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 12 13:56:21 2020

@author: merveyolcu
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

stylesheet = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# pandas dataframe to html table
def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

app = dash.Dash(__name__, external_stylesheets=stylesheet)
server = app.server

d = pd.read_csv('/Users/merveyolcu/Desktop/ma705project/moviedataset.csv')
df= d.head(n=10)
df =df.drop('Unnamed: 0', axis=1)
df
df.sort_values("Movie_names")

df2= d.iloc[-10:]
df2= df2.drop('Unnamed: 0', axis=1)

def floattype(s):
    if s == 'tbd':
        return 0
    return float(s)

d['User_scores'] = d['User_scores'].apply(floattype)
sd = d.sort_values(by=['User_scores'], inplace=False, ascending=False)
sd.drop('Unnamed: 0', axis=1)
sd.drop(sd.tail(63).index,inplace=True)
sd_head = sd.head(n=10)
sd_tail = sd.tail(n=10)


fig = px.bar(sd_head, x="User_scores", y="Movie_names")
fig.update_layout(xaxis_range=[8.5,9.5])


fig2 = px.bar(sd_tail, x="User_scores", y="Movie_names")
fig2.update_layout(xaxis_range=[2,5.5])


app.layout = html.Div([
    html.H1('Movie Scores', style={'textAlign': 'center'}),
    html.H5('Do both user score and meta score for movies align with each other? Let’s see the top and last 10 movies for user scores and meta scores located on meta critic website, and compare the result.'),

    html.Div([html.H3('Top 10 for Meta Scores'),
                  html.Div(id='df_div'),
    html.H3('Sort table by:'),
    dcc.Dropdown(options=[{'label': 'Meta_scores', 'value': 'Meta_scores'},
                          {'label': 'Movie_names', 'value': 'Movie_names'}],
                 id='sort_by_dropdown',
                 value='Movie_names')]),
    html.H3('Last 10 for Meta Scores'),
    generate_table(df2),
    html.H3('Top 10 for User Scores'),
    dcc.Graph(id='example-graph', figure=fig),
    html.H3('Last 10 for User Scores'),
    dcc.Graph(id='example2-graph', figure=fig2),
    html.H3('Conclusion'),
    html.H5('In the top 10 movies, only one movie is common for user scores and meta scores. Similarly, in the last 10 movies, there is only one movie common for both score types. It is clear that these scores are not based on similar criteria. Users should choose their movies based on one of the score types only, since they do not align with each other.')
    ])

#update the table
@app.callback(
    Output(component_id='df_div', component_property='children'),
    [Input(component_id='sort_by_dropdown', component_property='value')]
)                                   
def update_table(sort_by):
    x = df.sort_values(sort_by, ascending=(sort_by != "Meta_scores"))
    return generate_table(x)                  
                                   

if __name__ == '__main__':
    app.run_server(debug=True)