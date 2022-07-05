from myCodes.AST import utilities
from shutil import copy
from multiprocessing import Pool as ThreadPool
import multiprocessing
import os
import numpy as np
import networkx as nx
from networkx.readwrite import json_graph

"""
## get the hash of fp and non fp files
non_fp_organized = "/home/c6/Desktop/OpenWPM/jsons/CDX_api/gathered_downloaded_files/non_fp_date_organized/2019_unique/all"
fp_directory = "/home/c6/Desktop/OpenWPM/jsons/CDX_api/gathered_downloaded_files/fp_date_organized/2019/all"

#non_fp_organized = "/home/c6/Desktop/OpenWPM/jsons/AST/umar_ds/second_try/fp_non_fp/non_fp_hashes.json"
#fp_directory = "/home/c6/Desktop/OpenWPM/jsons/AST/umar_ds/second_try/fp_non_fp/fp_hashes.json"

raw_fp_files = utilities.get_files_in_a_directory(fp_directory)
raw_non_fp_files = utilities.get_files_in_a_directory(non_fp_organized)

fp_list = set([file.split('|')[1] for file in raw_fp_files])
non_fp_list = set([file.split('|')[1] for file in raw_non_fp_files])


print(len(fp_list))

print(len(non_fp_list))

#manager = multiprocessing.Manager()
#api_attendancy = manager.dict()
"""

"""def edit_umar_files(api_features):
    api_features_files = utilities.get_files_in_a_directory(api_features)
    for fil in api_features_files:
        script_content = utilities.read_list_compressed(fil)
        new_file = []
        for pair in script_content:
            new_pair = pair.split(':')[1]
            new_file.append(new_pair)
        name_fil = fil.split('/')[-1]
        utilities.write_list_compressed(os.path.join("/home/c6/Desktop/OpenWPM/jsons/AST/umar_ds/second_try/new_apis",name_fil), new_file)"""


# first call this to have all api_features in a unique directory
def api_feature_file_unify():
    years = list(np.arange(2010,2021,1))

    for year in years:
        final_feature_dir = "/home/c6/Desktop/OpenWPM/jsons/AST/CDX_results/Graphs/"+str(year)+"/api_features"
        if not os.path.exists(final_feature_dir):
            os.makedirs(final_feature_dir)
        fp_js = utilities.get_files_in_a_directory\
            ("/home/c6/Desktop/OpenWPM/jsons/AST/CDX_results/fp_files/"+str(year)+"/api_features")

        non_fp_js = utilities.get_files_in_a_directory\
            ("/home/c6/Desktop/OpenWPM/jsons/AST/CDX_results/non_fp_files/"+str(year)+"/api_features")

        for api_fi in fp_js:
            copy(api_fi, final_feature_dir)
        for api_f in non_fp_js:
            copy(api_f, final_feature_dir)


