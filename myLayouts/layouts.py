#------------------------------> IMPORTS <-----------------------------------------------

import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import os
import pandas as pd

                    ## Second Dash Application

#------------------------------> UPLOAD LAYOUT <-----------------------------------------

layout1 = html.Div(
    id='bodyUpload',
    style={
        'background': '#27293d',
        'margin': '1%',
        'borderRadius': '9px'
        },
    children = html.Div([
        html.H1(
            'Upload New Data',
            id='uploadH1',
            style={
                'marginTop': '3%',
                'align': 'center',
                'fontSize': '2.1rem',
                'color': 'blue',
                'fontStyle': 'oblique'
            }),
        dcc.Upload(
            id = 'upload_data',
            children = html.Div([
                'Drag and Drop or  ',
                html.A('Select a File')
                ],
                style={'color': 'cornflowerblue'}
            ),
            style={
                'width': '80%',
                'height': '70px',
                'textAlign': 'center',
                'fontSize': '17px',
                'fontStyle': 'italic',
                'lineHeight': '50px',
                'borderStyle': 'dashed',
                'borderColor': 'cornflowerblue',
                'borderWidth': '1.5px',
                'borderRadius': '10px',
                'margin': '5% 10%'
            },
            #Allow multiple files...
            multiple=True,
            #Allow certain file types...
            # accept = "text/csv, application/vnd.ms-excel"
        ),
        html.Hr(id='hr1'),
        html.Div(id='show_results')
    ])
)

layout3 = html.Div([
        html.H1(
            'Upload New Data',
            id='uploadH1',
            style={
                'marginTop':'3%',
                'fontSize' : '2.1rem',
                'color' : 'blue',
                'fontStyle' : 'oblique'
                }
        ),
        html.Div([
            html.Form([
                dcc.Input(
                    id= "uploadBtn",
                    type="file",
                    value="",
                    name = "file"
                    ),
                html.Br(),
                html.Button(
                    "submit",
                    type="submit",
                    id = "submitBtn" 
                    )
                ],
                style={
                    'borderStyle': 'dashed',
                    'borderColor': 'cornflowerblue',
                    'borderWidth': '1.5px',
                    'borderRadius': '10px',
                    'margin': '5% 10%',
                    'textAlign': 'center'
                },
                method="POST",
                action ='/uploadfile',
                encType="multipart/form-data"
            ),
            html.Hr(id='hr1')
        ])
    ],
    style={
        'background': '#27293d',
        'margin': '1%',
        'borderRadius': '9px'
    })

#------------------------------> HEADER & FOOTER LAYOUT <--------------------------------

