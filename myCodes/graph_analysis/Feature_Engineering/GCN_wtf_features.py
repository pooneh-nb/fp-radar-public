from networkx.readwrite import json_graph
import networkx as nx
import numpy as np
from myCodes.AST import utilities
import multiprocessing
from multiprocessing import Pool as ThreadPool
import os
import pandas as pd


def expand_edge_features_to_nodes(root):

    # Train dataset
    G_addr = os.path.join(root, 'train/Graph.json')
    g = utilities.read_json(G_addr)
    G = json_graph.node_link_graph(g)
    year = G_addr.split('/')[-3]
    print("Start, Train-->", year)
    for n1, n2 in G.edges():
        G.nodes[n1][n1 + "_" + n2 + "_wtf"] = G.edges[n1, n2]['wtf']
        G.nodes[n2][n1 + "_" + n2 + "_wtf"] = G.edges[n1, n2]['wtf']

        G.nodes[n1][n1 + "_" + n2 + "_W"] = G.edges[n1, n2]['weight']
        G.nodes[n2][n1 + "_" + n2 + "_W"] = G.edges[n1, n2]['weight']

        G.nodes[n1][n1 + "_" + n2 + "_AA"] = G.edges[n1, n2]['AA']
        G.nodes[n2][n1 + "_" + n2 + "_AA"] = G.edges[n1, n2]['AA']

        G.nodes[n1][n1 + "_" + n2 + "_CN"] = G.edges[n1, n2]['CN']
        G.nodes[n2][n1 + "_" + n2 + "_CN"] = G.edges[n1, n2]['CN']

        G.nodes[n1][n1 + "_" + n2 + "_HP"] = G.edges[n1, n2]['HP']
        G.nodes[n2][n1 + "_" + n2 + "_HP"] = G.edges[n1, n2]['HP']

        G.nodes[n1][n1 + "_" + n2 + "_HD"] = G.edges[n1, n2]['HD']
        G.nodes[n2][n1 + "_" + n2 + "_HD"] = G.edges[n1, n2]['HD']

        G.nodes[n1][n1 + "_" + n2 + "_JC"] = G.edges[n1, n2]['JC']
        G.nodes[n2][n1 + "_" + n2 + "_JC"] = G.edges[n1, n2]['JC']

        G.nodes[n1][n1 + "_" + n2 + "_LHN"] = G.edges[n1, n2]['LHN']
        G.nodes[n2][n1 + "_" + n2 + "_LHN"] = G.edges[n1, n2]['LHN']

        G.nodes[n1][n1 + "_" + n2 + "_RA"] = G.edges[n1, n2]['RA']
        G.nodes[n2][n1 + "_" + n2 + "_RA"] = G.edges[n1, n2]['RA']

        G.nodes[n1][n1 + "_" + n2 + "_SA"] = G.edges[n1, n2]['SA']
        G.nodes[n2][n1 + "_" + n2 + "_SA"] = G.edges[n1, n2]['SA']

        G.nodes[n1][n1 + "_" + n2 + "_SO"] = G.edges[n1, n2]['SO']
        G.nodes[n2][n1 + "_" + n2 + "_SO"] = G.edges[n1, n2]['SO']

    data = json_graph.node_link_data(G)
    utilities.write_json(os.path.join(G_addr), data)
    print("End, train-->", year)

    # Test dataset
    H_addr = os.path.join(root, 'test/Graph.json')
    h = utilities.read_json(H_addr)
    H = json_graph.node_link_graph(h)
    year = H_addr.split('/')[-3]
    print("Start, Test-->", year)
    for n1, n2 in H.edges():
        H.nodes[n1][n1 + "_" + n2 + "_wtf"] = H.edges[n1, n2]['wtf']
        H.nodes[n2][n1 + "_" + n2 + "_wtf"] = H.edges[n1, n2]['wtf']

        H.nodes[n1][n1 + "_" + n2 + "_W"] = H.edges[n1, n2]['weight']
        H.nodes[n2][n1 + "_" + n2 + "_W"] = H.edges[n1, n2]['weight']

        H.nodes[n1][n1 + "_" + n2 + "_AA"] = H.edges[n1, n2]['AA']
        H.nodes[n2][n1 + "_" + n2 + "_AA"] = H.edges[n1, n2]['AA']

        H.nodes[n1][n1 + "_" + n2 + "_CN"] = H.edges[n1, n2]['CN']
        H.nodes[n2][n1 + "_" + n2 + "_CN"] = H.edges[n1, n2]['CN']

        H.nodes[n1][n1 + "_" + n2 + "_HP"] = H.edges[n1, n2]['HP']
        H.nodes[n2][n1 + "_" + n2 + "_HP"] = H.edges[n1, n2]['HP']

        H.nodes[n1][n1 + "_" + n2 + "_HD"] = H.edges[n1, n2]['HD']
        H.nodes[n2][n1 + "_" + n2 + "_HD"] = H.edges[n1, n2]['HD']

        H.nodes[n1][n1 + "_" + n2 + "_JC"] = H.edges[n1, n2]['JC']
        H.nodes[n2][n1 + "_" + n2 + "_JC"] = H.edges[n1, n2]['JC']

        H.nodes[n1][n1 + "_" + n2 + "_LHN"] = H.edges[n1, n2]['LHN']
        H.nodes[n2][n1 + "_" + n2 + "_LHN"] = H.edges[n1, n2]['LHN']

        H.nodes[n1][n1 + "_" + n2 + "_RA"] = H.edges[n1, n2]['RA']
        H.nodes[n2][n1 + "_" + n2 + "_RA"] = H.edges[n1, n2]['RA']

        H.nodes[n1][n1 + "_" + n2 + "_SA"] = H.edges[n1, n2]['SA']
        H.nodes[n2][n1 + "_" + n2 + "_SA"] = H.edges[n1, n2]['SA']

        H.nodes[n1][n1 + "_" + n2 + "_SO"] = H.edges[n1, n2]['SO']
        H.nodes[n2][n1 + "_" + n2 + "_SO"] = H.edges[n1, n2]['SO']

    data = json_graph.node_link_data(H)
    utilities.write_json(os.path.join(H_addr), data)
    print("End, Test-->", year)


def main():
    years = np.arange(2019, 2020, 1)
    root_dir = []
    for year in years:
        root_dir.append("/home/c6/Desktop/OpenWPM/jsons/Prediction_new/GCN_wtf/" + str(year))

    cpu_to_relax = 3
    pool = ThreadPool(processes=9)
    result = pool.map(expand_edge_features_to_nodes, root_dir)
    pool.close()
    pool.join()


if __name__ == '__main__':
    main()