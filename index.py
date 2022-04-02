#------------------------------> IMPORTS <-------------------------------------------------------

import os
import shutil
import datetime
import pandas as pd
import sqlite3
from pathlib import Path
from datetime import datetime

#flask imports...
from flask import Flask, redirect, url_for, request, session, render_template
from werkzeug.serving import run_simple
from werkzeug.utils import secure_filename
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
from myClasses.controller import processData

#dash imports...
from dash import Dash
import dash_table
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State

#Layouts...
from myLayouts.layouts import layout1 as uploadLayout
from myLayouts.layouts import layout2 as headerLayout
from myLayouts.layouts import layout3 as uploadFileLayout
from myLayouts.layouts import layout4 as dashboardLayout
from myLayouts.layouts import layout5 as datatableLayout
from myLayouts.layouts import layout6 as mineLayout
# from myLayouts.layouts import layout20 as mapLayout

#handlers...
from myLayouts.handlers import process_data
from myLayouts.handlers import getFilename

#plotly imports...
import plotly.graph_objs as go

#------------------------------> APP CONFIGURATIONS <--------------------------------------------

#Flask configurations...
cwd = os.getcwd()
server = Flask(__name__)
server.config.update(
    DEBUG = True,
    SECRET_KEY = 'secret_xxx'
)
UPLOAD_FOLDER = cwd + '/tmp/'
ALLOWED_EXTENSIONS = set(['xlsx','csv','xls'])
server.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
isDataAvailable = False

#Dash configurations...
# dash_app1 = Dash(__name__, server = server, url_base_pathname='/charts/' )
dash_app2 = Dash(__name__, server = server, external_stylesheets=['/static/css/main.css'], url_base_pathname='/home/')

dash_app2.config['suppress_callback_exceptions']=True
# dash_app1.config['suppress_callback_exceptions']=True
# dash_app1.title = 'Charts'
dash_app2.title = 'Analytics'

dash_app2.layout = headerLayout
# dash_app1.layout = chartsLayout

#------------------------------> LOGIN MANAGEMENT <------------------------------------------

# flask-login...
login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = "login"

#user model...
class User(UserMixin):

    def __init__(self, id):
        self.id = id
        self.name = str(id)
        
    def __repr__(self):
        return "%d/%s" % (self.id, self.name)

#validate user Login...
def validate(username, password):
    dbFile = Path('static/User.db')
    con = sqlite3.connect(str(dbFile))
    valid = False

    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Users")
        rows = cur.fetchall()
        for row in rows:
            dbUser = row[0]
            dbPass = row[1]
            if dbUser==username:
                if dbPass == password:
                    valid = True

    con.close()
    return valid

#add new user account...
def log_user(logs):
    # datetime object containing current date and time
    now = datetime.now()
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d-%m-%Y %H:%M:%S")

    details = (logs, dt_string)
    try:
        con = sqlite3.connect(str(Path('static/User.db')))
    except Exception as e:
        print('Error in logging User: '+str(e))
        return False

    sql = "INSERT INTO logs (username, time) VALUES(?,?)"
    cur = con.cursor()
    cur.execute(sql, details)
    con.commit()
    con.close()
    return True

#add new user account...
def register(details):
    try:
        con = sqlite3.connect(str(Path('static/User.db')))
    except Exception as e:
        print('Error in creating User: '+str(e))
        return False

    sql = 'INSERT INTO users (USERNAME, PASSWORD) VALUES(?,?)'
    cur = con.cursor()
    cur.execute(sql, details)
    con.commit()
    con.close()
    return True

