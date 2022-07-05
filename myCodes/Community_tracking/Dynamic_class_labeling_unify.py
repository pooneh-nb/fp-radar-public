from myCodes.AST import utilities
import os

# Create a Dataset API-Interface-keyword
def create_apikeyw_interface(interface_keyword, outdir):
    # input: interface_apikeyw.json
    # output: apikeyw_interface.json
    # problem : missing interfaces without any API (30 interface)
    keyword_interface = {}
    for interface, api_keywlist in interface_keyword.items():
        for keyw in api_keywlist:
            if keyw not in keyword_interface.keys():
                keyword_interface[keyw] = []
                keyword_interface[keyw].append(interface)
            else:
                keyword_interface[keyw].append(interface)
    utilities.write_json(os.path.join(outdir, "labeling_clusters_edited/keyword_interface.json"), keyword_interface)


def create_interface_API(API_interface, outdir):
    # input: API_interface.json
    # output: interface_API.json
    interface_API = {}
    for API, interface_list in API_interface.items():
        for interface in interface_list:
            if interface not in interface_API.keys():
                interface_API[interface] = []
                interface_API[interface].append(API)
            else:
                interface_API[interface].append(API)
    utilities.write_json(os.path.join(outdir, "labeling_clusters_edited/interface_API.json"), interface_API)


def mono_mapping(keyword_interface, interface_APIs, API_interface, interface_keyword, outdir):
    API_interface_keyw = {}
    for api_keyword, interface_list in keyword_interface.items():
        if len(interface_list) == 1: # 1, 4, 6
            # 1 & 4
            for interface in interface_list:
                if interface in interface_APIs.keys():
                    if len(interface_APIs[interface]) == 1: # 1 ==>  keep it
                        API = interface_APIs[interface][0]
                        if API not in API_interface_keyw.keys():
                            API_interface_keyw[API] = {"interface": [], "api_keyw": []}
                            API_interface_keyw[API]["interface"].append(interface)
                            API_interface_keyw[API]["api_keyw"].append(api_keyword)
                            print("1==>", API, interface, api_keyword)
                            continue
                        API_interface_keyw[API]["interface"].append(interface)
                        API_interface_keyw[API]["api_keyw"].append(api_keyword)
                        print("1==>", API, interface, api_keyword)
                        continue

                if interface not in interface_APIs.keys(): # 4 ==> keep it
                    if interface not in API_interface_keyw.keys():
                        API_interface_keyw[interface] = {"interface": [], "api_keyw": []}
                        API_interface_keyw[interface]["api_keyw"].append(api_keyword)
                        print("4==>", interface, api_keyword)
                        continue
                    API_interface_keyw[interface]["api_keyw"].append(api_keyword)
                    print("4==>", interface, api_keyword)
                    continue

                ## Never happens!
                if interface in interface_APIs.keys():  # 4 ==> keep it
                    if len(interface_APIs[interface]) == 0:
                        if interface not in API_interface_keyw.keys():
                            API_interface_keyw[API] = {"interface": [], "api_keyw": []}
                            API_interface_keyw[interface]["api_keyw"].append(api_keyword)
                            print("OHHH")
                            continue
                        API_interface_keyw[interface]["api_keyw"].append(api_keyword)
                        print("OHHHH")
                        continue

                    if len(interface_APIs[interface]) > 1: # 6
                        # remove it
                        continue

        if len(interface_list) > 1: # 2 , 5, 8
            api_set = set()
            for interface in interface_list:
                if interface in interface_APIs.keys():
                    for api in interface_APIs[interface]:
                        api_set.add(api)
            if len(api_set) == 1: #2 , 2'
                # keep
                API = api_set.pop()
                for interface in interface_list:
                    if interface in API_interface[API]: # 2
                        if API not in API_interface_keyw.keys():
                            API_interface_keyw[API] = {"interface": [], "api_keyw": []}
                            API_interface_keyw[API]["interface"].append(interface)
                            API_interface_keyw[API]["api_keyw"].append(api_keyword)
                            print("2==>", API, interface, api_keyword)
                        else:
                            API_interface_keyw[API]["interface"].append(interface)
                            API_interface_keyw[API]["api_keyw"].append(api_keyword)
                            print("2==>", API, interface, api_keyword)
                            continue
                    else: # 2'
                        if interface not in API_interface_keyw.keys():
                            API_interface_keyw[interface] = {"interface": [], "api_keyw": []}
                            API_interface_keyw[interface]["api_keyw"].append(api_keyword)
                            print("2'==>", interface, api_keyword)
                            continue
                        API_interface_keyw[interface]["api_keyw"].append(api_keyword)
                        print("2'==>", interface, api_keyword)
                        continue




                """else:
                    for interface in interface_list:
                        API_interface_keyw[API]["interface"].append(interface)
                        print("2==>", API, interface, api_keyword)
                    API_interface_keyw[API]["api_keyw"].append(api_keyword)
                    continue"""
            else:   # 5, 8
                # remove
                continue

    for interface, apikeyw_list in interface_keyword.items(): # 3 , 7
        if len(apikeyw_list) == 0:
            if interface in interface_APIs.keys():
                if len(interface_APIs[interface]) == 1: # 3
                    # keep
                    API = interface_APIs[interface][0]
                    if API not in API_interface_keyw.keys():
                        API_interface_keyw[API] = {"interface": [], "api_keyw": []}
                        API_interface_keyw[API]["interface"].append(interface)
                        print("3==>", API, interface)
                        continue
                    else:
                        API_interface_keyw[API]["interface"].append(interface)
                        print("3==>", API, interface)
                        continue
            else:  # 7
                # remove
                continue
    # print(API_interface_keyw)
    utilities.write_json(os.path.join(outdir, "labeling_clusters_edited/API_interface_keyw.json"), API_interface_keyw)


