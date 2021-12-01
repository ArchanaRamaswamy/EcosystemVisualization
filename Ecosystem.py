import plotly.express as px

# Library for data manipulation and analysis
import pandas as pd

# Importing dash componants
import dash
# from jupyter_dash import JupyterDash

# For using dash components
from dash import dcc

# use of html tags like div
from dash import html

# For call back
from dash.dependencies import Output, Input

# For displaying the structural elements
import dash_bootstrap_components as dbc

#For chord graph
import pandas as pd
# import holoviews as hv
# from holoviews import opts, dim
import numpy as np

#using dash for chord
import dash_bio as dashbio

#Dash cytoscape
import dash_cytoscape as cyto

# Load data
df = pd.read_csv(r'C:\Users\archa\Documents\Archana\IIS_GoogleDrive\IIS\Thesis\Julius\Application_Panywhere\EcosystemVisualization\Data\Datacsv.csv',
                   header=1,skiprows=1, names=['Roles','Actors','Resources','Activities','value contribution in ecosystem','Value contribution for the actors','Dependency','RoleInfo'])

# Saving 4 elements into single column. This makes it easy to display the data
df = pd.melt(df, id_vars=['Roles','Actors','Dependency','RoleInfo'],
             value_vars=['Resources','Activities','value contribution in ecosystem','Value contribution for the actors'],
             var_name='results',value_name='StructuralEements')
#Actor data for cytoscape
Myelements = [ #Nodes
                {'data': {'id': 'BTC', 'label': 'BTC Business Technology Consulting AG'},
                 'position': {'x': 150, 'y': 50}, 'classes': 'NodeColor'
                 },

                {'data': {'id': 'Volkswagen', 'label': 'Volkswagen'},
                 'position': {'x': 300, 'y': 150}, 'classes': 'NodeColor'
                 },

                {'data': {'id': 'Lenze', 'label': 'Lenze'},
                 'position': {'x': 200, 'y': 200}, 'classes': 'NodeColor'
                 },

                {'data': {'id': 'Siemens', 'label': 'Siemens AG'},
                 'position': {'x': 190, 'y': 190}, 'classes': 'NodeColor'
                 },

                {'data': {'id': 'RapidMiner', 'label': 'RapidMiner GmbH'},
                 'position': {'x': 160, 'y': 190}, 'classes': 'NodeColor'
                 },

                {'data': {'id': 'slashwhy', 'label': 'Slashwhy'},
                 'position': {'x': 140, 'y': 170}, 'classes': 'NodeColor'
                 },

                {'data': {'id': 'Trump', 'label': 'Trump (Axoom platform)'},
                 'position': {'x': 120, 'y': 150}, 'classes': 'NodeColor'
                 },

                # Links
                {'data': {'source': 'Lenze', 'target': 'Siemens'}, 'classes': 'EdgeColor tri'},
                {'data': {'source': 'Siemens', 'target': 'Volkswagen'}, 'classes': 'EdgeColor tri'},

                {'data': {'source': 'BTC', 'target': 'Volkswagen'}, 'classes': 'EdgeColor SI'},
                {'data': {'source': 'BTC', 'target': 'RapidMiner'}, 'classes': 'EdgeColor SI'},

                {'data': {'source': 'RapidMiner', 'target': 'Volkswagen'}, 'classes': 'EdgeColor tri'},
                {'data': {'source': 'slashwhy', 'target': 'RapidMiner'}, 'classes': 'EdgeColor tri'},

                {'data': {'source': 'Trump', 'target': 'Lenze'}, 'classes': 'EdgeColor PI'},
                {'data': {'source': 'Trump', 'target': 'Siemens'}, 'classes': 'EdgeColor PI'},
                {'data': {'source': 'Trump', 'target': 'Volkswagen'}, 'classes': 'EdgeColor PI'},
                {'data': {'source': 'Trump', 'target': 'RapidMiner'}, 'classes': 'EdgeColor PI'},
                {'data': {'source': 'Trump', 'target': 'BTC'}, 'classes': 'EdgeColor PI'},
                {'data': {'source': 'Trump', 'target': 'slashwhy'}, 'classes': 'EdgeColor PI'},
            ]
# Build App
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

