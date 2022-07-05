from networkx.readwrite import json_graph
import networkx as nx
import json
import matplotlib.pyplot as plt
import community as community_louvain
import math
import numpy as np
from myCodes.AST import utilities
import multiprocessing
from multiprocessing import Pool as ThreadPool
import os
import pandas as pd


# integrate the list of nodes (API keywords) in this order: t-1,t,t+1
def extract_combined_apis(past_api_keys, current_api_keys, predicting_api_keys, combined_keys):
    keyword_set = set(past_api_keys + current_api_keys + predicting_api_keys)
    print(len(keyword_set))
    utilities.write_json(combined_keys, list(keyword_set))


# calculate some of the WTf each NODE
def node_wtf_degree_calculation(G, out_dir):
    print("Start -->", out_dir.split('/')[-2])
    for node_temp in G.nodes():
        wt = 0
        for nbr, eattr in G.adj[node_temp].items():
            wt = wt + eattr['weight'] * math.log2(int(eattr['year']) - 2010 + 3)
        G.nodes[node_temp]['node_wtf'] = wt
        G.nodes[node_temp]['deg'] = len(G.adj[node_temp])

    data = json_graph.node_link_data(G)
    utilities.write_json(out_dir, data)
    print("End -->", out_dir.split('/')[-2])


# calculate WTf of each EDGE
def edge_wtf_calculation(G, out_dir):
    for n1,n2 in G.edges():
        year = G.edges[n1,n2]['year']
        wtf = G.edges[n1,n2]['weight'] * tf(n1,n2, year)
        G.edges[n1,n2]['wtf'] = wtf

    data = json_graph.node_link_data(G)
    utilities.write_json(out_dir, data)
    print("End-->", year)


def tf(a,b,year):
    tf = math.log2((int(year)-2010)+3)
    return tf


def feature_extraction(G_addr):
    g = utilities.read_json(G_addr)
    G = json_graph.node_link_graph(g)
    year = G_addr.split('/')[-2]
    print("Start-->", year)

    for n1, n2 in G.edges():
        CN = 0 # common neighbors
        AA = 0 # Adamic_Adar
        HP = 0 # Hup promoted Index
        HD = 0 # Hup depressed index
        JC = 0 # jaccards coefficient
        LHN = 0 # Leich-Holm
        RA = 0 # Resource Allocation Index
        SA = 0 # Salton Index
        SO = 0 # Sorenson Index

        nghbr = list(nx.common_neighbors(G, n1, n2))
        if len(list(nghbr)) == 0:
            pass
        else:
            wtf_n1 = G.nodes[n1]['node_wtf']
            wtf_n2 = G.nodes[n2]['node_wtf']
            for z in nghbr:
                wtf_z = G.nodes[z]['node_wtf']
                numerator = G.edges[n1,z]['wtf'] + G.edges[n2,z]['wtf']
                AA += numerator / math.log2(1 + wtf_z)
                CN += numerator
                HP += numerator / min(wtf_n1, wtf_n2)
                HD += numerator / max(wtf_n1, wtf_n2)
                JC += numerator / (wtf_n1 + wtf_n2)
                LHN += numerator / (wtf_n1 * wtf_n2)
                RA += numerator / wtf_z
                SA += numerator / math.sqrt(wtf_n1 + wtf_n2)
                SO += (2 * numerator) / (wtf_n1 + wtf_n2)

        G.edges[n1,n2]['AA'] = AA
        G.edges[n1, n2]['CN'] = CN
        G.edges[n1, n2]['HP'] = HP
        G.edges[n1, n2]['HD'] = HD
        G.edges[n1, n2]['JC'] = JC
        G.edges[n1, n2]['LHN'] = LHN
        G.edges[n1, n2]['RA'] = RA
        G.edges[n1, n2]['SA'] = SA
        G.edges[n1, n2]['SO'] = SO

    data = json_graph.node_link_data(G)
    utilities.write_json(os.path.join(G_addr), data)
    print("End-->", year)


