import base64
import io
import pandas as pd
import dash_html_components as html
import dash_table
import plotly.graph_objs as go
from plotly import tools
from flask import session
from pathlib import Path

#save data for extraction...
def save_data(data, filename, ty):
    path = str(Path("tmp/"+session['username']+"/"+filename))
    #path = str(Path("tmp/"+filename))
    
    if ty=='csv':
        data.to_csv(path, index=False)
    elif ty=='xls':
        data.to_excel(path, index=False)

#process preview for uploaded file...
def process_data(contents, filename):
    content_type, content_string = contents.split(',')
    print(content_type)
    decoded = base64.b64decode(content_string)
    
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
            save_data(df, filename, 'csv')
            df1 = df.head()

        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
            save_data(df, filename, 'xls')
            df1 = df.head()
            
        else:
            return html.Div([
                html.H2([
                    'File format Handler unAvailable for '+ filename
                    ],
                    style={'color': 'tomato'}),
                html.Hr(
                    id='hr1',
                    style={
                        'marginBottom': '3%'
                        }
                    )
                ])

    except Exception as e:
        print(e)
        return html.Div([
            html.H2([
                'There was an error processing this file-('+filename+'). '+str(e)
            ]),
            html.Hr(id='hr1',style={'marginBottom': '3%'})
        ])

    return html.Div([
        html.H5(
            'DATA UPLOAD SUMMARY  => '+filename+'(head)',
            style={'color': 'wheat'}),
        #html.H6(datetime.datetime.fromtimestamp(date)),

        dash_table.DataTable(
            data=df1.to_dict('rows'),
            columns=[{'name': i, 'id': i} for i in df.columns]
        ),

        #html.Hr(),  # horizontal line

        # For debugging, display the raw contents provided by the web browser
        html.Div('Raw Content', style={'marginTop': '3%', 'color': 'cornflowerblue'}),
        html.Pre(contents[0:37] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all',
            'color': 'cornflowerblue'
        }),

        html.Hr(id='hr1',style={
            'marginBottom': '3%'
        })

    ])

#handle filename requests...
def getFilename(name):
    for fname in name:
        return fname

#handle plots for scatter home graph updates...
def update_scatterHome_graph(data, selected_dropdown_value):
    dff = data[data['country'] == selected_dropdown_value]
    
    traces = []
    traces.append(go.Scatter(
        x=dff.year,
        y=dff.c_newinc,
        opacity=0.7,
        marker={
            'size': 15,
            'line': {'width': 0.5, 'color': 'white'}
        }
    ))

    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={
                'title': 'Year',
                'titlefont': dict(size=18, color='darkgrey'),
                'zeroline': False,
                'ticks': 'outside'
                },
            yaxis={
                'title': selected_dropdown_value,
                'titlefont': dict(size=18, color='darkgrey'),
                'ticks': 'outside'
                },
            margin={'l': 60, 'b': 60, 't': 30, 'r': 20},
            legend={'x': 1, 'y': 1},
            hovermode='closest'
        )
    }

#handle plots for bar home graph updates...
def update_barHome_graph(data, selected_dropdown_value):
    dff = data[data['country'] == selected_dropdown_value]
    
    traces = []
    traces.append(go.Bar(
        x=dff.year,
        y=dff.c_new_tsr,
        opacity=0.7
    ))

    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={
                'title': 'Year',
                'titlefont': dict(size=18, color='darkgrey'),
                'zeroline': False,
                'ticks': 'outside'
                },
            yaxis={
                'title': selected_dropdown_value+'(%)',
                'titlefont': dict(size=18, color='darkgrey'),
                'ticks': 'outside'
                },
            margin={'l': 60, 'b': 60, 't': 30, 'r': 20},
            legend={'x': 1, 'y': 1},
            hovermode='closest'
        )
    }