#route to login...
@server.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        if request.form['submitBtn'] == 'Login':
            username = request.form['username']
            password = request.form['password']

            valid = validate(username, password)       
            if valid:
                id = username
                user = User(id)
                login_user(user)
                session['username'] = username
                log_user(username)
                nextPage = str(request.args.get("next"))
                #create user temp folder...
                try:
                    os.mkdir(server.config['UPLOAD_FOLDER']+"/"+session['username'])
                except:
                    print("Directory exists, creation cancelled")

                print('required page is '+nextPage)
                #check validity of requested page...
                if nextPage != 'None':
                    return redirect(request.args.get("next"))
                else:
                    return redirect('/')
            else:
                return render_template('login.html', error='Invalid Credentials')

        elif request.form['submitBtn'] == 'Sign Up':
            username = request.form['uname']
            password = request.form['pass']
            password1 = request.form['pass1']

            if username != "" and password != "" and password1 != "":
                if password == password1:
                    userdetails = (username, password)
                    registered = register(userdetails)
                    if registered:
                        return render_template('login.html', info='Account Created')
                    else:
                        return render_template('login.html', info='Account Creation Failed')

                else:
                    return render_template('login.html', error='Passwords Error! Try Again')

            else:
                return render_template('login.html', error='Fields Empty! Try Again')

        else:
            return render_template('login.html')

    else:
        return render_template('login.html')

#route to logout...
@server.route("/logout")
@login_required
def logout():
    logout_user()
    try:
      shutil.rmtree(server.config['UPLOAD_FOLDER']+"/"+session['username'])
    except:
      print("Error in deleting old user files")
    session.pop('username', None)
    return redirect(url_for('login'))
   
# callback to reload the user object...   
@login_manager.user_loader
def load_user(userid):
    return User(userid)

#------------------------------> SOME REQUIRED METHODS <----------------------------------------

#method to check if uploaded file has supported extension...
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

#watchdog required method...
def modification_date(filename):
    t = os.path.getmtime(filename)
    return datetime.fromtimestamp(t)

#handle page not found
@server.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404
 
#method to protect our apps from unregistered members...
def protect_views(app):
    for view_func in app.server.view_functions:
        if view_func.startswith(app.config['url_base_pathname']):
            app.server.view_functions[view_func] = login_required(app.server.view_functions[view_func])
    
    return app

#handle root url...
@server.route('/')
@login_required
def dashboard():
    return redirect('/home')

#handle file uploads...
@server.route('/uploadfile', methods = ['GET', 'POST'])
@login_required
def uploaded_file():
    if request.method == 'POST':
       
       file = request.files['file']
       if file and allowed_file(file.filename):
          filename = secure_filename(file.filename)
          #file.save(os.path.join(server.config['UPLOAD_FOLDER'], filename))
          file.save(os.path.join(server.config['UPLOAD_FOLDER'] +"/"+ session['username'], filename))
          print("file uploaded, redirecting")
          print('Path is -> '+str(cwd))

    return redirect(url_for('processing', filenam = filename))

#handle uploaded file...
@server.route('/processing/<filenam>')
@login_required
def processing(filenam):
    if filenam != '':
        try:
            processStatus = processData(filenam)
            if processStatus:
                print('processing successful')
                return redirect('/')
            else:
                return "<h1>An Error occurred during file processing. ref:[index(272)]</h1><p><a href='/'>Home Page</a></p>"
        except Exception as e:
            print('Error: '+str(e))
            return "<h1>An Unknown Error occurred. ref:[index(274)]</h1><p><a href='/'>Home Page</a></p>"
    
    else:
        print('failed to process file')
        return '<h1>Usatijairire..!! Check File Type. (CSV, XLS, XLSX)</h1>'

#------------------------------> CALLBACKS TO HANDLE USER EVENTS <------------------------------

#load data for app2 into system...
@dash_app2.callback(Output('storageDiv', 'children'),
                    [Input('body_home', 'children')])
def load_data(children ):
    # print("inside first callback")
    try:
        df =  pd.read_csv(str(Path('data\\new_data.csv')))
        if df.empty != True:
            # print("Data found")
            global isDataAvailable
            isDataAvailable = True
            return df.to_json(date_format='iso', orient='split')

    except:
        print("Data not found..")
        isDataAvailable = False
        return ''
    
#update logged in username...
@dash_app2.callback(Output('userName', 'children'),[Input('body_home', 'children')])
def get_User(children):
	return session['username']

#update logged in user picture...
@dash_app2.callback(Output('userPic', 'src'),[Input('userName','children')])
def get_Userpic(children):
    # print(children + ' is logged in')
    return '../static/img/'+children+'.png'

#update dashboard product count...
@dash_app2.callback(Output('productCount', 'children'),
                    [Input('storageDiv', 'children')])
def update_productsCount(data1):
    # print('4th callback')
    if isDataAvailable:
        df = pd.read_csv('data\\new_data.csv')
        myCount = df.StockCode.unique().size

    else:
        myCount = 0

    return myCount