# finding negative links
def non_connected_link_feature_extraction(root):
    disconnection_addr = os.path.join(root, 'disconnect.json')
    G_addr = os.path.join(root, 'Graph.json')
    g = utilities.read_json(G_addr)
    G = json_graph.node_link_graph(g)
    keyword_list = utilities.read_json(os.path.join(root, 'node_list.json'))
    #print(len(keyword_list))
    year = G_addr.split('/')[-2]

    print("Start-->", year)
    disconnection = []
    for idx, key in enumerate(keyword_list):
        for i in range(idx + 1, len(keyword_list)):
            #disconnect_edge = {}
            if keyword_list[idx] not in G.nodes():
                #idx += 1
                disconnection.append({"weight": 0.0, "ratio": 0.0, "correct_ratio": 0.0,
                                      "year": "0", "wtf": 0.0, "AA": 0.0, "CN": 0.0, "HP": 0.0,
                                      "HD": 0.0, "JC": 0.0, "LHN": 0.0, "RA": 0.0, "SA": 0.0, "SO": 0.0,
                                      "source": keyword_list[idx], "target": keyword_list[i]})
                break
            if keyword_list[i] not in G.nodes():
                disconnection.append({"weight": 0.0, "ratio": 0.0, "correct_ratio": 0.0,
                                      "year": "0", "wtf": 0.0, "AA": 0.0, "CN": 0.0, "HP": 0.0,
                                      "HD": 0.0, "JC": 0.0, "LHN": 0.0, "RA": 0.0, "SA": 0.0, "SO": 0.0,
                                      "source": keyword_list[idx], "target": keyword_list[i]})
                continue
            if keyword_list[idx] in G.nodes() and keyword_list[i] in G.nodes():
                if not G.has_edge(keyword_list[idx], keyword_list[i]):
                    #print(year, "new")
                    n1 = keyword_list[idx]
                    n2 = keyword_list[i]
                    CN = 0
                    AA = 0
                    HP = 0
                    HD = 0
                    JC = 0
                    LHN = 0
                    RA = 0
                    SA = 0
                    SO = 0

                    nghbr = list(nx.common_neighbors(G, n1, n2))
                    if len(list(nghbr)) == 0:
                        pass
                    else:
                        wtf_n1 = G.nodes[n1]['node_wtf']
                        a = G.nodes[n1]['deg']
                        wtf_n2 = G.nodes[n2]['node_wtf']
                        for z in nghbr:
                            wtf_z = G.nodes[z]['node_wtf']
                            nominator = G.edges[n1, z]['wtf'] + G.edges[n2, z]['wtf']
                            AA += nominator / math.log2(1 + wtf_z)
                            CN += nominator
                            HP += nominator / min(wtf_n1, wtf_n2)
                            HD += nominator / max(wtf_n1, wtf_n2)
                            JC += nominator / (wtf_n1 + wtf_n2)
                            LHN += nominator / (wtf_n1 * wtf_n2)
                            RA += nominator / wtf_z
                            SA += nominator / math.sqrt(wtf_n1 + wtf_n2)
                            SO += (2 * nominator) / (wtf_n1 + wtf_n2)
                    disconnection.append({"weight": 0.0, "ratio": 0.0, "correct_ratio": 0.0,
                                          "year": "0", "wtf": 0.0, "AA": AA, "CN": CN,
                                          "HP": HP, "HD": HD, "JC": JC, "LHN": LHN, "RA": RA,
                                          "SA": SA, "SO": SO, "source": keyword_list[idx], "target": keyword_list[i]})
                    #print(len(disconnection))

    utilities.write_json(disconnection_addr, disconnection)
    print("End-->", year)


# create dataframe for training and testing data
def DataFrame_creation(root):
    disconnection_addr = os.path.join(root, 'disconnect.json')
    disconnection = utilities.read_json(disconnection_addr)
    G_addr = os.path.join(root, 'Graph.json')
    g = utilities.read_json(G_addr)
    G = json_graph.node_link_graph(g)

    year = G_addr.split('/')[-2]

    ground_label_addr = "/home/c6/Desktop/OpenWPM/jsons/AST/CDX_results/Graphs/" + str(int(year) + 1) + "/Graph.json"
    ground_label_g = utilities.read_json(ground_label_addr)
    ground_label_graph = json_graph.node_link_graph(ground_label_g)
    print("Start-->", year)

    dataset_features = ['e1', 'e2', 'Wtf', 'W', 'CN', 'AA', 'HP', 'HD', 'JC', 'LHN', 'RA', 'SA', 'SO', 'ratio',
                        'deg_e1', 'deg_e2', 'e1_ratio', 'et_ratio']
    records = []
    for e1, e2 in G.edges():
        if ground_label_graph.has_edge(e1, e2):
            records.append({'e1': e1, 'e2': e2, 'edge_wtf': G.edges[e1, e2]['wtf'],
                            'W': G.edges[e1, e2]['weight'], 'CN': G.edges[e1, e2]['CN'],
                            'AA': G.edges[e1, e2]['AA'], 'HP': G.edges[e1, e2]['HP'],
                            'HD': G.edges[e1, e2]['HD'], 'JC': G.edges[e1, e2]['JC'],
                            'LHN': G.edges[e1, e2]['LHN'], 'RA': G.edges[e1, e2]['RA'],
                            'SA': G.edges[e1, e2]['RA'], 'SO': G.edges[e1, e2]['SO'],
                            'deg_e1': G.nodes[e1]['deg'], 'deg_e2': G.nodes[e2]['deg'],
                            'label': 1})
        else:
            records.append({'e1': e1, 'e2': e2, 'edge_wtf': G.edges[e1, e2]['wtf'],
                            'W': G.edges[e1, e2]['weight'], 'CN': G.edges[e1, e2]['CN'],
                            'AA': G.edges[e1, e2]['AA'], 'HP': G.edges[e1, e2]['HP'],
                            'HD': G.edges[e1, e2]['HD'], 'JC': G.edges[e1, e2]['JC'],
                            'LHN': G.edges[e1, e2]['LHN'], 'RA': G.edges[e1, e2]['RA'],
                            'SA': G.edges[e1, e2]['RA'], 'SO': G.edges[e1, e2]['SO'],
                            'deg_e1': G.nodes[e1]['deg'], 'deg_e2': G.nodes[e2]['deg'],
                            'label': 0})

    for non_link in disconnection:
        if ground_label_graph.has_edge(non_link['source'], non_link['target']):
            records.append({'e1': non_link['source'], 'e2': non_link['target'], 'edge_wtf': non_link['wtf'],
                            'W': non_link['weight'], 'CN': non_link['CN'], 'AA': non_link['AA'], 'HP': non_link['HP'],
                            'HD': non_link['HD'], 'JC': non_link['JC'], 'LHN': non_link['LHN'], 'RA': non_link['RA'],
                            'SA': non_link['RA'], 'SO': non_link['SO'], 'deg_e1': 0, 'deg_e2': 0,
                            'label': 1})
        else:
            records.append({'e1': non_link['source'], 'e2': non_link['target'], 'edge_wtf': non_link['wtf'],
                            'W': non_link['weight'], 'CN': non_link['CN'], 'AA': non_link['AA'], 'HP': non_link['HP'],
                            'HD': non_link['HD'], 'JC': non_link['JC'], 'LHN': non_link['LHN'], 'RA': non_link['RA'],
                            'SA': non_link['RA'], 'SO': non_link['SO'], 'deg_e1': 0, 'deg_e2': 0,
                            'label': 0})

    df = pd.DataFrame(records)
    df.to_csv(os.path.join(root, 'dataframe.csv'), index=False)
    print("End-->", year)


