#the histogram of node weight
# the result is less than 20
import plotly.express as px
import json
import pandas as pd

with open("/home/c6/Desktop/OpenWPM/jsons/AST/umar_ds/nodes_tuple.json", 'rt') as node:
    nodes = dict(json.load(node))

node_weight = []
for nod, val in nodes.items():
    if 0.2 > val['node_weight'] > 0:
        node_weight.append(val['node_weight'])


df = pd.DataFrame(node_weight)
fig = px.histogram(df, log_y=True)
fig.show()