#update dashboard customer count...
@dash_app2.callback(Output('customerCount', 'children'),
                    [Input('storageDiv', 'children')])
def update_customersCount(data1):
    # print('5th callback')
    if isDataAvailable:
        df = pd.read_csv('data\\new_data.csv')
        myCount = df.CustomerID.unique().size

    else:
        myCount = 0

    return myCount

#update dashboard locations count...
@dash_app2.callback(Output('locationCount', 'children'),
                    [Input('storageDiv', 'children')])
def update_locationsCount(data1):
    # print('6th callback')
    if isDataAvailable:
        df = pd.read_csv('data\\new_data.csv')
        myCount = df.Country.unique().size

    else:
        myCount = 0

    return myCount

#update dashboard main graph...
@dash_app2.callback(Output('dbdGraphMain', 'figure'),
                    [Input('storageDiv', 'children'), Input('live-update-text', 'children')])
def update_Main_dbd(data1, updated):
    data = pd.read_csv('data\\new_data.csv')

    yvalues = []
    xvalues = data['InvoiceDate'].unique()
    for year in xvalues:
        y = data[data.InvoiceDate == year]
        yv = y.Quantity.sum()
        yvalues.append(yv)

    figu = {
        'data': [
            go.Scatter(
                x=xvalues,
                y=yvalues,
                opacity=0.5,
                line = {
                    'width': 5,
                    'shape': 'spline'
                }
                )
            ],

        'layout': go.Layout(
            xaxis={
                'title': 'Date & Time',
                'titlefont': dict(size=18, color='wheat'),
                'zeroline': False,
                'ticks': 'outside'
                },
            yaxis={
                'title': 'Product Quantities',
                'titlefont': dict(size=18, color='wheat'),
                'ticks': 'outside'
                },
            margin={'l': 60, 'b': 60, 't': 30, 'r': 20},
            legend={'x': 1, 'y': 1},
            hovermode='closest',
            plot_bgcolor= '#27293d',
            paper_bgcolor='#27293d',
            font={'color':'#e14eca'},
            title='Products Buying Statistics'
        )
    }

    return figu

#update dashboard chart-2...
@dash_app2.callback(Output('dbdGraph2', 'figure'),
                    [Input('storageDiv', 'children'), Input('live-update-text', 'children')])
def update_deathsGraph(data1, updated):
    df = pd.read_csv('data\\new_data.csv')

    yvalues = []
    xvalues = df.Description.unique()[:5]
    for stock in xvalues:
        y = df[df.Description == stock]
        yv = y.Quantity.sum()
        yvalues.append(yv)

    figur={
        'data':[
            {
                'x':xvalues,
                'y':yvalues,
                'type':'bar',
                'marker':{
                    'color':'purple',
                    'line': {
                        'color':'rgb(158,202,225)',
                        'width':1.5
                        }
                },
                'opacity':0.6
            }
        ],
        'layout': {
            'plot_bgcolor': '#27293d',
            'paper_bgcolor': '#27293d',
            'yaxis': {
                'title': 'Quantity',
                'titlefont': dict(size=18, color='wheat'),
                'ticks': 'outside'
            },
            'xaxis': {
                'title': 'Product',
                'titlefont': dict(size=14, color='lime')
            },
            'font':{
                'color': '#e14eca'
            },
            'title': 'Overview of 5 Most Sought Products'
        }
    }

    return figur

#update dashboard chart-3...
@dash_app2.callback(Output('dbdGraph3','figure'),
                    [Input('storageDiv', 'children'), Input('live-update-text', 'children')])
def update_Chart3_dbd(data1, updated):
    df = pd.read_csv('data\\new_data.csv')

    yvalues = []
    xvalues = df.Country.unique()
    for locate in xvalues:
        y = df[df.Country == locate]
        yv = y.Quantity.sum()
        yvalues.append(yv)

    figur={
        'data':[
            {
                'x':xvalues,
                'y':yvalues,
                'type':'bar',
                'marker':{
                    'color':'#e14eca',
                    'line': {
                        'color':'rgb(158,202,225)',
                        'width':1.5
                        }
                },
                'opacity':0.6
            }
        ],
        'layout': {
            'plot_bgcolor': '#27293d',
            'paper_bgcolor': '#27293d',
            'yaxis': {
                'title': 'Quantity of Products',
                'titlefont': dict(size=18, color='wheat'),
                'ticks': 'outside'
            },
            'xaxis': {
                'title': 'Locations',
                'titlefont': dict(size=14, color='lime')
            },
            'font':{
                'color': '#e14eca'
            },
            'title': 'Overview of Product Quantity by Locations'
        }
    }

    return figur

