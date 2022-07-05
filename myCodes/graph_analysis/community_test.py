import community as community_louvian
import networkx as nx
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import json
with open("/jsons/AST/umar_ds/nodes_tuple.json", "rt") as nod:
    nodes_list = json.load(nod)
nodes = [tuple(l) for l in nodes_list]
with open("/jsons/AST/umar_ds/edges_tuple.json", "rt") as ed:
    edges_list = json.load(ed)
edges = [tuple(ee) for ee in edges_list]

print(len(nodes))
print(len(edges))

G = nx.Graph()
G.add_nodes_from(nodes)
G.add_edges_from(edges)

#first compute the best partition
partition = community_louvian.best_partition(G)

# draw the graph
pos = nx.spring_layout(G)
# color the nodes according to their partition>>>
cmap = cm.get_cmap('viridis', max(partition.values()) + 1)
nx.draw_networkx_nodes(G, pos, partition.keys(), node_size=40, cmap=cmap, node_color=list(partition.values()))
nx.draw_networkx_edges(G, pos, alpha=0.5)
plt.show()
#print(G)
#print(set(partition.values()))
# compute the best partition