"""def extract_unique_apis(api_features, keyword_dir):
    api_features_list = utilities.get_files_in_a_directory(api_features)
    keywrd_list = set()

    for script in api_features_list:
        script_content = utilities.read_list_compressed(script)
        apis_in_script_content = list(script_content)
        for keyw in apis_in_script_content:
            print(keyw)
            keywrd_list.add(keyw)
    print(len(keywrd_list))
    utilities.write_json(keyword_dir, list(keywrd_list))

    #with open("/home/c6/Desktop/OpenWPM/jsons/AST/CDX_results/Graphs/2019/keyword_list.json", 'w') as kw:
        #json.dump(list(keywrd_list), kw, indent=4)

def find_attending_scripts(keyw):
    #print(keyw)
    #script_apis_dir = "/home/c6/Desktop/OpenWPM/jsons/AST/CDX_results/Graphs/2019/api_features"

    #scripts_apis_list = utilities.get_files_in_a_directory(script_apis_dir)
    api_hash_list = []
    for script_api in scripts_apis_list:
        script_content_list = set(utilities.read_list_compressed(script_api))
        #print(script_content_list)
        if keyw in script_content_list:
            script_name = script_api.split('/')[-1].split('.')[0].split('_')[-1]
           #print(script_name, keyw)
            api_hash_list.append(script_name)
    api_attendancy[keyw] = api_hash_list
    #print(api_attendancy)
    print(len(api_attendancy))


def add_hash_as_key(api_attend, api_hash_frac_addr):
    # this should be used after finding attending scripts
    #with open("/home/c6/Desktop/OpenWPM/jsons/AST/CDX_results/Graphs/2019/api_attendancy.json", 'rt') as at:
        #api_attend = json.load(at)
    api_attend = utilities.read_json(api_attend)
    temp_dict ={}
    for api_key, hash_values in api_attend.items():
        temp_dict[api_key] = {'hash': hash_values}
    utilities.write_json(api_hash_frac_addr, temp_dict)
    #with open("/home/c6/Desktop/OpenWPM/jsons/AST/CDX_results/Graphs/2019/api_attendancy.json", 'w') as att:
         #json.dump(temp_dict, att, indent=4)


def calc_fraction(api_hash_frac):
    #with open("/home/c6/Desktop/OpenWPM/jsons/AST/CDX_results/Graphs/2019/api_attendancy.json", 'rt') as att:
        #api_hash = json.load(att)
    api_hash = utilities.read_json(api_hash_frac)
    for api_key, hash_values in api_hash.items():
        hash_values_set = set(hash_values['hash'])
        print(hash_values_set)
        fp_frac = len(hash_values_set.intersection(fp_list))
        non_fp_frac = len(hash_values_set.intersection(non_fp_list))
        print(fp_frac, non_fp_frac)
        if non_fp_frac == 0 and fp_frac != 0:
            fraction = 10000
            print("boomb!")
        if fp_frac == 0:
            fraction = 0
        if non_fp_frac != 0 and fp_frac != 0:
            fraction = round(fp_frac / non_fp_frac,3)
            print(fraction)
            #temp = {"fp_frac": fp_frac, "non_fp_frac": non_fp_frac, "fraction": fraction}
        api_hash[api_key]['fp_frac'] = fp_frac
        api_hash[api_key]['non_fp_frac'] = non_fp_frac
        api_hash[api_key]['node_weight'] = fraction
        api_hash[api_key]['scripts'] = fp_frac + non_fp_frac
    utilities.write_json(api_hash_frac, api_hash)
    #with open("/home/c6/Desktop/OpenWPM/jsons/AST/CDX_results/Graphs/2019/api_hash_frac.json", 'w') as att:
        #json.dump(api_hash, att, indent=4)"""


def api_presence_without_type_and_with_hashes(feature_files_addr):

    out_dir = feature_files_addr.split('api_features')[0]
    out_dir = out_dir[:-1]
    print("Start --> ", out_dir.split('/')[-1])
    all_features = {}
    count = 1
    feature_files_addr = utilities.get_files_in_a_directory(feature_files_addr)
    for f_name in feature_files_addr:
        current_apis = set()
        file_hash = f_name.strip().split('/')[-1].split('|')[1].replace('.txt', '')
        file_content = utilities.read_list_compressed(f_name)

        for item in file_content:
            splitted_item = item
            if splitted_item not in current_apis:
                current_apis.add(splitted_item)
                if splitted_item not in all_features:
                    all_features[splitted_item] = {}
                    all_features[splitted_item]['id'] = count
                    all_features[splitted_item]['count'] = 1
                    all_features[splitted_item]['hashes'] = []
                    all_features[splitted_item]['hashes'].append(file_hash)
                    count += 1
                else:
                    all_features[splitted_item]['count'] = all_features[splitted_item]['count'] + 1
                    all_features[splitted_item]['hashes'].append(file_hash)

    utilities.write_json(os.path.join(out_dir, 'all_discovered_apis_with_hash.json'), all_features)
    print("End --> ", out_dir.split('/')[-1])


