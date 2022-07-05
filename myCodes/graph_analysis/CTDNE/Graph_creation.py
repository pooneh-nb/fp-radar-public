import numpy as np
from networkx.readwrite import json_graph
from myCodes.AST import utilities
import networkx as nx
import pandas as pd
import os
from shutil import copyfile


def create_graph(graph_1, graph_2, node_list, out_dir, year):

    # train
    if year == 2012:
        G_train = nx.MultiGraph()
        for node in node_list:
            if node == "null":
                node = "nll"
            if node == "NaN":
                node = "NN"
            if node == "NULL":
                node = "NLL"
            G_train.add_node(node)

        edges_train = []
        for e1, e2 in graph_1.edges():
            year_attrr = int(graph_1[e1][e2]['year'])
            if e1 == "null":
                e1 = "nll"
            if e1 == "NaN":
                e1 = "NN"
            if e1 == "NULL":
                e1 = "NLL"

            if e2 == "null":
                e2 = "nll"
            if e2 == "NaN":
                e2 = "NN"
            if e2 == "NULL":
                e2 = "NLL"
            G_train.add_edge(e1, e2, weight=year_attrr)
            edges_train.append({'source': e1, 'target': e2, 'time': year_attrr})


        edges_train_df = pd.DataFrame(edges_train)
        edges_train_df.to_csv(os.path.join(out_dir, str(year) + '/train/edges.csv'), index=False)

        data = json_graph.node_link_data(G_train)
        utilities.write_json(os.path.join(os.path.join(out_dir, str(year) +'/train/Graph.json')), data)
        print("2010 edges - >", len(G_train.edges()))

    else:
        G_train = graph_1
        edges_train_df = pd.read_csv("/home/c6/Desktop/OpenWPM/jsons/CTDNE/"+str(year)+"/train/edges.csv")

    # test
    G_test = G_train
    edges_test = []
    for e1, e2 in graph_2.edges():
        year_attrr = int(graph_2[e1][e2]['year'])
        if e1 == "null":
            e1 = "nll"
        if e1 == "NaN":
            e1 = "NN"
        if e1 == "NULL":
            e1 = "NLL"

        if e2 == "null":
            e2 = "nll"
        if e2 == "NaN":
            e2 = "NN"
        if e2 == "NULL":
            e2 = "NLL"
        G_test.add_edge(e1, e2, weight=year_attrr)
        edges_test.append({'source': e1, 'target': e2, 'time': year_attrr})

    edges_test_df = pd.DataFrame(edges_test)
    edges_frames = [edges_test_df, edges_train_df]
    result = pd.concat(edges_frames)
    result.to_csv(os.path.join(out_dir, str(year) + '/test/edges.csv'), index=False)
    copyfile(os.path.join(out_dir, str(year) + '/test/edges.csv'), os.path.join(out_dir, str(year+1) + '/train/edges.csv'))
    #result.to_csv(os.path.join(out_dir, str(year+1) + '/train/edges.csv'), index=False)

    data = json_graph.node_link_data(G_test)
    utilities.write_json(os.path.join(out_dir, str(year) + '/test/Graph.json'), data)
    copyfile(os.path.join(out_dir, str(year) + '/test/Graph.json'), os.path.join(out_dir, str(year+1) + '/train/Graph.json'))
    #utilities.write_json(os.path.join(out_dir, str(year+1) + '/train/Graph.json'), data)
    print(year, " test edges - >", len(G_test.edges()))
    print(year, " edges - >", len(result))


def create_pos_neg_links(G_positive, year, out_dir):
    edges_train_label = []
    for e1, e2 in G_positive.edges():
        year_attrr = int(G_positive[e1][e2]['year'])
        if e1 == "null":
            e1 = "nll"
        if e1 == "NaN":
            e1 = "NN"
        if e1 == "NULL":
            e1 = "NLL"

        if e2 == "null":
            e2 = "nll"
        if e2 == "NaN":
            e2 = "NN"
        if e2 == "NULL":
            e2 = "NLL"
        edges_train_label.append({'source': e1, 'target': e2, 'time': year_attrr})
            
    edges_train_df = pd.DataFrame(edges_train_label)
    edges_train_df.to_csv(os.path.join(out_dir, str(year) + '/train/edges_train_label.csv'), index=False)
    if year != 2012:
        edges_train_df.to_csv(os.path.join(out_dir, str(year-1) + '/test/edges_train_label.csv'), index=False)

def main():
   years = np.arange(2012, 2021, 1)

   """for year in years:
       if year == 2012:
           graph_1 = json_graph.node_link_graph(
               utilities.read_json("/home/c6/Desktop/OpenWPM/jsons/AST/CDX_results/Graphs/" + str(
                   2010) + "/Graph.json"))  # Graph in 2010
           graph_2 = json_graph.node_link_graph(
               utilities.read_json("/home/c6/Desktop/OpenWPM/jsons/AST/CDX_results/Graphs/" + str(
                   2011) + "/Graph.json"))
           print("year 2011 edges ", len(graph_2.edges()))

       else:
           graph_1 = json_graph.node_link_graph(
               utilities.read_json("/home/c6/Desktop/OpenWPM/jsons/CTDNE/"+str(year)+"/train/Graph.json"))
           graph_2 = json_graph.node_link_graph(
               utilities.read_json("/home/c6/Desktop/OpenWPM/jsons/AST/CDX_results/Graphs/" + str(
                   year-1) + "/Graph.json"))
           print("year", str(year-1) , len(graph_2.edges()))
       out_dir = "/home/c6/Desktop/OpenWPM/jsons/CTDNE/"
       node_list = utilities.read_json("/home/c6/Desktop/OpenWPM/jsons/CTDNE/" + str(year) + "/node_list.json")
       create_graph(graph_1, graph_2, node_list, out_dir, year)"""

   out_dir = "/home/c6/Desktop/OpenWPM/jsons/CTDNE"
   for year in years:
       G_positive = json_graph.node_link_graph(
            utilities.read_json("/home/c6/Desktop/OpenWPM/jsons/AST/CDX_results/Graphs/" + str(
                year-1) + "/Graph.json"))
       create_pos_neg_links(G_positive, year, out_dir)
        

if __name__ == '__main__':
    main()

