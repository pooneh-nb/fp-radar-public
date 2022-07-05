#the histogram of node weight
# the result is less than 20
import plotly.express as px
import json
import pandas as pd

with open("/home/c6/Desktop/OpenWPM/jsons/AST/umar_ds/api_hash_frac.json", 'rt') as node:
    general = json.load(node)

scripts = []
for nod, val in general.items():
    if val['scripts'] < 1000:
        scripts.append(val['scripts'])

print(len(scripts))
df = pd.DataFrame(scripts)
fig = px.histogram(df, log_y=True)
fig.show()