#validate url path for page layouts...
@dash_app2.callback(Output('bodyHome', 'children'),
              [Input('urlValidation', 'pathname')])
def display_page(pathname):
    if isDataAvailable:
        if pathname == "/home/":
            return dashboardLayout
        
        elif pathname == "/upload/":
            return uploadLayout

        elif pathname == "/uploading/":
            return uploadFileLayout

        elif pathname == "/tables/":
            return datatableLayout
            
        elif pathname == "/mining/":
            return mineLayout

        else:
            return pathname

    else:
        if pathname == "/upload/":
            return uploadLayout

        elif pathname == "/uploading/":
            return uploadFileLayout

        else:
            return html.Div(
                html.H3(
                    'No Data Found or Not Loaded',
                    style={
                        'marginTop': '10%',
                        'marginBottom': '6%',
                        'color': 'red'
                    })
            )

#update upload file preview...
@dash_app2.callback(
    Output('show_results','children'),
    [Input('upload_data', 'contents')],
    [State('upload_data', 'filename')]
)
def update_output(content, names):
    if content != None:
        children = [
            process_data(c, n) for c, n in
            zip(content, names)]
        return children + [
        dcc.Link(
            html.Button(
                'Proceed',
                id='proBtn'
            ),
            refresh=True,
            href=url_for('processing', filenam=getFilename(names))
            #id='proBtn'
        ),

        html.Hr(id='hr2')]

#update the uploaded filenames...
@dash_app2.callback(Output('fileNames', 'children'),[Input('upload_data', 'filename')])
def get_upload_file_name(name):
    return name

#update datatable accordingly...
@dash_app2.callback(Output('datatable', 'children'),
            [Input('storageDiv', 'children')])
def updateDatatable(tbDataa):
    noty_data = pd.read_json(tbDataa, orient='split')
    
    if (True):
        return dash_table.DataTable(
                    columns=[{"name": i, "id": i} for i in noty_data.columns],
                    data=noty_data.to_dict("rows")
                ) 

    else:
        return html.H3('No Data Source..')


#------------------------------> MINING AREA CALLBACKS <----------------------------------------

#load dropdown country options...
@dash_app2.callback(Output('dropdownCountry', 'options'),
     [Input('storageDiv', 'children')])
def load_country_options(data):
    dff = pd.read_json(data, orient='split')
    # print(dff)
    try:
        options = dff['Description'].unique()
    except:
        return [{}]

    return [
            {'label': i, 'value': i} for i in options
        ]

# update options for graph manipulation...
@dash_app2.callback(Output('graphOptions', 'children'),
                    [Input('chartType', 'value'), Input('chartArea', 'children'),
                    Input('storageDiv', 'children')])
def update_graphOptions(value, dummy, data):
    dff = pd.read_json(data, orient='split')
    # options = value + ' Options not available'
    # print(options)
    
    if value != 'pie':
        options = html.Div([
            html.Div([
                'X-axis:',
                dcc.Dropdown(
                    id='dropdownValue1',
                    options = [{'label': i, 'value': i} for i in dff.columns.unique()],
                    placeholder='Select Value...',
                    value = 'Country',
                    style={'width': '50%', 'margin': '3px'}
                ),
                'Y-axis:',
                dcc.Dropdown(
                    id='dropdownValue2',
                    options = [{'label': i, 'value': i} for i in dff.columns.unique()],
                    placeholder='Select Value...',
                    value = 'Quantity',
                    style={'width': '50%', 'margin': '3px'}
                )
            ],
            style={'display': 'flex'})
                    
        ])

    elif value == 'pie':
        options = html.Div([
            # dcc.RadioItems(
            #     id='tbType',
            #     options=[
            #         {'label': 'XDR-TB', 'value': 'xdr'},
            #         {'label': 'MDR-TB', 'value': 'mdr'},
            #         {'label': 'HIV-TB', 'value': 'hiv'}
            #     ],
            #     value='hiv',
            #     labelStyle={'display': 'inline-block'}
            # )
            'Pie Chart Options not Available'
        ],
        className='p-2')

    return options

