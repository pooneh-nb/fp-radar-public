from myCodes.AST import utilities
import os
import numpy as np


def collect_suspicious_apis():
    fp_dy_cluster = utilities.read_json("/home/c6/Desktop/OpenWPM/jsons/community_tracking/real_graphs/DY_COMM"
                                        "/selected_comms/selected_DY_communities.json")["26"]
    static_clusters_base = "/home/c6/Desktop/OpenWPM/jsons/community_tracking/real_graphs"
    suspicious_apis = {}
    for static_cluster in fp_dy_cluster:
        static_name = static_cluster[0]
        static_year = str(static_cluster[1])
        suspicious_apis[static_year] = list(utilities.read_json(os.path.join(static_clusters_base, static_year, static_name)))
    return suspicious_apis


def detect_suspicious_scripts(base_dir_apis, out_dir):
    threshold = 15
    suspicious_apis = collect_suspicious_apis()
    years = np.arange(2013, 2014)
    for year in years:
        if year == 2012:
            break
        year = str(year)
        suspicious_apis_snapshot = set(suspicious_apis[year])
        fp_files = utilities.get_files_in_a_directory(os.path.join(base_dir_apis, "fp_files/" + year + "/api_features"))
        non_fp_files = utilities.get_files_in_a_directory(os.path.join(base_dir_apis, "non_fp_files/" + year + "/api_features"))

        for fp_file in fp_files:
            file_name = fp_file.split('/')[-1]
            fp_content = set(utilities.read_list_compressed(fp_file))
            common_keywords = fp_content.intersection(suspicious_apis_snapshot)
            if len(common_keywords) > threshold:
                utilities.write_list_compressed(os.path.join(out_dir, "suspicious", year, file_name), fp_content)
            else:
                utilities.write_list_compressed(os.path.join(out_dir, "non_suspicious", year, file_name), fp_content)

        for file in non_fp_files:
            file_name = file.split('/')[-1]
            fp_content = set(utilities.read_list_compressed(file))
            common_keywords = fp_content.intersection(suspicious_apis_snapshot)
            if len(common_keywords) > threshold:
                utilities.write_list_compressed(os.path.join(out_dir, "suspicious", year, file_name), fp_content)
            else:
                utilities.write_list_compressed(os.path.join(out_dir, "non_suspicious", year, file_name), fp_content)


def weighing_apis(base_dir_sus):
    suspicious_apis = collect_suspicious_apis()
    years = np.arange(2011, 2020)
    ddg_tracker_weight = {}
    for year in years:
        print(year)
        if year == 2012:
            year += 1
        year = str(year)
        ddg_tracker_weight[year] = {}
        for api in suspicious_apis[year]:
            suspicious_counter = 0
            non_suspicious_counter = 0

            suspicious_files = utilities.get_files_in_a_directory(os.path.join(base_dir_sus, "suspicious", year))
            non_suspicious_files = utilities.get_files_in_a_directory(
                os.path.join(base_dir_sus, "non_suspicious", year))
            suspicious_total = len(suspicious_files)
            non_suspicious_total = len(non_suspicious_files)

            for suspicious in suspicious_files:
                content = set(utilities.read_list_compressed(suspicious))
                if api in content:
                    suspicious_counter += 1

            for non_suspicious in non_suspicious_files:
                content = set(utilities.read_list_compressed(non_suspicious))
                if api in content:
                    non_suspicious_counter += 1
            # assign a weight
            if non_suspicious_counter == 0 and suspicious_counter != 0:
                api_weight = 1000000
            else:
                api_weight = (suspicious_counter / suspicious_total ) / (non_suspicious_counter / non_suspicious_total)
            ddg_tracker_weight[year][api] = api_weight
    utilities.write_json(os.path.join(base_dir_sus, "ddg_tracker_weight.json"), ddg_tracker_weight)


def main():
    base_dir_apis = "/home/c6/Desktop/OpenWPM/jsons/AST/CDX_results"
    out_dir = "/home/c6/Desktop/OpenWPM/jsons/ddg_tracker"
    #detect_suspicious_scripts(base_dir_apis, out_dir)
    weighing_apis(out_dir)


if __name__ == '__main__':
    main()
