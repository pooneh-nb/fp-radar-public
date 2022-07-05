import community as community_louvian
import networkx as nx
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import json
from myCodes.AST import utilities
import operator


def make_partitions():
    with open("/home/pooneh/Desktop/OpenWPM/jsons/AST/umar_ds/nodes_tuple.json", "rt") as nod:
        nodes_list = json.load(nod)
    nodes = [tuple(l) for l in nodes_list]
    with open("/home/pooneh/Desktop/OpenWPM/jsons/AST/umar_ds/edges_tuple.json", "rt") as ed:
        edges_list = json.load(ed)
    edges = [tuple(ee) for ee in edges_list]

    G = nx.Graph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    partition = community_louvian.best_partition(G, resolution=0.95)
    print(set(partition.values()))

    #assign apis to groups
    with open("/home/pooneh/Desktop/OpenWPM/jsons/AST/umar_ds/api_hash_frac.json", "rt") as api:
        api_hash_fract = json.load(api)
    louvain_part = {}
    # assign each api to a group which is made by louvain
    for key, value in partition.items():
        api_hash_fract[key]['louvain_partitioning'] = value
    with open("/home/pooneh/Desktop/OpenWPM/jsons/AST/umar_ds/louvian_resolution_test/partitions/api_hash_frac_louvian_0.95.json",
              "w") as lo:
        json.dump(api_hash_fract, lo, indent=4)


def calc_fp_group():
    with open("/home/pooneh/Desktop/OpenWPM/jsons/AST/umar_ds/louvian_resolution_test/partitions/api_hash_frac_louvian_0.95.json", "rt") as api:
        api_louvain = json.load(api)

    num_of_partitions = len(api_louvain.items())
    louvain_cluster = {}

    print(len(api_louvain.items()))
    api_list  = []
    fraction = 0
    for i in range(num_of_partitions+1):
        for key, value in api_louvain.items():
            if value['louvain_partitioning'] == i:
                api_list.append(key)
                fraction = fraction + value['node_weight']
        louvain_cluster[str(i)] = {'api_list': api_list, 'fraction': fraction}

    #for key, value in louvain_cluster.items():
        #print(key, value['fraction'])

    #print(louvain_cluster['13']['api_list'])

    with open("/home/pooneh/Desktop/OpenWPM/jsons/AST/umar_ds/louvian_resolution_test/partition_report/louvian_clusters_0.95.json", "w") as r:
        json.dump(louvain_cluster, r, indent=4)


def compare_with_fpjs2():

    with open("/home/pooneh/Desktop/OpenWPM/myCodes/AST/jsons/fingerprinting_js2.txt", 'r') as file:
        bench_lib = file.read().splitlines()

    with open("/home/pooneh/Desktop/OpenWPM/jsons/AST/umar_ds/louvian_resolution_test/partition_report/"
              "louvian_clusters_0.95.json", "rt") as r:
        louvain_cluster = json.load(r)

        max = 0
        for key, value in louvain_cluster.items():
            if value['fraction'] > max:
                max = value['fraction']
                group_inx = key
        print(max, group_inx)

        danger = 0
        for api in louvain_cluster[group_inx]['api_list']:
            if api in bench_lib:
                danger += 1
        print("Percent of appereance in fpjs2 library: ", 100 * danger/len(louvain_cluster[group_inx]['api_list']))

#make_partitions()
#calc_fp_group()
compare_with_fpjs2()