def setify_API_interface_keyw(API_interface_keyw, outdir):
    for API, value in API_interface_keyw.items():
        interface_list = list(set([inter for inter in value["interface"]]))
        API_interface_keyw[API]["interface"] = interface_list

        keyw_list = list(set([keyw for keyw in value["api_keyw"]]))
        API_interface_keyw[API]["api_keyw"] = keyw_list

    utilities.write_json(os.path.join(outdir, "labeling_clusters_edited/API_interface_keyw.json"), API_interface_keyw)


def test_mono_keywords(API_interface_keyw):
    for root, value in API_interface_keyw.items():
        for keyword in value["api_keyw"]:
            for root_next, value_next in API_interface_keyw.items():
                if root != root_next:
                    if keyword in value_next["api_keyw"]:
                        print(root, root_next, keyword)


def freq_of_api_keywords(base_dir, API_interface_keyw):
    selected_dynamic_communities = utilities.read_json(
        os.path.join(base_dir, "selected_comms/selected_DY_communities.json"))

    for dy_name, static_com_list in selected_dynamic_communities.items():
        label_dict = {}
        for member in static_com_list:
            static_name = member[0]
            year = member[1]
            static_comm = utilities.read_json(os.path.join("/home/c6/Desktop/OpenWPM/jsons/community_tracking/"
                                                           "real_graphs/",str(year), static_name))
            for api_keyword in static_comm:
                for root, keyvalues in API_interface_keyw.items():
                    if api_keyword == root:
                        if root not in label_dict.keys():
                            label_dict[root] = 1
                        else:
                            label_dict[root] += 1

                    if api_keyword in keyvalues["interface"]:
                        if root not in label_dict.keys():
                            label_dict[root] = 1
                        else:
                            label_dict[root] += 1

                    if api_keyword in keyvalues["api_keyw"]:
                        if root not in label_dict.keys():
                            label_dict[root] = 1
                        else:
                            label_dict[root] += 1

        utilities.write_json(os.path.join(base_dir, "labeling_clusters_edited/dynamic_cluster_weights", dy_name + ".json"), label_dict)

# Frequency of APIs
def normalize_class_wight(base_dir, API_interface_keyw):
    selected_dynamic_communities = utilities.read_json(
        os.path.join(base_dir, "selected_comms/selected_DY_communities.json"))

    for dyname, stat_comms in selected_dynamic_communities.items():
        dynamic_cluster_length = len(stat_comms)
        freq_report = utilities.read_json(
            os.path.join(base_dir, "labeling_clusters_edited/dynamic_cluster_weights", dyname + ".json"))

        for root in freq_report:
            if root == "Vibration":
                print("Stop")
            len_root = len(API_interface_keyw[root]["interface"]) + len(API_interface_keyw[root]["api_keyw"]) + 1
            freq_report[root] = round((freq_report[root]) / (dynamic_cluster_length * len_root) * 100, 2)

        utilities.write_json(
            os.path.join(base_dir, "labeling_clusters_edited/normalized_by_cluster_weights", dyname + ".json"),
            freq_report)