layout2 = html.Div([

    #main wrapper
    dcc.Location(id='urlValidation', refresh=False),
    html.Div([
        #main header
        html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([
                            html.A([
                                html.Img(
                                    #src='assets/img/logo2.png',
                                    src='../static/img/logo2.png',
                                    alt='logo'
                                )
                            ],
                            href='#'
                            )
                        ],
                        className='logo')
                    ],
                    className='col-md-3'
                    ),
                    #profile info
                    html.Div([
                        html.Div([
                            html.Ul([
                                html.Li([
                                    html.I(className='ti-fullscreen')
                                ],
                                id='full-view'
                                ),
                                html.Li([
                                    html.I(className='ti-zoom-out')
                                ],
                                id='full-view-exit')
                            ],
                            className='notification-area')
                        ],
                        className='d-md-inline-block d-block mr-md-4'
                        ),
                        html.Div([
                            html.Div([
                                html.Img(
                                    id='userPic',
                                    className='avatar user-thumb',
                                    alt='avatar'
                                ),
                                html.H4([
                                    html.Label(
                                        'none',
                                        id='userName'
                                        ),
                                    html.I(className='fa fa-angle-down')
                                ],
                                className='user-name dropdown-toggle',
                                **{'data-toggle':'dropdown'}
                                ),
                                html.Div([
                                    html.A(
                                        'Log Out',
                                        className='dropdown-item',
                                        href='/logout'
                                    )
                                ],
                                className='dropdown-menu')
                            ],
                            className='user-profile m-0')
                        ],
                        className='clearfix d-md-inline-block d-block')
                    ],
                    className='col-md-9 clearfix text-right')
                ],
                className='row align-items-center')
            ],
            className='container')
        ],
        className='mainheader-area'
        ),
        #header area ... navigation
        html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([
                            html.Nav([
                                html.Ul([
                                    html.Li([
                                        html.A([
                                            html.I(className='ti-dashboard'),
                                            html.Span('home')
                                        ],
                                        href='javascript:void(0)'
                                        ),
                                        html.Ul([
                                            html.Li([
                                                html.A(
                                                    'Dashboard',
                                                    href='/'
                                                    )
                                            ])
                                        ],
                                        className='submenu')
                                    ]),
                                    html.Li([
                                        html.A([
                                            html.I(className='ti-slice'),
                                            html.Span('Add new...')
                                        ],
                                        href='javascript:void(0)'
                                        ),
                                        html.Ul([
                                            html.Li([
                                                dcc.Link(
                                                    'CSV',
                                                    href='/upload/'
                                                )
                                            ]),
                                            html.Li([
                                                dcc.Link(
                                                    'XLS',
                                                    href='/upload/'
                                                )
                                            ]),
                                            # html.Li([
                                            #     dcc.Link(
                                            #         'TXT',
                                            #         href='/uploading/'
                                            #     )
                                            # ]),
                                            # html.Li([
                                            #     dcc.Link(
                                            #         'JSON',
                                            #         href='/uploading/'
                                            #     )
                                            # ])
                                        ],
                                        className='submenu')
                                    ]),
                                    html.Li([
                                        html.A([
                                            html.I(className='ti-pie-chart'),
                                            html.Span('Charts')
                                        ],
                                        href='javascript:void(0)'
                                        ),
                                        html.Ul([
                                            html.Li([
                                                html.A(
                                                    'All Charts',
                                                    href='/charts'
                                                )
                                            ])
                                        ],
                                        className='submenu')
                                    ]),
                                    html.Li([
                                        html.A([
                                            html.I(className='fa fa-table'),
                                            html.Span('Tables')
                                        ],
                                        href='javascript:void(0)'
                                        ),
                                        html.Ul([
                                            html.Li([
                                                dcc.Link(
                                                    'Data Table',
                                                    href='/tables/'
                                                )
                                            ])
                                        ],
                                        className='submenu')
                                    ]),
                                    # html.Li([
                                    #     html.A([
                                    #         html.I(className='ti-map-alt'),
                                    #         html.Span('Maps')
                                    #     ],
                                    #     href='/maps')
                                    # ]),
                                    # html.Li([
                                    #     html.A([
                                    #         html.I(className='ti-help'),
                                    #         html.Span('Help')
                                    #     ],
                                    #     href='javascript:void(0)'
                                    #     ),
                                    #     html.Ul([
                                    #         html.Li([
                                    #             dcc.Link(
                                    #                 'About System',
                                    #                 href='/summary/'
                                    #             )
                                    #         ]),
                                    #         html.Li([
                                    #             html.A(
                                    #                 'Contacts',
                                    #                 href=''
                                    #             )
                                    #         ]),
                                    #         html.Li([
                                    #             html.A(
                                    #                 'System Info',
                                    #                 href=''
                                    #             )
                                    #         ])
                                    #     ],
                                    #     className='submenu')
                                    # ]),
                                ],
                                id='nav_menu')
                            ])
                        ],
                        className='horizontal-menu'
                        )
                    ],
                    className='col-lg-9 d-none d-lg-block'
                    ),                    
                    
                    #mobile menu
                    html.Div([
                        html.Div(id='mobile_menu')
                    ],
                    className='col-12 d-block d-lg-none'
                    ),

                    #time
                    html.Div(
                        id='clockbox',
                        className='clearfix d-md-inline-block d-block',
                        style={'color': 'wheat'}
                        )
                ],
                className='row align-items-center')
            ],
            className='container')
        ],
        className='header-area header-bottom'
        ),

        #preloader
        html.Div([
            html.Div([
                html.Div(id='loader'),
                html.Div(className='loader-section section-left'),
                html.Div(className='loader-section section-right')
            ],
            id='loader-wrapper'
            ),
            
            html.Div([
                #main content area
                html.Div(
                    id='bodyHome',
                    className='main-content-inner'
                ),
            ])
        ],
        id='demo-content'),

        #footer
        # html.Footer([
        #     html.Div([
        #         html.P([
        #             '© Copyright 2022. All right reserved. ',
        #             # html.A(
        #             #     '#teammulaga',
        #             #     href=''
        #             # )
        #         ],
        #         # style={'marginTop': '23%'}
        #         )
        #     ],
        #     className='footer-area')
        # ],
        # id='footer',
        # style={'background':'#27293d'})
    ],
    className='horizontal-main-wrapper'
    ),

    # Hidden div inside the app that stores the dataset values...
    html.Div(id='storageDiv', style={'display': 'none'}),
    html.Div(id='storageDiv2', style={'display': 'none'}),
    #hidden div inside the app that stores the uploaded file name...
    html.Div(id='fileNames', style={'display': 'none'})
    
],
className='body-bg',
id='body_home')

