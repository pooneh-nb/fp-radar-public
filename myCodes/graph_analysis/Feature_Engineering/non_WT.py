import itertools

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


def feature_extraction(year, G_addr):
    if year != 2012:
        G_train_address = os.path.join(G_addr, str(year)+"/train/Graph.json")
        G_test_address_previous = os.path.join(G_addr, str(year-1) + "/test/Graph.json")
    else:
        G_train_address = G_addr
    g = utilities.read_json(G_train_address)
    G = json_graph.node_link_graph(g)
    #year = G_addr.split('/')[-3]
    print("Start, FE-->", year)

    for n1, n2 in G.edges():
        CN = 0  # common neighbors
        AA = 0  # Adamic_Adar
        HP = 0  # Hup promoted Index
        HD = 0  # Hup depressed index
        JC = 0  # jaccards coefficient
        LHN = 0  # Leich-Holm
        RA = 0  # Resource Allocation Index
        SA = 0  # Salton Index
        SO = 0  # Sorenson Index

        nghbr = list(nx.common_neighbors(G, n1, n2))

        if len(list(nghbr)) == 0:
            pass
        else:
            numenator = len(nghbr)

            CN = numenator
            HP = numenator / min(G.nodes[n1]['deg'], G.nodes[n2]['deg'])
            HD = numenator / max(G.nodes[n1]['deg'], G.nodes[n2]['deg'])
            community_ngbr = set([n for n in G.neighbors(n1)] + [n for n in G.neighbors(n2)])
            JC = numenator / len(community_ngbr)

            LHN = numenator / (G.nodes[n1]['deg'] * G.nodes[n2]['deg'])
            SA = numenator / math.sqrt(G.nodes[n1]['deg'] + G.nodes[n2]['deg'])
            SO = (2 * numenator) / (G.nodes[n1]['deg'] + G.nodes[n2]['deg'])
            for z in nghbr:
                try:
                    AA += 1 / math.log2(G.nodes[z]['deg'])
                    RA += 1 / G.nodes[z]['deg']
                except:
                    print(z)

        G.edges[n1, n2]['AA'] = AA
        G.edges[n1, n2]['CN'] = CN
        G.edges[n1, n2]['HP'] = HP
        G.edges[n1, n2]['HD'] = HD
        G.edges[n1, n2]['JC'] = JC
        G.edges[n1, n2]['LHN'] = LHN
        G.edges[n1, n2]['RA'] = RA
        G.edges[n1, n2]['SA'] = SA
        G.edges[n1, n2]['SO'] = SO

    data = json_graph.node_link_data(G)
    utilities.write_json(G_train_address, data)
    if year != 2012:
        utilities.write_json(G_test_address_previous, data)
    print("End-->", year)


# finding negative links
def non_connected_link_feature_extraction(year, root):
    if year != 2012:
        disconnect_train_addrr = os.path.join(root, str(year) + "/train/disconnect.json")
        disconnect_test_addrr = os.path.join(root, str(year - 1) + "/test/disconnect.json")
        G_train_address = os.path.join(root, str(year) + "/train/Graph.json")
        G_test_address_previous = os.path.join(root, str(year - 1) + "/test/Graph.json")
    else:
        disconnect_train_addrr = os.path.join(root, str(year) + "/train/disconnect.json")
        G_train_address = os.path.join(root, str(year) + "/train/Graph.json")
    # disconnection_addr = os.path.join(root, 'disconnect.json')

    g = utilities.read_json(G_train_address)
    # g = utilities.read_json(G_addr)
    G = json_graph.node_link_graph(g)
    keyword_list = utilities.read_json(os.path.join(root, str(year) + '/node_list.json'))

    print("Start,non-->", year)
    disconnection = []
    for idx, key in enumerate(keyword_list):
        for i in range(idx + 1, len(keyword_list)):
            # disconnect_edge = {}
            if keyword_list[idx] not in G.nodes():
                # idx += 1
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
                    # print(year, "new")
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
                        numenator = len(nghbr)
                        CN = numenator
                        HP = numenator / min(G.nodes[n1]['deg'], G.nodes[n2]['deg'])
                        HD = numenator / max(G.nodes[n1]['deg'], G.nodes[n2]['deg'])
                        community_ngbr = set([n for n in G.neighbors(n1)] + [n for n in G.neighbors(n2)])
                        JC = numenator / len(community_ngbr)

                        LHN = numenator / (G.nodes[n1]['deg'] * G.nodes[n2]['deg'])
                        SA = numenator / math.sqrt(G.nodes[n1]['deg'] + G.nodes[n2]['deg'])
                        SO = (2 * numenator) / (G.nodes[n1]['deg'] + G.nodes[n2]['deg'])
                        for z in nghbr:
                            # numenator = G.edges[n1,z]['wtf'] + G.edges[n2,z]['wtf']
                            AA += 1 / math.log2(G.nodes[z]['deg'])
                            RA += 1 / G.nodes[z]['deg']
                    disconnection.append({"weight": 0.0, "ratio": 0.0, "correct_ratio": 0.0,
                                          "year": "0", "wtf": 0.0, "AA": AA, "CN": CN,
                                          "HP": HP, "HD": HD, "JC": JC, "LHN": LHN, "RA": RA,
                                          "SA": SA, "SO": SO, "source": keyword_list[idx], "target": keyword_list[i]})
                    # print(len(disconnection))

    utilities.write_json(disconnect_train_addrr, disconnection)
    if year != 2012:
        utilities.write_json(disconnect_test_addrr, disconnection)

    print("End-->", year)