def main():
    years = np.arange(2018, 2019, 1)
    # 1. extract unique apis
    """
    for year in years:
        combined_keys = "/home/c6/Desktop/OpenWPM/jsons/Prediction_new/Most_recent_graphs_Prediction/"+str(year)+"/node_list.json"
        past_api_keys = list(json_graph.node_link_graph\
            (utilities.read_json("/home/c6/Desktop/OpenWPM/jsons/AST/CDX_results/Graphs/"+str(year-2)+"/Graph.json"))\
            .nodes())
        current_api_keys = list(json_graph.node_link_graph\
            (utilities.read_json("/home/c6/Desktop/OpenWPM/jsons/AST/CDX_results/Graphs/"+str(year-1)+"/Graph.json"))\
            .nodes())
        predicting_api_keys = list(json_graph.node_link_graph\
            (utilities.read_json("/home/c6/Desktop/OpenWPM/jsons/AST/CDX_results/Graphs/"+str(year)+"/Graph.json"))\
            .nodes())
        extract_combined_apis(past_api_keys, current_api_keys, predicting_api_keys, combined_keys)"""

    # 2. calculate wtf of edges
    """
    for year in years:
        graph = json_graph.node_link_graph(
            utilities.read_json("/home/c6/Desktop/OpenWPM/jsons/AST/CDX_results/Graphs/" + str(
                year) + "/Graph.json"))
        graph_address = "/home/c6/Desktop/OpenWPM/jsons/Prediction_new/Most_recent_graphs_Prediction/" + str(year) + "/Graph.json"
        edge_wtf_calculation(graph, graph_address)"""

    # 3. calculate sum of nodes' weight and degree
    """
    for year in years:
        graph = json_graph.node_link_graph(
            utilities.read_json("/home/c6/Desktop/OpenWPM/jsons/Prediction_new/Most_recent_graphs_Prediction/" + str(
                year) + "/Graph.json"))
        graph_address = "/home/c6/Desktop/OpenWPM/jsons/Prediction_new/Most_recent_graphs_Prediction/" + str(year) + "/Graph.json"
        node_wtf_degree_calculation(graph, graph_address)"""

    # 4. Feature Extraction
    """graph_list = []
    for year in years:
        graph_list.append("/home/c6/Desktop/OpenWPM/jsons/Prediction_new/Most_recent_graphs_Prediction/" + str(year) + "/Graph.json")
    # multiprocessing
    #cpu_to_relax = 3
    pool = ThreadPool(processes=10)
    # pool = ThreadPool(processes=1)
    results = pool.map(feature_extraction, graph_list)
    pool.close()
    pool.join()

    #for g in graph_list:
        #feature_extraction(g)"""

    # 5. non_connected_link_feature_extraction
    """root_dir = []
    for year in years:
        root_dir.append("/home/c6/Desktop/OpenWPM/jsons/Prediction_new/Most_recent_graphs_Prediction/" + str(year))
    pool = ThreadPool(processes=1)
    result = pool.map(non_connected_link_feature_extraction, root_dir)
    pool.close()
    pool.join()"""

    # 6. Make DataFrame
    root_dir = []
    for year in years:
        root_dir.append("/home/c6/Desktop/OpenWPM/jsons/Prediction_new/Most_recent_graphs_Prediction/" + str(year))

    pool = ThreadPool(processes=3)
    result = pool.map(DataFrame_creation, root_dir)
    pool.close()
    pool.join()


if __name__ == '__main__':
    main()