#Layout of all the graphs
app.layout = dbc.Container([
    dbc.Row([
    #Creating treemap
        dbc.Col([
            dcc.Graph(id='treemap',
                      figure=px.treemap(df,
                                        path=[px.Constant('Ecosystem'), 'Roles', 'Actors'],
                                        values='Dependency',
                                        height=600, width=700).update_layout(margin=dict(t=25, r=0, l=5, b=20))
                      )], width=6),
        #Creating cytoscope for actors
        dbc.Col([
            html.Div([
                dcc.Dropdown(
                    id='dpdn',
                    value='breadthfirst',
                    clearable=False,
                    options=[
                        {'label': name.capitalize(), 'value': name}
                        for name in ['breadthfirst' ,'grid', 'random', 'circle', 'cose', 'concentric']
                    ]
                ),
                cyto.Cytoscape(
                    id='cytoscapeActors',
                    autoungrabify = False,
                    minZoom=0.2,
                    maxZoom=1,
                    layout={'name': 'grid', 'rows':3,'cols':3},
                    style={'width': '100%', 'height': '400px'},
                    elements= Myelements,
                    stylesheet=[
                        # Group selectors for NODES
                        {
                            'selector': 'node',
                            'style': {
                                'label': 'data(label)'
                            }
                        },
                        {
                            'selector': 'edge',
                            'style': {
                                'curve-style': 'straight'
                            }
                        },

                        # Group selectors for EDGES
                        # {
                        #     'selector': 'edge',
                        #     'style': {
                        #         'label': 'data(weight)'
                        #     }
                        # },
                        # Class selectors
                        {
                            'selector': '.NodeColor',
                            'style': {
                                'background-color': '#33D5FF',
                                'line-color': '#33D5FF'
                            }
                        },
                        {
                            'selector': '.EdgeColor',
                            'style': {
                                'background-color': '#9433FF',
                                'line-color': '#9433FF'
                            }
                        },
                      {
                            'selector': '.SI',
                            'style': {
                                'target-arrow-color': 'blue',
                                'target-arrow-shape': 'triangle',
                                'line-color': 'red'
                            }
                        },
                        {
                            'selector': '.tri',
                            'style': {
                                'target-arrow-color': 'blue',
                                'target-arrow-shape': 'triangle'
                            }
                        },
                        {
                            'selector': '.PI',
                            'style': {
                                'target-arrow-color': 'blue',
                                'target-arrow-shape': 'triangle',
                                'line-color': 'blue'
                            }
                    ]
                    )]
                )], width =6)
    ]),

    #     Div to display the elements. This will be empty till a brach is cliked in treemap
    dbc.Row([
        dbc.Col([html.Div(id='Elementscontainer')], width=12)
    ])

], fluid=True)

#callback and update for dropdown
@app.callback(Output('cytoscapeActors', 'layout'),
              Input('dpdn', 'value'))
def update_layout(layout_value):
    if layout_value == 'breadthfirst':
        return {
        'name': layout_value,
        'roots': '[id = "Lenze"]',
        'animate': True
        }
    else:
        return {
            'name': layout_value,
            'animate': True
        }

#callback for cytograph actor click (can be used in future)
# @app.callback(
#     Output("Elementscontainer", "children"),
#     Input('cytoscapeActors', 'tapNodeData')
# )
# def update_nodes(data):
#     # print(data)
#     if data is None:
#         return dash.no_update
#     else:
#         label_slct = data['points'][0]['label']
#         parent_slct = data['points'][0]['parent']
#         # Filtering data for selected actor
#         dff = df[(df.Roles == parent_slct) & (df["Actors"] == label_slct)]
#         # create the table
#         table_header = [html.Thead(html.Tr([html.Th(label_slct)]))]
#         rows = []
#         for x in dff["StructuralEements"]:
#             if pd.isnull(x):
#                 continue
#             rows.append(html.Tr([html.Td(x)]))
#         table_body = [html.Tbody(rows)]
#         return dbc.Table(table_header + table_body, bordered=True)


# Define callback to display the structural elememts
@app.callback(
    #     Output("treemap", "figure"),
    Output("Elementscontainer", "children"),
    Input("treemap", "clickData")
)
def update_modal(data):
    # if black frame of treemap, don't update
    if data is None:
        return dash.no_update

        # if no currentpath or ecosystem is chosen, don't update
    elif data['points'][0].get('currentPath') is None \
            or data['points'][0]['percentRoot'] == 1 \
            and data['points'][0]['label'] == 'Ecosystem':
        table_header = " "
        table_body = " "
        return dbc.Table(table_header + table_body, bordered=False)

    # if Role is chosen (ecosystem is parent), don't update
    elif data['points'][0]['label'] in df.Roles.unique():
        label_slct = data['points'][0]['label']
        parent_slct = data['points'][0]['parent']
        # Filtering data for the seleced role
        dff = df[(df.Roles == label_slct)]
        # create the table
        table_header = [html.Thead(html.Tr([html.Th(label_slct)]))]
        table_body = [html.Tbody(dff["RoleInfo"].unique())]
        return dbc.Table(table_header + table_body, bordered=True)

    # if Actor is chosen, build table
    else:
        label_slct = data['points'][0]['label']
        parent_slct = data['points'][0]['parent']
        # Filtering data for selected actor
        dff = df[(df.Roles == parent_slct) & (df["Actors"] == label_slct)]
        # create the table
        table_header = [html.Thead(html.Tr([html.Th(label_slct)]))]
        rows = []
        for x in dff["StructuralEements"]:
            if pd.isnull(x):
                continue
            rows.append(html.B((x.split(":"))[0]))             
            rows.append(html.Tr([html.Td(x)]))
        table_body = [html.Tbody(rows)]
        return dbc.Table(table_header + table_body, bordered=True)


if __name__ == '__main__':
    app.run_server(debug='True')
