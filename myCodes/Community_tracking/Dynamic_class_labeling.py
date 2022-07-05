import os
from myCodes.AST import utilities


def freq_of_interfaced_and_apis(base_dir):

    selected_dynamic_communities = utilities.read_json(
        os.path.join(base_dir, "DY_COMM/selected_comms/selected_DY_communities.json"))
    interface_dict = utilities.read_json(os.path.join(base_dir, "DY_COMM/labeling_clusters/interface_keyword.json"))
    api_interface_dict = utilities.read_json(
        os.path.join(base_dir, "DY_COMM/labeling_clusters/API_interface_dict_with_unknown.json"))

    # report the frequency of interface and APIs in each dynamic community
    for dy_name, static_com_list in selected_dynamic_communities.items():
        api_interface_freq = {"interfaces": {}, "APIs": {}}
        interface_set_each_dy_com = set()
        for member in static_com_list:
            static_name = member[0]
            year = member[1]
            static_comm = utilities.read_json(os.path.join(base_dir, str(year), static_name))
            for keyword in static_comm:
                for interface, api_keyword_list in interface_dict.items():
                    # compare with interface.key
                    if keyword == interface:
                        if interface in api_interface_freq["interfaces"].keys():
                            api_interface_freq["interfaces"][interface] += 1
                        else:
                            api_interface_freq["interfaces"][interface] = 1
                        # increase related API
                        for api_name, interface_list in api_interface_dict.items():
                            if interface in interface_list:
                                if api_name in api_interface_freq["APIs"].keys():
                                    api_interface_freq["APIs"][api_name] += 1
                                else:
                                    api_interface_freq["APIs"][api_name] = 1
                    # compare with list of keywords
                    if keyword in api_keyword_list:
                        #interface_set_each_dy_com.add(interface)
                        if interface in api_interface_freq["interfaces"].keys():
                            api_interface_freq["interfaces"][interface] += 1
                        else:
                            api_interface_freq["interfaces"][interface] = 1
                        # increase related API
                        for api_name, interface_list in api_interface_dict.items():
                            if interface in interface_list:
                                if api_name in api_interface_freq["APIs"].keys():
                                    api_interface_freq["APIs"][api_name] += 1
                                else:
                                    api_interface_freq["APIs"][api_name] = 1

                # check whether the keyword is an API name
                for api_name, interface_list in api_interface_dict.items():
                    if keyword == api_name:
                        if api_name in api_interface_freq["APIs"].keys():
                            api_interface_freq["APIs"][api_name] += 1
                        else:
                            api_interface_freq["APIs"][api_name] = 1

                    """if interface in interface_list:
                        if api_name in api_interface_freq["APIs"].keys():
                            api_interface_freq["APIs"][api_name] += 1
                        else:
                            api_interface_freq["APIs"][api_name] = 1"""

            """for interface in interface_set_each_dy_com:
                for api_name, interface_list in api_interface_dict.items():
                    if interface in interface_list:
                        if api_name in api_interface_freq["APIs"].keys():
                            api_interface_freq["APIs"][api_name] += 1
                        else:
                            api_interface_freq["APIs"][api_name] = 1"""
        utilities.write_json(
            os.path.join(base_dir, "DY_COMM/labeling_clusters/before_monoliza/dynamic_cluster_weights", dy_name + ".json"),
            api_interface_freq)


def normalize_class_wight(base_dir):
    selected_dynamic_communities = utilities.read_json(
        os.path.join(base_dir, "DY_COMM/selected_comms/selected_DY_communities.json"))
    interface_dict = utilities.read_json(os.path.join(base_dir, "DY_COMM/labeling_clusters/interface_keyword.json"))
    api_interface_dict = utilities.read_json(
        os.path.join(base_dir, "DY_COMM/labeling_clusters/API_interface_dict_with_unknown.json"))

    for dyname, stat_comms in selected_dynamic_communities.items():
        dynamic_cluster_length = len(stat_comms)
        freq_report = utilities.read_json(
            os.path.join(base_dir, "DY_COMM/labeling_clusters/before_monoliza/dynamic_cluster_weights", dyname + ".json"))
        for interface in freq_report["interfaces"]:
            try:
                if len(interface_dict[interface]) == 0:
                    dominator = 1
                else:
                    dominator = (freq_report["interfaces"][interface]) / \
                                                     (dynamic_cluster_length * len(interface_dict[interface]))
                freq_report["interfaces"][interface] = round(dominator * 100, 2)
            except Exception as e:
                print(e, interface, dyname)

        for api in freq_report["APIs"]:
            # calculate the denominator of API service
            # API_I = [interface_1, interface_2] = set([properties of interface_1] + [properties of interface_2])
            length_of_denominator = len(set([api_key for interf in api_interface_dict[api] for api_key in interface_dict[interf]]))
            freq_report["APIs"][api] = round((freq_report["APIs"][api]) / (dynamic_cluster_length * length_of_denominator) * 100, 2)
        #sorted_context = sorted(freq_report.items(), key=lambda kv: kv["APIs"][1], reverse=True)
        utilities.write_json(os.path.join(base_dir, "DY_COMM/labeling_clusters/before_monoliza/normalized_by_cluster_weights", dyname+".json"), freq_report)


# report apis and interfaces with value more than 100
def report_abnormal_interface_and_apis(base_dir):
    base_dir = base_dir+"/DY_COMM"
    selected_dynamic_communities = utilities.read_json(
        os.path.join(base_dir, "selected_comms/selected_DY_communities.json"))

    interface_dict = utilities.read_json(os.path.join(base_dir, "labeling_clusters/interface_keyword.json"))

    api_interface_dict = utilities.read_json(
        os.path.join(base_dir, "labeling_clusters/API_interface_dict.json"))

    for dy_name, static_com_list in selected_dynamic_communities.items():
        freq_report = utilities.read_json(
            os.path.join(base_dir, "labeling_clusters/before_monoliza/normalized_by_cluster_weights", dy_name + ".json"))
        for interface in freq_report["interfaces"]:
            if freq_report["interfaces"][interface] > 100:
                print(dy_name, interface, "==>interface")
        for api in freq_report["APIs"]:
            if freq_report["APIs"][api] > 100:
                print(dy_name, api, "=+>api")


def main():
    base_dir = "/home/c6/Desktop/OpenWPM/jsons/community_tracking/real_graphs"
    # 1. # report the frequency of interface and APIs in each dynamic community
    #freq_of_interfaced_and_apis(base_dir)

    # 2. normalize frequency on interfaces and APIs
    #normalize_class_wight(base_dir)

    # 3. report apis and interfaces with value more than 100
    report_abnormal_interface_and_apis(base_dir)


if __name__ == '__main__':
    main()
