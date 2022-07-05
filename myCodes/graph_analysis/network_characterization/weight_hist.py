import networkx as nx
import json


def weight():
    with open("2020/nodes_tuple.json", "rt") as nod:
        nodes_list = json.load(nod)
    nodes = [tuple(l) for l in nodes_list]
    with open("2020/edges_tuple.json", "rt") as ed:
        edges_list = json.load(ed)
    edges = [tuple(ee) for ee in edges_list]
    G = nx.Graph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)

    for node_temp in G.nodes():
        # add two attributes to each node; l and u. l=0 and u = number of neighbors(degree)
        # attr u should be the average weight of u
        # self.G.nodes[node_temp]['u'] = len(self.G.adj[node_temp])
        wt = 0
        for nbr, eattr in G.adj[node_temp].items():
            wt = wt + sum(eattr['w'])


weight()
