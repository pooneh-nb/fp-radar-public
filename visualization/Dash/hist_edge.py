#the histogram of edge weight between pure FP APIs with every other nodes
# the result is less than 20
import plotly.express as px
import json
import pandas as pd

with open("/home/c6/Desktop/OpenWPM/jsons/AST/umar_ds/edges_tuple.json", 'rt') as node:
    edges = json.load(node)

with open("/home/c6/Desktop/OpenWPM/jsons/AST/umar_ds/nodes_tuple.json", 'rt') as node:
    nodes = dict(json.load(node))

pure_fp = []
for nod, val in nodes.items():
    if val['node_weight'] == 10000:
        pure_fp.append(nod)
print(len(pure_fp))

weight = list()
for value in edges:
    if value[0] in pure_fp or value[1] in pure_fp:
        weight.append(value[2]["edge_weight"])

df = pd.DataFrame(weight)
fig = px.histogram(df, log_y=True)
fig.show()