def select_only_normalized_APIs(normalized_address, APIs):
    normalized_clusters = utilities.get_files_in_a_directory(normalized_address)
    for cluster in normalized_clusters:
        cluster_context = utilities.read_json(cluster)
        cluster_name = cluster.split('/')[-1]
        cluster_freq_dict = {}
        for root, value in cluster_context.items():
            if root in APIs:
                cluster_freq_dict[root] = value
        utilities.write_json(os.path.join(normalized_address, "only_APIs"+cluster_name), cluster_freq_dict)


# Frequency of Keywords
def api_frequency(base_dir):
    selected_dynamic_communities = utilities.read_json(
        os.path.join(base_dir, "selected_comms/selected_DY_communities.json"))

    for dy_name, static_comms in selected_dynamic_communities.items():
        keyword_dict = {}
        dynamic_length = len(static_comms)
        for static_comm in static_comms:
            static_name = static_comm[0]
            year = str(static_comm[1])
            static_keywords = utilities.read_json(os.path.join
                                                  ("/home/c6/Desktop/OpenWPM/jsons/community_tracking/real_graphs",
                                                   year, static_name))
            for keyw in static_keywords:
                if keyw not in keyword_dict.keys():
                    keyword_dict[keyw] = 1
                else:
                    keyword_dict[keyw] += 1

        keyword_dict = dict(sorted(keyword_dict.items(), key=lambda kv: kv[1], reverse=True))
        utilities.write_json(os.path.join(base_dir, "labeling_clusters_edited/keyword_level_labeling/dynamic_cluster_weights",
                                          dy_name), keyword_dict)

        for keyw, freq in keyword_dict.items():
            keyword_dict[keyw] = freq / dynamic_length
        keyword_dict = dict(sorted(keyword_dict.items(), key=lambda kv: kv[1], reverse=True))
        utilities.write_json(os.path.join(base_dir, "labeling_clusters_edited/keyword_level_labeling/normalized_by_cluster_weights",
                                          dy_name), keyword_dict)


def main():
    base_dir = "/home/c6/Desktop/OpenWPM/jsons/community_tracking/real_graphs/DY_COMM"
    interface_keyword = utilities.read_json(os.path.join(base_dir, "labeling_clusters_edited/interface_keyword.json"))
    API_interface = utilities.read_json(os.path.join(base_dir, "labeling_clusters_edited/API_interface_dict.json"))
    normalized_addr = "/home/c6/Desktop/OpenWPM/jsons/community_tracking/real_graphs/DY_COMM/labeling_clusters_edited/normalized_by_cluster_weights"
    APIs = utilities.read_json(os.path.join(base_dir, "labeling_clusters_edited/APIs.json"))
    Umars_keywords = list(utilities.read_file_newline_stripped("/home/c6/Desktop/OpenWPM/myCodes/AST/jsons/cleaned_apis_unique.txt"))

    create_apikeyw_interface(interface_keyword, base_dir)
    create_interface_API(API_interface, base_dir)

    interface_API = utilities.read_json(os.path.join(base_dir, "labeling_clusters_edited/interface_API.json"))
    keyword_interface = utilities.read_json(os.path.join(base_dir, "labeling_clusters_edited/keyword_interface.json"))
    mono_mapping(keyword_interface, interface_API, API_interface, interface_keyword, base_dir)
    API_interface_keyw = utilities.read_json(os.path.join(base_dir, "labeling_clusters_edited/API_interface_keyw.json"))
    setify_API_interface_keyw(API_interface_keyw, base_dir)

    # test_mono_keywords(API_interface_keyw)

    # Frequency of APIs
    freq_of_api_keywords(base_dir, API_interface_keyw)
    normalize_class_wight(base_dir, API_interface_keyw)

    # filter out interfaces
    # select_only_normalized_APIs(normalized_addr, APIs)

    ## Frequency of keywords
    #api_frequency(base_dir)

    #### test
    """my_keywords = set()
    # length of keywords: 4934
    print(len(keyword_interface.keys()))
    my_keywords.update(keyword_interface.keys())
    # length of interfaces : 1026
    print(len(interface_API.keys()))
    my_keywords.update(interface_API.keys())
    # length of APIs 87
    print(len(APIs))
    my_keywords.update(APIs)
    # length of umar's keywords: 6167
    print(len(Umars_keywords))
    print(len(my_keywords))
    difference = []
    for keyw in Umars_keywords:
        if keyw not in list(my_keywords):
            difference.append(keyw)
    for keyw in difference:
        print(keyw)"""


if __name__ == '__main__':
    main()