# create dataframe for training and testing data
def DataFrame_creation(year, root):
    if year != 2012:
        disconnect_train_addrr = os.path.join(root, str(year) + "/train/disconnect.json")
        disconnect_test_addrr = os.path.join(root, str(year - 1) + "/test/disconnect.json")
        disconnection = utilities.read_json(disconnect_train_addrr)
        G_train_address = os.path.join(root, str(year) + "/train/Graph.json")
        G_test_address_previous = os.path.join(root, str(year - 1) + "/test/Graph.json")
    else:
        disconnect_train_addrr = os.path.join(root, str(year) + "/train/disconnect.json")
        disconnection = utilities.read_json(disconnect_train_addrr)
        G_train_address = os.path.join(root, str(year) + "/train/Graph.json")

    g = utilities.read_json(G_train_address)
    G = json_graph.node_link_graph(g)
    print("Start, df-->", year)

    ground_label_addr = "/home/c6/Desktop/OpenWPM/jsons/AST/CDX_results/Graphs/" + str(int(year) - 1) + "/Graph.json"
    ground_label_g = utilities.read_json(ground_label_addr)
    ground_label_graph = json_graph.node_link_graph(ground_label_g)

    dataset_features = ['e1', 'e2', 'Wtf', 'W', 'CN', 'AA', 'HP', 'HD', 'JC', 'LHN', 'RA', 'SA', 'SO', 'ratio',
                        'deg_e1', 'deg_e2', 'e1_ratio', 'et_ratio']
    records = []
    """for e1, e2 in G.edges():
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
                            'label': 0})"""

    for e1, e2 in ground_label_graph.edges():
        if G.has_edge(e1, e2):
            records.append({'e1': e1, 'e2': e2, 'edge_wtf': G.edges[e1, e2]['wtf'],
                            'W': G.edges[e1, e2]['weight'], 'CN': G.edges[e1, e2]['CN'],
                            'AA': G.edges[e1, e2]['AA'], 'HP': G.edges[e1, e2]['HP'],
                            'HD': G.edges[e1, e2]['HD'], 'JC': G.edges[e1, e2]['JC'],
                            'LHN': G.edges[e1, e2]['LHN'], 'RA': G.edges[e1, e2]['RA'],
                            'SA': G.edges[e1, e2]['RA'], 'SO': G.edges[e1, e2]['SO'],
                            'deg_e1': G.nodes[e1]['deg'], 'deg_e2': G.nodes[e2]['deg'],
                            'label': 1})
        else:
            records.append({'e1': e1, 'e2': e2, 'edge_wtf': 0,
                            'W': 0, 'CN': 0,
                            'AA': 0, 'HP': 0,
                            'HD': 0, 'JC': 0,
                            'LHN': 0, 'RA': 0,
                            'SA': 0, 'SO': 0,
                            'deg_e1': 0, 'deg_e2': 0,
                            'label': 1})

    for e1, e2 in G.edges():
        if not ground_label_graph.has_edge(e1, e2):
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
    ### disconnect
    """for e1, e2 in ground_label_graph.edges():
        e1e2 = False
        for non_link in disconnection:
            if (non_link['source'] == e1 and non_link['target'] == e2) or (
                    non_link['source'] == e2 and non_link['target'] == e1):
                records.append({'e1': non_link['source'], 'e2': non_link['target'], 'edge_wtf': non_link['wtf'],
                                'W': non_link['weight'], 'CN': non_link['CN'], 'AA': non_link['AA'],
                                'HP': non_link['HP'],
                                'HD': non_link['HD'], 'JC': non_link['JC'], 'LHN': non_link['LHN'],
                                'RA': non_link['RA'],
                                'SA': non_link['RA'], 'SO': non_link['SO'], 'deg_e1': 0, 'deg_e2': 0,
                                'label': 1})
                e1e2 = True
        if not e1e2:
            records.append({'e1': e1, 'e2': e2, 'edge_wtf': 0,
                            'W': 0, 'CN': 0, 'AA': 0, 'HP': 0,
                            'HD': 0, 'JC': 0, 'LHN': 0, 'RA': 0,
                            'SA': 0, 'SO': 0, 'deg_e1': 0, 'deg_e2': 0,
                            'label': 1})

    for non_link in disconnection:
        if not ground_label_graph.has_edge(non_link['source'], non_link['target']):
            records.append({'e1': non_link['source'], 'e2': non_link['target'], 'edge_wtf': non_link['wtf'],
                            'W': non_link['weight'], 'CN': non_link['CN'], 'AA': non_link['AA'], 'HP': non_link['HP'],
                            'HD': non_link['HD'], 'JC': non_link['JC'], 'LHN': non_link['LHN'], 'RA': non_link['RA'],
                            'SA': non_link['RA'], 'SO': non_link['SO'], 'deg_e1': 0, 'deg_e2': 0,
                            'label': 0})"""


    df = pd.DataFrame(records)
    df.to_csv(os.path.join(root, str(year) + '/train/dataframe.csv'), index=False)
    if year != 2012:
        df.to_csv(os.path.join(root, str(year - 1) + '/test/dataframe.csv'), index=False)
    print("End, df-->", year)


