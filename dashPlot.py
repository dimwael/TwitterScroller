import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State,  Event
import twitterScroller as ts
import time
import numpy as np
import pandas as pd


df = pd.DataFrame(np.random.randint(low=0, high=10, size=(3, 3)),columns=['Polarity', 'tweets', 'Subjectivity'])
app = dash.Dash()

Tab_Colors = {
                'veryBad' : '#EE6055',
                'bad': '#FDE74C',
                'null': '#FFE6AC',
                'good': '#9CEC5B',
                'veryGood': '#468a0f'
}
def pickColor(sent):

    clr = ''
    if(sent< -0.5):
        clr = Tab_Colors ['veryBad']
    if(sent>=-0.5 and sent <0):
        clr = Tab_Colors ['bad']
    if(sent==0):
        clr = Tab_Colors ['null']
    if(sent<=0.5 and sent > 0):
        clr = Tab_Colors ['good']
    if(sent>0.5):
        clr = Tab_Colors ['veryGood']
    return clr

def generate_table(df, max_rows=10):
    return html.Table(className="responsive-table",
                      children=[
                          html.Thead(
                              html.Tr(
                                  children=[
                                      html.Th(col.title()) for col in df.columns.values],
                                  style={'color':colors['background']}
                                  )
                              ),
                          html.Tbody(
                              [

                              html.Tr(
                                  children=[
                                      html.Td(data) for data in d
                                      ], style={'color':colors['background'],
                                                'background-color': pickColor(d[1])}
                                 )
                               for d in df.values.tolist()])
                          ]
    )

colors = {
    'background' : '#6d6769',
    'text' : '#00ccff'
        }

app.layout = html.Div(style={'backgroundColor': colors['background']},children=[
    html.H1(children='Tweeter Scroller', style={'color': colors['text']}),

    html.Div([
    html.Div(dcc.Input(id='input-box', type='text', style={'border-bottom-style': 'solid','border-top-style': 'none','border-right-style': 'none','border-color' : colors['text'],'width':'98%','margin-left':10,'margin-right':10,'max-width':50000,'backgroundColor': colors['background'],'color': colors['text']})),
    html.Button('Submit', id='button', style={'border-style': 'none','border-top-style': 'solid','width':'98%','margin-left':10,'margin-right':10,'max-width':50000,'backgroundColor': colors['background'],'color': colors['text']}),
    html.Div(id='output-container-button',
    children='Enter a value and press submit',
    style ={'border-style': 'none','border-top-style': 'solid','width':'98%','margin-left':10,'margin-right':10,'max-width':50000,'backgroundColor': colors['background'],'color': colors['text']})
    ]),

    html.H1(children='', style={'color': colors['text']}),
    dcc.Graph(
    style={'backgroundColor': colors['background']},
        id='example-graph2',

        figure={
            'data': [
                {'x': [1], 'y': [ts.GetPolarityMean()], 'type': 'bar', 'name': 'For' },
                {'x': [1], 'y': [1-ts.GetPolarityMean()], 'type': 'bar', 'name': u'Against'},
            ],
            'layout': {
                'title': 'Polarity vs Subjectivity'
            }
        }
    ),
    html.Div(className='row', children=[html.Div(id="recent-tweets-table", className='col s12 m6 l6')]),
                                        #html.Div(dcc.Graph(id='sentiment-pie', animate=False), className='col s12 m6 l6'),]),


    dcc.Interval(
        id='graph-update',
        interval=1*1000
    ),
    dcc.Interval(
        id='historical-update',
        interval=60*1000
    ),

    dcc.Interval(
        id='related-update',
        interval=30*1000
    ),

    dcc.Interval(
        id='recent-table-update',
        interval=2*1000
    ),

    dcc.Interval(
        id='sentiment-pie-update',
        interval=60*1000
    )
])

@app.callback(Output('recent-tweets-table', 'children'),
              [dash.dependencies.Input('button', 'n_clicks')],
              [dash.dependencies.State('input-box', 'value')],
              events=[Event('recent-table-update', 'interval')]
              )
def update_recent_tweets(sentiment_term, value):
    df = ts.CollectingTweets(value)
    update_graph(0,0)
    return generate_table(df, max_rows=10)

@app.callback(
    dash.dependencies.Output('output-container-button', 'children'),
    [dash.dependencies.Input('button', 'n_clicks')],
    [dash.dependencies.State('input-box', 'value')])

def update_output(n_clicks, value):
    return 'You searched for "{}" '.format(
        value
    )




@app.callback(Output('example-graph2', 'figure'),
                  [dash.dependencies.Input('button', 'n_clicks')],
                  [dash.dependencies.State('input-box', 'value')],
                  events=[Event('recent-table-update', 'interval')]
                  )
def update_graph(n_clicks, value):
    X = df.index
    Y = ts.GetPolarityMean()
    print(ts.GetPolarityMean())
    return { 'style' : {'backgroundColor': colors['background']},
    'data': [
        {'x': [1], 'y': [ts.GetPolarityMean()], 'type': 'bar', 'name': 'For', 'bar' : {'color': '#ff0066'} },
        {'x': [1], 'y': [1-ts.GetPolarityMean()], 'type': 'bar', 'name': u'Against'},
        {'x': [2], 'y': [ts.GetSubjectivityMean()], 'type': 'bar', 'name': 'For'},
        {'x': [2], 'y': [1-ts.GetSubjectivityMean()], 'type': 'bar', 'name': u'Against'}
    ],
    'layout': {
        'title': 'Polarity vs Subjectivity' , 'backgroundColor': colors['background']
    }
}
    #return {'data': [data]}


if __name__ == '__main__':
    for d in df.values.tolist():
        print (d[2])
    app.run_server(debug=True)
