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

source_data = { "GRCh37": [{"id": "BTC Business Technology Consulting AG","label": "BTC Business Technology Consulting AG",
                            "color": "#996600","len": 369250621},
                           {"id": "Sennheiser","label": "Sennheiser",
                            "color": "#666600","len": 249250621},
                           {"id": "Gerresheimer","label": "Gerresheimer",
                            "color": "#99991E","len": 249250621},
                           {"id": "Volkswagen","label": "Volkswagen",
                            "color": "#CC0000","len": 249250621},
                           {"id": "Lenze AG","label": "Lenze AG",
                            "color": "#FF0000","len": 149250621},
                           {"id": "Siemens AG","label": "Siemens AG",
                            "color": "#FF00CC","len": 249250621},
                           {"id": "infor GmbH Deutschland","label": "infor GmbH Deutschland",
                            "color": "#FFCCCC","len": 249250621},
                           {"id": "ÍNDUMESS (industrielle Messtechnik)","label": "ÍNDUMESS (industrielle Messtechnik)",
                            "color": "#FF9900","len": 349250621},
                           {"id": "slashwhy","label": "slashwhy",
                            "color": "#FFCC00","len": 249250621}],
               "chords": [{"color": "#ff5722","source": {"id": "slashwhy","start": 22186054,"end": 36186054},
                           "target": {"id": "Volkswagen","start": 21478117,"end": 85478117} },
                         {"color": "#ff5722","source": {"id": "Volkswagen","start":  74807187,"end": 78807187},
                           "target": {"id": "Lenze AG","start": 21478117,"end": 85478117} }]
              }
# Load data
df = pd.read_excel(r'C:\Users\archa\Documents\Archana\IIS_GoogleDrive\IIS\Thesis\Julius\Application_Panywhere\EcosystemVisualization\Data\Data.xlsx',
                   header=1,skiprows=1, names=['Roles','Actors','Resources','Activities','value contribution in ecosystem','Value contribution for the actors','Dependency','RoleInfo'])

# Saving 4 elements into single column. This makes it easy to display the data
df = pd.melt(df, id_vars=['Roles','Actors','Dependency','RoleInfo'],
             value_vars=['Resources','Activities','value contribution in ecosystem','Value contribution for the actors'],
             var_name='results',value_name='StructuralEements')
# Build App
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app.layout = dbc.Container([
    #     Creating treemap
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='treemap',
                      figure=px.treemap(df,
                                        path=[px.Constant('Ecosystem'), 'Roles', 'Actors'],
                                        values='Dependency',
                                        height=600, width=700).update_layout(margin=dict(t=25, r=0, l=5, b=20))
                      )], width=6),
        dbc.Col([dashbio.Circos(
            id='Dashcircos',
            layout=source_data['GRCh37'],
            size=600,
            #                               labels = 'Actors supply chain',
            config={
                'innerRadius': 200,  # 600 / 2 - 80,
                'outerRadius': 180,  # 600 / 2 - 40,
                'ticks': {'display': False},
                'labels': {
                    'position': 'bottom',
                    'display': True,
                    'size': 11,
                    'color': '#996600',
                    'radialOffset': 15,
                },
            },
            #                                 selectEvent={"0": "hover", "1": "click", "2": "both"},
            tracks=[{
                'type': 'CHORDS',
                'data': source_data['chords'],
                'ticks': {'display': False, 'labelDenominator': 1000000},
                'config': {
                    'tooltipContent': {
                        'source': 'source',
                        'sourceID': 'id',
                        'target': 'target',
                        'targetID': 'id',
                        #                     'targetEnd': 'end'
                    }
                }
            }],
        )], width=6)
    ]),

    #     Div to display the elements. This will be empty till a brach is cliked in treemap
    dbc.Row([
        dbc.Col([html.Div(id='Elementscontainer')], width=12)
    ])

], fluid=True)


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

        #         figure= px.treemap(df,
        #                                 path=[px.Constant('Ecosystem'),'Roles','Actors'],
        #                                 values='Dependency',
        #                                 height=700, width=1200).update_layout(margin=dict(t=25, r=0, l=5, b=20))
        #         print(figure)
        #         figure= figure.update_traces(height=700, width=1200).update_layout(margin=dict(t=25, r=0, l=5, b=20))
        #         return figure,dbc.Table(table_header + table_body, bordered=False)
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

        # Updating the treemap to reduce the size
        #         figure= px.treemap(dff,
        #                                 path=[px.Constant('Ecosystem'),'Roles','Actors'],
        #                                 values='Dependency',
        #                                 height=500, width=500).update_layout(margin=dict(t=25, r=0, l=5, b=20))

        #         return figure,dbc.Table(table_header + table_body, bordered=True)
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
            rows.append(html.Tr([html.Td(x)]))
        table_body = [html.Tbody(rows)]

        # Updating the treemap to reduce the size
        #         figure= px.treemap(dff,
        #                                 path=[px.Constant('Ecosystem'),'Roles','Actors'],
        #                                 values='Dependency',
        #                                 height=500, width=500).update_layout(margin=dict(t=25, r=0, l=5, b=20))
        #         print(figure)
        #         return figure,dbc.Table(table_header + table_body, bordered=True)
        return dbc.Table(table_header + table_body, bordered=True)


if __name__ == '__main__':
    app.run_server(debug='True')
