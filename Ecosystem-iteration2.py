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

#Dash cytoscape
import dash_cytoscape as cyto

#Pyautogui for scrolling
import pyautogui

import webbrowser

#To make the elements bold
Boldstart = "\033[1m"
Boldend = "\033[0;0m"

def df_style(val):
    return "font-weight: bold"

# Load data
df = pd.read_csv(r'C:\Users\archa\Documents\Archana\IIS_GoogleDrive\IIS\Thesis\Julius\Application_Panywhere\EcosystemVisualization\Data\Datacsv.csv',
                   header=0, names=['Roles','Actors','Resources','Activities','value contribution in ecosystem','Value contribution for the actors','Dependency','RoleInfo'])

# Saving 4 elements into single column. This makes it easy to display the data
df = pd.melt(df, id_vars=['Roles','Actors','Dependency','RoleInfo'],
             value_vars=['Resources','Activities','value contribution in ecosystem','Value contribution for the actors'],
             var_name='results',value_name='StructuralEements')

#Actor data for cytoscape
Myelements = [ #Nodes
                {'data': {'id': 'BTC', 'label': 'BTC Business Technology Consulting AG'},
                 'position': {'x': 150, 'y': 50}, 'classes': 'BTC'
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

                {'data': {'id': 'IIP', 'label': 'Operator Gmbh (IIP platform)'},
                 'position': {'x': 120, 'y': 150}, 'classes': 'IIP'
                 },

                # Links
                {'data': {'source': 'Lenze', 'target': 'Siemens'}, 'classes': 'EdgeColor tri'},
                {'data': {'source': 'Siemens', 'target': 'Volkswagen'}, 'classes': 'EdgeColor tri'},

                {'data': {'source': 'BTC', 'target': 'Volkswagen'}, 'classes': 'EdgeColor SI'},
                {'data': {'source': 'BTC', 'target': 'RapidMiner'}, 'classes': 'EdgeColor SI'},

                {'data': {'source': 'RapidMiner', 'target': 'Volkswagen'}, 'classes': 'EdgeColor tri'},
                {'data': {'source': 'RapidMiner', 'target': 'RapidMiner'}, 'classes': 'EdgeColor tri'},

                {'data': {'source': 'IIP', 'target': 'Lenze'}, 'classes': 'EdgeColor PI'},
                {'data': {'source': 'IIP', 'target': 'Siemens'}, 'classes': 'EdgeColor PI'},
                {'data': {'source': 'IIP', 'target': 'Volkswagen'}, 'classes': 'EdgeColor PI'},
                {'data': {'source': 'IIP', 'target': 'RapidMiner'}, 'classes': 'EdgeColor PI'},
                {'data': {'source': 'IIP', 'target': 'BTC'}, 'classes': 'EdgeColor PI'}
            ]
# Build App
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

#Layout of all the graphs
app.layout = dbc.Container([
    dbc.Row([
    #Creating treemap
        dbc.Col([
            html.Div([
            html.Label(html.Th(['Dependency of actors on Ecosystem. 3 is highest and 1 is lowest'])),
            # strRole = df.Roles,
            dcc.Graph(id='treemap',
                     figure=px.treemap(df, path=[px.Constant('Ecosystem'), 'Roles', 'Actors'],
                            labels={'Dependency'},
                            color='Dependency',
                            values='Dependency',
                            height=600, width=700,
                            # hover_data=['Dependency']
                            ).update_layout(margin=dict(t=25, r=0, l=5, b=20)
                            ).update_traces(hovertext='test',hoverinfo='text'),
                      # hovertemplate='%{currentPath}'
                      )]),
            ], width=6),
        #Creating cytoscope for actors
        dbc.Col([
            html.Div([
                dcc.Dropdown(
                    id='dpdn',
                    value='circle',
                    clearable=False,
                    style={'width': '100%', 'height': '20px'},
                    options=[
                        {'label': name.capitalize(), 'value': name}
                        for name in ['breadthfirst','grid', 'random', 'circle', 'cose', 'concentric']
                    ]
                ),
                cyto.Cytoscape(
                    id='cytoscapeActors',
                    autoungrabify=False,
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
                        # Class selectors
                        {
                            'selector': '.NodeColor',
                            'style': {
                                'background-color': '#9433FF',
                                'line-color': '#33D5FF'
                            }
                        },
                        {
                            'selector': '.EdgeColor',
                            'style': {
                                'background-color': '#9433FF',
                                'line-color': '#9433FF',
                            }
                        },
                        {
                            'selector': '.SI',
                            'style': {
                                'target-arrow-color': 'red',
                                'target-arrow-shape': 'triangle',
                                'line-color': 'red'
                            }
                        },
                        {
                            'selector': '.tri',
                            'style': {
                                'target-arrow-color': '#9433FF',
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
                        },
                        {
                            'selector': '.BTC',
                            'style': {
                                'background-color': 'red',
                            }
                        },
                        {
                            'selector': '.IIP',
                            'style': {
                                'background-color': 'blue',
                            }
                        },
                    ]
                    )]
                )],width =4),
                dbc.Col([
                cyto.Cytoscape(
                    id='cytoscapeLegend',
                    autoungrabify=True,
                    minZoom=0.45,
                    maxZoom=0.8,
                    # layout={'name': 'grid', 'rows':3,'cols':1},
                    layout={'name': 'preset'},
                    style={'width': '100%', 'height': '200px'},
                    elements= [
                    {'data': {'id': 'Red', 'label': 'System Integrator(Not all actors depend on system Integrator)'}, 'position': {'x': 10, 'y': 250},'size':40, 'classes': 'BTC'},
                    {'data': {'id': 'Blue', 'label': 'Platform Operator(All actors depends on platform operator)'}, 'position': {'x':10, 'y': 300},'size':40, 'classes': 'IIP'},
                    {'data': {'id': 'purple', 'label': 'Other Actors(Links are based on value chain)'}, 'position': {'x': 10, 'y': 350},'size':40, 'classes': 'NodeColor'}
                ],
                stylesheet=[
                        # Group selectors for NODES
                        {
                            'selector': 'node',
                            'style': {
                                'label': 'data(label)',
                                'text-halign':'right',
                                'text-valign':'center',
                                'shape': 'square',
                                'width': "30%",
                                'height': "30%"
                            }
                        },
                        # Class selectors
                        {
                            'selector': '.NodeColor',
                            'style': {
                                'background-color': '#9433FF',
                                'line-color': '#33D5FF',
                            }
                        },
                        {
                            'selector': '.BTC',
                            'style': {
                                'background-color': 'red',
                            }
                        },
                        {
                            'selector': '.IIP',
                            'style': {
                                'background-color': 'blue',
                            }
                        }
                    ]
                )], width=2)
    ]),

    #     Div to display the elements. This will be empty till a brach is cliked in treemap
    dbc.Row([
        dbc.Col([html.Div(id='Elementscontainer')], width=12),
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

# callback for cytograph actor click (can be used in future)
# @app.callback(
#     Output("treemap", "figure"),
#     Output("ElementscontainerFromNode", "children"),
#     Input('cytoscapeActors', 'tapNodeData')
# )
# def update_nodes(data):
#     # print(data)
#     if data is None:
#         return dash.no_update
#     else:
#         label_slct = data['label']
#         dff = df[(df["Actors"] == label_slct)]
#         figure = px.treemap(dff, path=[px.Constant('Ecosystem'),'Roles', 'Actors'],
#                             labels={'Dependency'},
#                             color='Dependency',
#                             values='Dependency',
#                             height=600, width=700).update_layout(margin=dict(t=25, r=0, l=5, b=20))
#         # print(label_slct)
#         # print(dff)
#         # print(df)
#         # # label_slct = data['points'][0]['label']
#         # label_slct = data['label']
#         # # parent_slct = data['points'][0]['parent']
#         # # Filtering data for selected actor
#         # # dff = df[(df.Roles == parent_slct) & (df["Actors"] == label_slct)]
#         # dff = df["Actors"] == label_slct
#         #create the table
#         table_header = [html.Thead(html.Tr([html.Th(label_slct)]))]
#         rows = []
#         for x in dff["StructuralEements"]:
#             if pd.isnull(x):
#                 continue
#             rows.append(html.Tr([html.Td(x)]))
#         table_body = [html.Tbody(rows)]
#         return figure, dbc.Table(table_header + table_body, bordered=True)
        # return figure



# Define callback to display the structural elememts
@app.callback(
    Output("treemap", "figure"),
    Output("Elementscontainer", "children"),
    Input("treemap", "clickData"),
    Input('cytoscapeActors', 'tapNodeData'),
    # State("treemap", "figure"),
    # State("Elementscontainer", "children")
)
def update_modal(treemapclick,nodeclick):
    # print(treemapclick)
    # print(nodeclick)
    # count =0
    cxt = dash.callback_context
    if not cxt.triggered:
        # ClickID = None
        return dash.no_update, dash.no_update
    else:
        ClickID = cxt.triggered[0]['prop_id'].split('.')[0]
    # print(ClickID)
    data = cxt.triggered[0]['value']
    # print(data)
    # print(data)
    if ClickID == 'treemap':
        # if black frame of treemap, don't update
        if data is None:
            return dash.no_update,dash.no_update
            #if no currentpath or ecosystem is chosen, don't update *+
        elif data['points'][0].get('currentPath') is None \
                or data['points'][0]['percentRoot'] == 1 \
                and data['points'][0]['label'] == 'Ecosystem':
            # print("Ecosystem Entered")
            # count = 1
            # print(data)
            # print(count)
            table_header = " "
            table_body = " "
            # data['points'][0]['pointNumber'] = 19
            # data['points'][0]['value'] = 80
            # data['points'][0]['color'] = 1.9
            # data['points'][0]['customdata'] = [1.9]
            # if count == 2:
            # print(df)
            figure = px.treemap(df, path=[px.Constant('Ecosystem'), 'Roles', 'Actors'],
                                labels={'Dependency'},
                                color='Dependency',
                                values='Dependency',
                                height=600, width=700).update_layout(margin=dict(t=25, r=0, l=5, b=20)).update_traces(
                    hovertemplate='%{currentPath}')
            # count =0
            return figure, dbc.Table(table_header + table_body, bordered=False)
            # figure = " "
            # dash.no_update

        # if Role is chosen (ecosystem is parent), don't update
        elif data['points'][0]['label'] in df.Roles.unique():
            label_slct = data['points'][0]['label']
            parent_slct = data['points'][0]['parent']
            # Filtering data for the seleced role
            dff = df[(df.Roles == label_slct)]
            # create the table
            table_header = [html.Thead(html.Tr([html.Th(label_slct)]))]
            table_body = [html.Tbody(dff["RoleInfo"].unique())]
            return dash.no_update,dbc.Table(table_header + table_body, bordered=True)
            # return dbc.Table(table_header + table_body, bordered=True)

        # if Actor is chosen, build table
        else:
            label_slct = data['points'][0]['label']
            parent_slct = data['points'][0]['parent']
            # Filtering data for selected actor
            dff = df[(df.Roles == parent_slct) & (df["Actors"] == label_slct)]
            # print(dff)
            # create the table
            table_header = [html.Thead(html.Tr([html.Th(label_slct)]))]
            rows = []
            for x in dff["StructuralEements"]:
                if pd.isnull(x):
                    continue
                rows.append(html.B((x.split("|"))[0]))
                rows.append(html.Tr([html.Td((x.split("|"))[1])]))
                table_body = [html.Tbody(rows)]
            return dash.no_update,dbc.Table(table_header + table_body, bordered=True)
            # return dbc.Table(table_header + table_body, bordered=True)
    elif ClickID == 'cytoscapeActors':
        label_slct = data['label']
        dff = df[(df["Actors"] == label_slct)]
        # print(dff)
        figure = px.treemap(dff, path=[px.Constant('Ecosystem'),'Roles', 'Actors'],
                            labels={'Dependency'},
                            color='Dependency',
                            values='Dependency',
                            height=600, width=700).update_layout(margin=dict(t=25, r=0, l=5, b=20)).update_traces(hovertemplate='%{currentPath}')
        # print(dff)
        # create the table
        table_header = [html.Thead(html.Tr([html.Th(label_slct)]))]
        rows = []
        for x in dff["StructuralEements"]:
            if pd.isnull(x):
                continue
            rows.append(html.B((x.split("|"))[0]))
            rows.append(html.Tr([html.Td((x.split("|"))[1])]))
            table_body = [html.Tbody(rows)]
        return figure, dbc.Table(table_header + table_body, bordered=True)
        # return dbc.Table(table_header + table_body, bordered=True)

if __name__ == '__main__':
    app.run_server(debug=True)
