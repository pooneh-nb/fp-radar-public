from myCodes.AST import utilities
import os
import numpy as np


def find_non_observed_keywords():
    clusters_dir = "/home/c6/Desktop/OpenWPM/jsons/community_tracking/real_graphs"
    API_interface_keyword = utilities.read_json(os.path.join(clusters_dir,
                                                             "DY_COMM/labeling_clusters/API_interface_keyw.json"))

    years = np.arange(2010,2020)
    for year in years:
        static_clusters = utilities.get_files_in_a_directory(os.path.join(clusters_dir, str(year)))
        static_keyword_glossary = set()
        fake_list = []
        for cluster in static_clusters:
            cluster_name = cluster.split('/')[-1]
            if not cluster_name.startswith("C_fake"):
                cluster_context = utilities.read_json(cluster)
                static_keyword_glossary.update(cluster_context)

        for root, value in API_interface_keyword.items():
            if root not in static_keyword_glossary:
                fake_list.append(root)
            for interface in value["interface"]:
                if interface not in static_keyword_glossary:
                    fake_list.append(interface)
            for keyw in value["api_keyw"]:
                if keyw not in static_keyword_glossary:
                    fake_list.append(keyw)
        utilities.write_json(os.path.join(clusters_dir, str(year), "C_fake"), fake_list)


def freq_of_api_keywords():
    clusters_dir = "/home/c6/Desktop/OpenWPM/jsons/community_tracking/real_graphs"
    API_interface_keyw = utilities.read_json(os.path.join(clusters_dir,
                                                             "DY_COMM/labeling_clusters/API_interface_keyw.json"))
    years = np.arange(2010, 2020)
    for year in years:
        static_clusters = utilities.get_files_in_a_directory(os.path.join(clusters_dir, str(year)))
        for static_cluster in static_clusters:
            api_freq = {}
            static_name = static_cluster.split("/")[-1]
            static_cluster_context = utilities.read_json(static_cluster)
            for keyw in static_cluster_context:
                for root, keyvalues in API_interface_keyw.items():
                    if keyw == root:
                        if root not in api_freq.keys():
                            api_freq[root] = 1
                        else:
                            api_freq[root] += 1
                    if keyw in keyvalues["interface"]:
                        if root not in api_freq.keys():
                            api_freq[root] = 1
                        else:
                            api_freq[root] += 1
                    if keyw in keyvalues["api_keyw"]:
                        if root not in api_freq.keys():
                            api_freq[root] = 1
                        else:
                            api_freq[root] += 1

            utilities.write_json(os.path.join("/home/c6/Desktop/OpenWPM/myCodes/Community_tracking"
                                              "/Sanity_Checking_drequency_labeling/Yearly_cluster_weights",
                                              str(year), static_name), api_freq)


def normalize_class_wight():
    clusters_dir = "/home/c6/Desktop/OpenWPM/jsons/community_tracking/real_graphs"
    API_interface_keyw = utilities.read_json(os.path.join(clusters_dir,
                                                          "DY_COMM/labeling_clusters/API_interface_keyw.json"))
    years = np.arange(2010, 2020)
    for year in years:
        static_freq_normal = {}
        static_cluster_freqs = utilities.get_files_in_a_directory\
            (os.path.join("/home/c6/Desktop/OpenWPM/myCodes/Community_tracking/Sanity_Checking_drequency_labeling/"
                          "Yearly_cluster_weights", str(year)))
        for static_cluster in static_cluster_freqs:
            static_cluster_context = utilities.read_json(static_cluster)
            for API, freq in static_cluster_context.items():
                len_root = len(API_interface_keyw[API]["interface"]) + len(API_interface_keyw[API]["api_keyw"]) + 1
                if API not in static_freq_normal.keys():
                    static_freq_normal[API] = static_cluster_context[API] / len_root
                else:
                    static_freq_normal[API] += (static_cluster_context[API] / len_root)
        utilities.write_json(os.path.join("/home/c6/Desktop/OpenWPM/myCodes/Community_tracking"
                                          "/Sanity_Checking_drequency_labeling/normalized_by_cluster_weights",
                                          str(year)), static_freq_normal)


def check_frequency_percentage():
    clusters_dir = "/home/c6/Desktop/OpenWPM/jsons/community_tracking/real_graphs"
    API_interface_keyw = utilities.read_json(os.path.join(clusters_dir,
                                                          "DY_COMM/labeling_clusters/API_interface_keyw.json"))
    freq_report = utilities.get_files_in_a_directory(
        os.path.join("/home/c6/Desktop/OpenWPM/myCodes/Community_tracking/Sanity_Checking_drequency_labeling/"
                     "normalized_by_cluster_weights"))

    API_frequency_accumulative = {}
    for dycomm in freq_report:
        try:
            dy_content = utilities.read_json(dycomm)
            for API in dy_content:
                if API not in API_frequency_accumulative.keys():
                    API_frequency_accumulative[API] = dy_content[API]
                else:
                    API_frequency_accumulative[API] = API_frequency_accumulative[API] + dy_content[API]
        except Exception as e:
            print(API, dycomm, e)

    utilities.write_json(os.path.join
                         ("/home/c6/Desktop/OpenWPM/myCodes/Community_tracking/Sanity_Checking_drequency_labeling",
                          "API_frequency_accumulative.json"), API_frequency_accumulative)


def compare_keywords():


    My_kewords = set()
    for root, value in API_interface_keyw.items():
        My_kewords.add(root)
        for interface in value["interface"]:
            My_kewords.add(interface)
        for keyw in value["api_keyw"]:
            My_kewords.add(keyw)

    All_keywords = set(utilities.read_file_newline_stripped("/home/c6/Desktop/OpenWPM/myCodes/AST/jsons/cleaned_apis_unique.txt"))
    print(All_keywords.difference(My_kewords))
    print(len(My_kewords))
    print(len(All_keywords))




def main():
    # find_non_observed_keywords()
    # freq_of_api_keywords()
    normalize_class_wight()
    # check_frequency_percentage()
    # compare_keywords()

    """freq_report = utilities.get_files_in_a_directory(
        os.path.join("/home/c6/Desktop/OpenWPM/myCodes/Community_tracking/Sanity_Checking_drequency_labeling/"
                     "normalized_by_cluster_weights"))
    for cluster in freq_report:
        cluster_context = utilities.read_json(cluster)
        if "Document_Object_Model" in cluster_context.keys():
            print(cluster_context["Document_Object_Model"])"""


if __name__ == '__main__':
    main()