#------------------------------> DASHBOARD LAYOUT <--------------------------------------

layout4 = html.Div([
    html.Div([
        #dummy input to trigger chart load..
        # dcc.Dropdown(
        #         id='dummyInput',
        #         value='chris',
        #         style={
        #             'display': 'none'
        #         }
        #     ),
        #interval for watchdog...
        # dcc.Interval(
        #     id='interval-component',
        #     interval=1*30000, # in milliseconds
        #     n_intervals=0
        # ),

        html.Div([
            html.Div(
                id='live-update-text',
                style={'display': 'none'}
                ),

            #first Graph...
            # html.Div([
            #     html.Div([
            #         html.Div([
            #             # dcc.Loading(
            #             #     id='loading-main',
            #             #     children=[
            #                     html.Div([
            #                         html.Div([
            #                             dcc.Graph(
            #                                 id='dbdGraphMain',
            #                                 animate=True
            #                             )
            #                         ],
            #                         className='chart-area')
            #                     ],
            #                     className='card-body')
            #             #     ],
            #             #     # type='graph',
            #             #     fullscreen=False
            #             # )
            #         ],
            #         className='card card-chart')
            #     ],
            #     className='col-12')
            # ],
            # className='row'
            # ),

            #second row graphs...
            # html.Div([
            #     #chart 1
            #     html.Div([
            #         html.Div([
            #             html.Div([
            #                 dcc.Loading(
            #                     id='loading-1',
            #                     children=[
            #                         html.Div([
            #                             dcc.Graph(
            #                                 id='dbdGraph1'
            #                             )
            #                         ],
            #                         className='chart-area')
            #                     ],
            #                     type='circle',
            #                     fullscreen=False
            #                 )
            #             ],
            #             className='card-body')
            #         ],
            #         className='card card-chart')
            #     ],
            #     className='col-lg-6'
            #     ),
            #     #chart 2
            #     html.Div([
            #         html.Div([
            #             html.Div([
            #                 dcc.Loading(
            #                     id='loading-2',
            #                     children=[
            #                         html.Div([
            #                             dcc.Graph(
            #                                 id='dbdGraph2'
            #                             )
            #                         ],
            #                         className='chart-area')
            #                     ],
            #                     type='circle',
            #                     fullscreen=False
            #                 )
            #             ],
            #             className='card-body')
            #         ],
            #         className='card card-chart')
            #     ],
            #     className='col-lg-6'
            #     ),
            #     #chart 3
            #     # html.Div([
            #     #     html.Div([
            #     #         html.Div([
            #     #             dcc.Loading(
            #     #                 id='loading-3',
            #     #                 children=[
            #     #                     html.Div([
            #     #                         dcc.Graph(
            #     #                             id='dbdGraph3' 
            #     #                         )
            #     #                     ],
            #     #                     className='chart-area')
            #     #                 ],
            #     #                 type='circle',
            #     #                 fullscreen=False
            #     #             )
            #     #         ],
            #     #         className='card-body')
            #     #     ],
            #     #     className='card card-chart')
            #     # ],
            #     # className='col-lg-4')
            # ],
            # className='row')
        ],
        className='content')
    ],
    className='main-panel')
],
className='wrapper ')


#------------------------------> DATATABLE LAYOUT <--------------------------------------

layout5 = html.Div([
    html.Div([
        html.H1(
            'Source Dataset',
            style={'color' : 'wheat'}
            )
    ],
    style={'margin': '10px'},
    className='card'),

    # html.Div([
    #     html.Div([
    #         dcc.RadioItems(
    #             id='dataSource',
    #             options=[
    #                 {'label': 'Notifications', 'value': 'not'},
    #                 {'label': 'Outcomes', 'value': 'out'}
    #             ],
    #             value='out'
    #         )
    #     ],
    #     style={
    #         'margin': '5%',
    #         'borderStyle': 'double',
    #         'borderRadius': '8px'
    #     })
    # ],
    # className='card',
    # style={
    #     'marginLeft': '35%',
    #     'marginRight': '35%',
    #     'width' : '20%'
    # }),

    html.Div([
        html.Div(
            id='datatable',
            style={
                'color': 'blue',
                # 'fontSize': '0.5rem',
                # 'fontFamily': 'sans-serif'
            })
    ],
    style={'margin': '10px'},
    # className='card'
    ),

])