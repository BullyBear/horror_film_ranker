import os 
import color_scale
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import numpy as np
import pandas as pd 
import scipy as sp
import sklearn as sk


mapbox_access_token = 'pk.eyJ1IjoiYnVsbHliZWFyIiwiYSI6ImNqbDB1M2dnaDE4cWQza2xlazE3Z2t4ZnUifQ.m3UgrvGKwKUsPFDUa1MT5w'
#mapbox_access_token = 'pk.eyJ1IjoiaXZhbm5pZXRvIiwiYSI6ImNqNTU0dHFrejBkZmoycW9hZTc5NW42OHEifQ._bi-c17fco0GQVetmZq0Hw'

app = dash.Dash(name=__name__)
app.config.supress_callback_exceptions = True

server = app.server
server.secret_key = os.environ.get('secret_key', 'secret')

# Color scale for heatmap (green-to-red)
color_scale = color_scale.GREEN_RED

# Load styles
css_url = 'https://codepen.io/bullybear/pen/RYbbpW.css'
css_bootstrap_url = 'https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.6/css/bootstrap.min.css'
app.css.append_css({
    "external_url": [css_bootstrap_url, css_url],
})

df = pd.read_csv('/Users/WilliamStevens/Documents/deplorable_snowflake/ds/app_6/horror_films.csv')
#print(df.head())


yearmax = df.groupby('Year', as_index=False)[
    'Jump', 'Scary', 'Gore'].max()

yearmean = df.groupby('Year', as_index=False)[
    'Jump', 'Scary', 'Gore'].mean()

yearmin = df.groupby('Year', as_index=False)[
    'Jump', 'Scary', 'Gore'].min()

#year_scores = [yearmax, yearmean, yearmin]
#print(year_scores) 


####################################

#       INITIALIZE DASH APP

####################################


app.layout = html.Div([

    # LANDING
    html.Div(
        className='section',
        children=[
            html.H1('ARE YOU AFRAID OF THE DARK?', className='landing-text')
        ]
    ),
    html.Div(
        className='content',
        children=[

            # SLIDER ROW
            html.Div(
                className='col',
                children=[
                  	html.Div(
                      	id='slider',
                      	children=[
                          	dcc.Slider(
                              	id='date-slider',
                              	min=min(df['Year']),
                              	max=max(df['Year']),
                              	marks={
                              	1921: {'label': '1921'},
                              	1930: {'label': '1930'},
                              	1940: {'label': '1940'},
                              	1950: {'label': '1950'},
                              	1960: {'label': '1960'},
                              	1970: {'label': '1970'},
                              	1980: {'label': '1980'},
                              	1990: {'label': '1990'},
                              	2000: {'label': '2000'},
                              	2010: {'label': '2010'},
                              	2018: {'label': '2018'}, 
                              	},
                              	value=1975,
                          		),
                      			], 	
                      			style={
                          		'background': '#191a1a',
                          		'margin-bottom': '50px'
                      			}
                  				)
                				], 	
                				style={
                    			'background': '#191a1a',
                				})
            					]), 

            # GRAPHS ROW
            html.Div(
                id='graphs',
                className='row',
                children=[
                    html.Div(
                        className='col-4',
                        children=[
                          	dcc.Graph(
                              	id='graph-1',
                          	),
                        ]),
                    html.Div(
                        className='col-4',
                        children=[
                            dcc.Graph(
                                id='graph-2',
                            ),
                        ]),
                    html.Div(
                        className='col-4',
                        children=[
                            dcc.Graph(
                                id='graph-3',
                            ),
                        ])
                ], 	style={
                    	'padding-bottom': 100
                }
            ),

            # MAP ROW
            html.Div(
                className='row',
                children=[
                    
                    dcc.Graph(
                        id='graph-4',
                        animate=True,
                        style={
                          'width': '100%',
                          'height': 800,
                        }
                    ),
                ]),

            # ABOUT ROW
            html.Div(
                className='row',
                children=[
                  	html.Div(
                    	className='col',
                    	children=[
                      	html.P(
                        'Data Extracted From:'
                      	),
                      	html.A(
                          	'Scared To Watch',
                          	href='https://www.scaredtowatch.com/'
                      	)                    
                    ]
                )], 

    
                			
        		style={
        			'padding': 40
                } 
            )

        ])


# CHART 1

@app.callback(
	Output('graph-1', 'figure'),
    [Input('date-slider', 'value')]
    ) 