#update chart area...
@dash_app2.callback(Output('chartArea', 'children'), [Input('chartType', 'value')])
def upadte_graphType(ctype):
    figu = {}

    return dcc.Loading(
            id='loading-main',
            children=[
                dcc.Graph(
                    id=ctype + 'Graph',
                    figure=figu
                )
            ],
            type='circle',
            fullscreen=False
        ) 

#update chart plot diagram (bar)...
@dash_app2.callback(Output('barGraph', 'figure'),
              [Input('storageDiv', 'children'), Input('dropdownCountry', 'value'),
               Input('dropdownValue1', 'value'), Input('dropdownValue2', 'value')])
def update_bar(data1, vCountry, xValue, yValue):
    data = pd.read_json(data1, orient='split')

    if vCountry != 'all':
        dff = data[data['Description'] == vCountry ]
        traces = []
        traces.append(go.Bar(
            # x=dff.Country,
            # y=dff.Quantity,
            x = dff[xValue],
            y = dff[yValue],
            opacity = 0.7
        ))

        return {
            'data': traces,
            'layout': go.Layout(
                xaxis={
                    'title': 'Location',
                    'titlefont': dict(size=18, color='darkgrey'),
                    'zeroline': False,
                    'ticks': 'outside'
                    },
                yaxis={
                    'title': vCountry + ' Quantity',
                    'titlefont': dict(size=18, color='darkgrey'),
                    'ticks': 'outside'
                    },
                    title='Product Buying per Location',
                margin={'l': 60, 'b': 60, 't': 30, 'r': 20},
                legend={'x': 1, 'y': 1},
                hovermode='closest',
                paper_bgcolor='#27293d',
                plot_bgcolor='#27293d',
                font={'color':'#e14eca'}
            )
        }

    else:
        dff = data
        traces = []
        traces.append(go.Bar(
            # x=dff.Country,
            # y=dff.Quantity,
            x = dff[xValue],
            y = dff[yValue],
            opacity=0.7
        ))
        return {
                'data': traces,
                'layout': go.Layout(
                    xaxis={
                        'title': 'Location',
                        'titlefont': dict(size=18, color='darkgrey'),
                        'zeroline': False,
                        'ticks': 'outside'
                        },
                    yaxis={
                        'title': 'Products Quantities',
                        'titlefont': dict(size=18, color='darkgrey'),
                        'ticks': 'outside'
                        },
                    margin={'l': 60, 'b': 60, 't': 30, 'r': 20},
                    legend={'x': 1, 'y': 1},
                    hovermode='closest',
                    title='Products Buying per Location',
                    paper_bgcolor='#27293d',
                    plot_bgcolor='#27293d',
                    font={'color':'#e14eca'}
                )
            }

#update chart plot diagram (scatter)...
@dash_app2.callback(Output('scatterGraph', 'figure'),
              [Input('storageDiv', 'children'), Input('dropdownCountry', 'value'),
               Input('dropdownValue1', 'value'), Input('dropdownValue2', 'value')])
