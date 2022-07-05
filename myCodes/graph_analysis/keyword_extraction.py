from myCodes.AST import utilities
import numpy as np

# if you want to predict 2011, the list of keywords of 2010 and 2011 is stored in 2011
def extract_unique_apis(keyword_list_current, api_features_future, completed_keyword_dir):
    #api_features_list1 = utilities.get_files_in_a_directory(api_features_current)
    #api_features_list2 = utilities.get_files_in_a_directory(api_features_future)
    api_features_list = utilities.get_files_in_a_directory(api_features_future)


    keywrd_list = set(keyword_list_current)

    for script in api_features_list:
        script_content = utilities.read_list_compressed(script)
        apis_in_script_content = list(script_content)
        for keyw in apis_in_script_content:
            #print(keyw)
            keywrd_list.add(keyw)
    print(len(keywrd_list))
    utilities.write_json(completed_keyword_dir, list(keywrd_list))


def main():

    years = np.arange(2013,2021,1)
    for year in years:
        keyword_list_current = utilities.read_json("/home/c6/Desktop/OpenWPM/jsons/Prediction/"+str(year)+"/node_list.json")
        api_features_future = "/home/c6/Desktop/OpenWPM/jsons/AST/CDX_results/Graphs/"+str(year+1)+"/api_features"
        completed_keyword = "/home/c6/Desktop/OpenWPM/jsons/Prediction/"+str(year+1)+"/node_list.json"
        extract_unique_apis(keyword_list_current, api_features_future, completed_keyword)


if __name__ == '__main__':
    main()