def update_graph_1(year_value): 


    data = go.Data([
        go.Scatter(
            name='Max Scary',
            # events qty
            x=np.arange(1921, year_value),
            # year
            y=yearmax['Scary'],

            #mode='lines',
            #marker={
                #'symbol': 'circle'
                #'size': 5
                #'color': '#eb1054'
            #},
            #hoverlabel={
                #'bgcolor': '#FFF',
            #},
        ),
        go.Scatter(
            name='Mean Scary',
            # events qty
            x=np.arange(1921, year_value + 1),
            # year
            y=yearmean['Scary'],

            #mode='lines',
            #marker={
                #'symbol': 'circle',
                #'size': 5,
                #'color': '#C2FF0A'
            #},
            #hoverlabel={
                #'bgcolor': '#FFF',
            #},
        ),
        go.Scatter(
            name='Min Scary',
            # events qty
            x=np.arange(1921, year_value + 1),
            # year
            y=yearmin['Scary'],

            #mode='lines',
            #marker={
                #'symbol': 'circle',
                #'size': 5,
                #'color': '#52e5ec'
            #},
            #hoverlabel={
                #'bgcolor': '#FFF',
            #},
        ),
    ])

    layout = go.Layout(
        xaxis={
            'autorange': True,
            'color': '#FFF',
            'title': 'Year',
        },
        yaxis={
            'autorange': True,
            'color': '#FFF',
            'title': 'Score',
        },
        margin={
            'l': 40,
            'b': 40,
            't': 10,
            'r': 0
        },
        hovermode='closest',
        paper_bgcolor='#191a1a',
        plot_bgcolor='#191a1a',
    )

    return go.Figure(
        data=data,  # 54b4e4
        layout=layout
    )



# CHART 2

@app.callback(
    Output('graph-2', 'figure'),
    [Input('date-slider', 'value')]
)


def update_graph_2(year_value):
	bars = []
	bar = go.Bar(
    			{'x':df['Film'], 'y': df['IMDB'], 'name': 'IMDB Score'},
    			#{'x':df['Film'], 'y': df['IMDB'], 'type': 'bar', 'name': 'IMDB Score'},

    			###### UNCOMMENT OUT LINE BELOW FOR ROTTEN SCORES!!! ########
    			{'x':df['Film'], 'y': df['Rotten'], 'name': 'Rotten Tomatoes Score'},

    			#{'x':df['Film'], 'y': df['Rotten'], 'type': 'bar', 'name': 'Rotten Tomatoes Score'}
    			#marker=dict(
        		#color='rgb(158,202,225)',
        		#line=dict(
            	#color='rgb(8,48,107)'
            	#width=1.5
        				)
    					
    			#opacity=0.6
				
	bars.append(bar)
	data = go.Data(bars
                   #style={
                       #'color': '#000'}
                       ) 
	layout = go.Layout(
        yaxis=dict(
            title='Year',
            autorange=True,
            zeroline=True,
            gridwidth=1,
            zerolinecolor='rgb(255, 255, 255)',
            zerolinewidth=2,
        ),
        hoverlabel={
            'bgcolor': '#FFF',
            'font': {
                'color': 'black'
            },
        },
        margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
        hovermode='closest',
        paper_bgcolor='#191a1a',
        plot_bgcolor='#191a1a',
    					)
	return go.Figure(
		data=data, 
		layout=layout
    	)



@app.callback(
    Output('graph-3', 'figure'),
    [Input('date-slider', 'value')]
)


def update_graph_3(year_value):


    dff = df[df['Year'] == year_value]
    data = go.Data([
        go.Scatter(
            x=dff['Gore'],
            y=dff['Jump'],
            text=dff['Film'],
            mode='markers',
            marker={
                'symbol': 'circle',
                'size': dff['Scary'],
                'color': '#C2FF0A'
            },
            hoverlabel={
                'bgcolor': '#FFF',
                'font': {
                    'color': 'black'
                },
            },
        )
    ],
        #style={
        #'color': '#FFF'}
        )

    layout = go.Layout(
        autosize=True,
        xaxis={
            'color': '#FFF',
            'autorange': True,
            'title': 'Gore',
        },
        yaxis={
            'color': '#FFF',
            'autorange': True,
            'title': 'Jump',
        },
        margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
        hovermode='closest',
        paper_bgcolor='#191a1a',
        plot_bgcolor='#191a1a',
    )

    return go.Figure(
        data=data,
        layout=layout
    )


@app.callback(
    Output('graph-4', 'figure'),
    [Input('date-slider', 'value')]
)

def update_graph_4(year_value):


    dff = df[df['Year'] == year_value] 

    data = go.Data([
        go.Scattermapbox(
            lat=dff['lat'],
            lon=dff['lon'],
            mode='markers',
            marker=go.Marker(
                size=dff['Scary'],
                colorscale=color_scale,
                cmin=dff['Scary'].min(),
                color=dff['Scary'],
                cmax=dff['Scary'].max(),
                colorbar=dict(
                    title='Total Scares Across The Globe'
                ),
                opacity=0.5
            ),
            text=dff['Film'],
            #hoverlabel={
                #'bordercolor': 'transparent',
                #'font': {
                    #'color': '#FFF'
                #}
            #}
        )
    ],
        #style={
        #'height': 800
    #}
    )

    layout = go.Layout(
        autosize=True,
        hovermode='closest',
        mapbox=dict(
            accesstoken=mapbox_access_token,
            bearing=0,
            pitch=0,
            zoom=1.8,
            style='dark'
        ),
        paper_bgcolor='#191a1a',
        plot_bgcolor='#191a1a',
    )

    return go.Figure(
        data=data,
        layout=layout
    )




# Run Dash Server

if __name__ == '__main__':
    app.run_server(debug=True)
