def main():
    years = np.arange(2017, 2021, 1)

    # 1. Feature Extraction
    """graph_2012_train = "/home/c6/Desktop/OpenWPM/jsons/Prediction_new/non_temporal_unweighted/2012/train/Graph.json"
    feature_extraction(2012, graph_2012_train)"""

    """cpu_to_relax = 3
    pool = ThreadPool(processes=multiprocessing.cpu_count() - cpu_to_relax)
    g_addrr = "/home/c6/Desktop/OpenWPM/jsons/Prediction_new/non_temporal_unweighted/"
    results = pool.starmap(feature_extraction, zip(years, itertools.repeat(g_addrr)))
    pool.close()
    pool.join()"""

    # 2. non_connected_link_feature_extraction
    """root_12 = "/home/c6/Desktop/OpenWPM/jsons/Prediction_new/non_temporal_unweighted/"
    non_connected_link_feature_extraction(2012, root_12)"""

    #cpu_to_relax = 3
    #pool = ThreadPool(processes=multiprocessing.cpu_count() - cpu_to_relax)
    g_addrr = "/home/c6/Desktop/OpenWPM/jsons/Prediction_new/non_temporal_unweighted/"
    #non_connected_link_feature_extraction(2020, g_addrr)
    #results = pool.starmap(non_connected_link_feature_extraction, zip(years, itertools.repeat(g_addrr)))
    #pool.close()
    #pool.join()


    # 3. Make DataFrame
    root = "/home/c6/Desktop/OpenWPM/jsons/Prediction_new/non_temporal_unweighted/"
    #DataFrame_creation(2012, root)


    cpu_to_relax = 3
    pool = ThreadPool(processes=multiprocessing.cpu_count() - cpu_to_relax)
    g_addrr = "/home/c6/Desktop/OpenWPM/jsons/Prediction_new/non_temporal_unweighted/"
    results = pool.starmap(DataFrame_creation, zip(years, itertools.repeat(g_addrr)))
    pool.close()
    pool.join()



if __name__ == '__main__':
    main()