def make_graph(out_dir):
    year = out_dir.split('/')[-1]
    print("Start -->", year)
    all_features = utilities.read_json(os.path.join(out_dir, 'all_discovered_apis_with_hash.json'))
    all_files_addr = utilities.get_files_in_a_directory(os.path.join(out_dir, 'api_features'))
    fp_dir = out_dir.split('Graphs')[0] + 'fp_files/' + year + '/api_features'
    #positive_dir = utilities.get_files_in_a_directory(os.path.join(fp_dir, year))
    positive_dir = utilities.get_files_in_a_directory(fp_dir)
    positives_list = [fp.split('/')[-1].split('|')[1] for fp in positive_dir]

    api_graph = nx.Graph()

    ### add nodes
    positives_set = set()
    positives_set = set(positives_list)

    positives_count = len(positives_set)
    negative_count = len(all_files_addr) - len(positives_set)

    all_keys = []
    for key in all_features:
        #     if all_features[key]['count'] < 300:
        #         continue

        intersection_set = set(all_features[key]['hashes']).intersection(positives_set)
        p_count = len(intersection_set)
        n_count = len(set(all_features[key]['hashes'])) - p_count

        if n_count == 0:
            node_ratio = 'i'
        else:
            node_ratio = (p_count / positives_count) / (n_count / negative_count)

        node_weight = len(intersection_set) / positives_count

        #api_graph.add_node(all_features[key]['id'], api_name=key, node_weight=node_weight, ratio=node_ratio)
        api_graph.add_node(key, api_id=all_features[key]['id'], node_weight=node_weight, ratio=node_ratio)
        all_keys.append(key)

    print(year, "--> nodes: ", len(api_graph.nodes()))

    ### add edges
    for idx, key in enumerate(all_keys):
        check_hashes = set(all_features[key]['hashes'])
        for i in range(idx + 1, len(all_keys)):
            current_hashes = set(all_features[all_keys[i]]['hashes'])
            intersection_set = check_hashes.intersection(current_hashes)
            if len(intersection_set) > 0:
                # Ratio
                p_count = len(intersection_set.intersection(positives_set))
                n_count = len(intersection_set) - p_count

                if n_count == 0:
                    edge_ratio = 'i'
                else:
                    edge_ratio = (p_count / positives_count) / (n_count / negative_count)

                # Non-Ratio
                edge_weight = len(intersection_set) / (positives_count + negative_count)

                api_graph.add_edge(key, all_keys[i], weight=edge_weight, ratio=edge_ratio)
                #api_graph.add_edge(all_features[key]['id'], all_features[all_keys[i]]['id'], weight=edge_weight,
                                   #ratio=edge_ratio)

    print(year, "--> edges: ", len(api_graph.edges()))

    # weight normalization
    ratios = []
    for node in api_graph.nodes():
        if api_graph.nodes[node]['ratio'] != 'i':
            ratios.append(api_graph.nodes[node]['ratio'])

    #print(ratios[0])
    ratios.sort()
    #print(ratios[-1])

    max_val = ratios[-1]

    for node in api_graph.nodes():
        if api_graph.nodes[node]['ratio'] != 'i':
            api_graph.nodes[node]['correct_ratio'] = api_graph.nodes[node]['ratio'] / max_val
        else:
            api_graph.nodes[node]['correct_ratio'] = 1

    ratios = []
    for edge in api_graph.edges():
        if api_graph.edges[edge]['ratio'] != 'i':
            ratios.append(api_graph.edges[edge]['ratio'])

    #print(ratios[0])
    ratios.sort()
    #print(ratios[-1])

    max_val = ratios[-1]

    for edge in api_graph.edges():
        if api_graph.edges[edge]['ratio'] != 'i':
            api_graph.edges[edge]['correct_ratio'] = api_graph.edges[edge]['ratio'] / max_val
        else:
            api_graph.edges[edge]['correct_ratio'] = 1

    data = json_graph.node_link_data(api_graph)
    utilities.write_json(os.path.join(out_dir, 'Graph.json'), data)
    print(year, "--> done!")


