from math import log

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import json
from dash.dependencies import Input, Output
import dill


with open("/home/c6/Desktop/OpenWPM/jsons/AST/umar_ds/pruned/pruned_api_hash_frac_louvian_0.94.json", 'rt') as node:
    nodes = json.load(node)

nodes_df = pd.DataFrame(columns=['api_keyw', 'node_weight', 'num_scripts', 'cluster', 'fp_status', 'x_pos', 'y_pos'])
for api_key, values in nodes.items():
    if values['louvain_partitioning'] < 7:
        api_keyw = api_key
        node_weight = values['node_weight']
        num_scripts = log(values['scripts'])
        #num_scripts = values['scripts']
        x_pos = values['x_pos']
        y_pos = values['y_pos']
        cluster = values['louvain_partitioning']
        if values['node_weight'] == 10000:
            #node_weight = 34
            fp_status = "FP"
        if values['fp_frac'] == 0 and values['non_fp_frac'] != 0:
            fp_status = "non_FP"
            #node_weight = 1
        if values['non_fp_frac'] != 0 and values['fp_frac'] != 0:
            fp_status = "both"
        if values['non_fp_frac'] == 0 and values['fp_frac'] == 0:
            fp_status = "neutral"
        nodes_df = nodes_df.append({'api_keyw': api_keyw, 'node_weight': node_weight, 'num_scripts': num_scripts,
                                    'cluster': cluster, 'fp_status': fp_status, 'x_pos': x_pos, 'y_pos': y_pos},
                                   ignore_index=True)


### these 2 lines related to CSS Stylesheet
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Graph(
        id='clustered'
    ),
    dcc.Slider(id='slider', min=nodes_df['cluster'].min(), max=nodes_df['cluster'].max(),
               marks={str(cluster): str(cluster) for cluster in nodes_df['cluster'].unique()},
               value=nodes_df['cluster'].min(), step=None)
])


@app.callback(
    Output('clustered', 'figure'),
    [Input('slider', 'value')]
)


def update_figure(selected_cluster):
    nodes_df_filter = nodes_df[nodes_df.cluster == selected_cluster]
    print(nodes_df_filter['node_weight'])
    fig = px.scatter(nodes_df_filter, x="x_pos", y="y_pos", size="num_scripts", color="fp_status",
                     hover_name="api_keyw")
    fig.update_layout(transition_duration=500)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)