def update_scatter(theData, vCountry, xValue, yValue):
    data = pd.read_json(theData, orient='split')

    if vCountry != 'all':
        # print('all: ' + vCountry)
        dff = data[data['Description'] == vCountry ]
        traces = []
        traces.append(go.Scatter(
            x=dff.Country,
            y=dff.Quantity,
            opacity=0.7,
            mode='markers',
            marker={
                'size': 15,
                'line': {'width': 0.5, 'color': 'white'}
            }
        ))

        return {
            'data': traces,
            'layout': go.Layout(
                xaxis={
                    'title': 'Location',
                    'titlefont': dict(size=18, color='darkgrey'),
                    'zeroline': False,
                    'ticks': 'outside'
                    },
                yaxis={
                    'title': vCountry,
                    'titlefont': dict(size=18, color='darkgrey'),
                    'ticks': 'outside'
                    },
                title='Product Buying Distribution',
                margin={'l': 60, 'b': 60, 't': 30, 'r': 20},
                legend={'x': 1, 'y': 1},
                hovermode='closest',
                paper_bgcolor='#27293d',
                plot_bgcolor='#27293d',
                font={'color':'#e14eca'}
            )
        }

    else:
        return {
            'data': [
                go.Scatter(
                    x=data[data['Country'] == i],
                    y=data[data['Country'] == i]['Quantity'],
                    # text=data[data['Country'] == i]['Quantity'],
                    mode='markers',
                    opacity=0.7,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                        },
                    name=i
                    ) for i in data.Country.unique()
                ],

            'layout': go.Layout(
                xaxis={
                    'title': 'Location',
                    'titlefont': dict(size=18, color='lime'),
                    'zeroline': False,
                    'ticks': 'outside'
                    },
                yaxis={
                    'title': 'Quantity',
                    'titlefont': dict(size=18, color='lime'),
                    'ticks': 'outside'
                    },
                margin={'l': 60, 'b': 60, 't': 30, 'r': 20},
                legend={'x': 1, 'y': 1},
                hovermode='closest',
                title='Buying Behaviours',
                paper_bgcolor='#27293d',
                plot_bgcolor='#27293d',
                font={'color':'#e14eca'}
            )
        }

#update chart plot diagram (pie)...
@dash_app2.callback(Output('pieGraph', 'figure'),
              [Input('storageDiv', 'children'), Input('dropdownCountry', 'value'),
              Input('sliderYear', 'value')])
def update_pie(theData, vCountry, vYear):
    dat = pd.read_json(theData, orient='split')
    
    if vCountry != 'all':
        df = dat[dat['Description'] == vCountry]
        # data = df[df['year'] == vYear]
        
        labels = df.Country
        values = df.Quantity

    else:
        labels = dat.Country
        values = dat.Quantity
    
    trace = go.Pie(labels=labels, values=values)

    return {
        'data':[
            trace
            ],
        'layout':
            go.Layout(
                    paper_bgcolor='#27293d',
                    plot_bgcolor='#27293d',
                    font={'color':'#e14eca'},
                    title='Products Buying Distribution'
                )
        
        }

#update chart plot diagram (line)...
@dash_app2.callback(Output('lineGraph', 'figure'),
              [Input('storageDiv', 'children'), Input('dropdownCountry', 'value'),
               Input('dropdownValue1', 'value'), Input('dropdownValue2', 'value')])
def update_line(data1, vCountry, xValue, yValue):
    data = pd.read_json(data1, orient='split')

    if vCountry != 'all':
        dff = data[data['Description'] == vCountry ]
        plot = [go.Scatter(
                    x=dff[xValue],
                    y=dff[yValue],
                    # text=dff['year'],
                    opacity=0.7
                )]

    else:
        plot = [go.Scatter(
                    x=data[data['Country'] == i]['Description'],
                    y=data[data['Country'] == i]['Quantity'],
                    text=data[data['Country'] == i]['Description'],
                    opacity=0.7,
                    name=i
                ) for i in data.Country.unique()]

    figu = {
        'data': plot,

        'layout': go.Layout(
            xaxis={
                'title': 'Year',
                'titlefont': dict(size=18, color='wheat'),
                'zeroline': False,
                'ticks': 'outside'
                },
            yaxis={
                'title': 'New Reported Cases',
                'titlefont': dict(size=18, color='wheat'),
                'ticks': 'outside'
                },
            margin={'l': 60, 'b': 60, 't': 30, 'r': 20},
            legend={'x': 1, 'y': 1},
            hovermode='closest',
            plot_bgcolor= '#27293d',
            paper_bgcolor='#27293d',
            font={'color':'#e14eca'},
            title='Reported Cases Statistics'
        )
    }

    return figu




#------------------------------> ENCAPSULATING APPLICATION <-------------------------------------

#protect views...
# dash_app1 = protect_views(dash_app1)
dash_app2 = protect_views(dash_app2)

#------------------------------> RUNNING THE SERVER <--------------------------------------------

#dev server(flask) on port 8000...
run_simple('0.0.0.0', 8000, server, use_reloader=True, use_debugger=True)