def add_year_attr(graph_dir):
    year = graph_dir.split('/')[-1]

    g = utilities.read_json(os.path.join(graph_dir, 'Graph.json'))
    G = json_graph.node_link_graph(g)

    for edge in G.edges():
        G.edges[edge]['year'] = year

    data = json_graph.node_link_data(G)
    utilities.write_json(os.path.join(graph_dir, 'Graph.json'), data)


def main():
    #api_feature_file_unify()
    years = list(np.arange(2018, 2020, 1))
    out_dir = "/home/c6/Desktop/OpenWPM/jsons/AST/CDX_results/Graphs"

    # create api hashes
    api_features_list = []
    for year in years:
        api_features_list.append(os.path.join(out_dir, str(year) + '/api_features'))
    cpu_to_relax = 1
    
    pool = ThreadPool(processes=multiprocessing.cpu_count() - cpu_to_relax)
    results = pool.map(api_presence_without_type_and_with_hashes, api_features_list)
    pool.close()
    pool.join()

    ### call make graph
    graph_dir_list = []
    for year in years:
        graph_dir_list.append(out_dir + "/" + str(year))

    cpu_to_relax = 1
    pool = ThreadPool(processes=multiprocessing.cpu_count() - cpu_to_relax)
    results = pool.map(make_graph, graph_dir_list)
    pool.close()
    pool.join()

    # call add year attribute
    years = list(np.arange(2010, 2021, 1))
    out_dir = "/home/c6/Desktop/OpenWPM/jsons/AST/CDX_results/Graphs"

    graph_dir_list = []
    for year in years:
        graph_dir_list.append(out_dir + "/" + str(year))

    cpu_to_relax = 1
    pool = ThreadPool(processes=multiprocessing.cpu_count() - cpu_to_relax)
    results = pool.map(add_year_attr, graph_dir_list)
    pool.close()
    pool.join()

    #api_features = "/home/c6/Desktop/OpenWPM/jsons/AST/umar_ds/second_try/api_features/2019/api_features"
    #keyword_list = "/home/c6/Desktop/OpenWPM/jsons/AST/CDX_results/Graphs/2019/keyword_list.json"
    #api_attend_addr = "/home/c6/Desktop/OpenWPM/jsons/AST/CDX_results/Graphs/2019/api_attendancy.json"

    ###api_features = "/home/c6/Desktop/OpenWPM/jsons/AST/umar_ds/second_try/api_features"
    ###edit_umar_files(api_features)

    api_features = "/home/c6/Desktop/OpenWPM/jsons/AST/umar_ds/second_try/api_features"
    keyword_list_addr = "/home/c6/Desktop/OpenWPM/jsons/AST/umar_ds/second_try/keyword_list.json"
    api_attend_addr = "/home/c6/Desktop/OpenWPM/jsons/AST/umar_ds/second_try/api_attendancy.json"
    api_hash_frac_addr = "/home/c6/Desktop/OpenWPM/jsons/AST/umar_ds/second_try/api_hash_frac.json"
    #extract_unique_apis(api_features, keyword_list_addr)

    #keyword_list = utilities.read_json("/home/c6/Desktop/OpenWPM/jsons/AST/umar_ds/second_try/keyword_list.json")

    #cpu_to_relax = 1
    #print(multiprocessing.cpu_count())
    #pool = ThreadPool(processes=multiprocessing.cpu_count() - cpu_to_relax)
    #pool = ThreadPool(processes=1)
    #results = pool.map(find_attending_scripts, keyword_list)
    #pool.close()
    #pool.join()
    #print(len(api_attendancy.keys()))
    #utilities.write_json(api_attend_addr, dict(api_attendancy))
    #with open("/home/c6/Desktop/OpenWPM/jsons/AST/CDX_results/Graphs/2019/api_attendancy.json", 'w') as att:
        #json.dump(dict(api_attendancy), att, indent=4)
    #add_hash_as_key(api_attend_addr, api_hash_frac_addr)
    #calc_fraction(api_hash_frac_addr)


if __name__ == '__main__':
    main()
