# output : DY_COMM/number.json

import os
from os import listdir
from os.path import isfile, join
import re
from myCodes.AST import utilities
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
from multiprocessing import Pool as ThreadPool
import multiprocessing
import numpy as np


def extract_class(api_name):
    api_class = []
    page_load_timeout = 4
    file_write_timeout = 4

    options = Options()
    options.headless = True
    DRIVER_PATH = '/home/c6/Downloads/chromedriver'

    driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
    driver.set_page_load_timeout(page_load_timeout)

    try:
        driver.get("https://developer.mozilla.org/en-US/search?q=" + api_name + "+")
        time.sleep(file_write_timeout)
        link_lists = driver.find_elements_by_partial_link_text('/en-US/docs/Web/API/')
        for link in link_lists:
            if link.text.split('/')[-1] == api_name:
                api_class.append(link.text.split('/')[-2])
                #print(api_name," : ",link.text.split('/')[-2])
        driver.quit()
        return api_class

    except Exception as ex:
        time.sleep(4)
        print(ex)


def call_execute_class_multiproc(static_comm):
    if static_comm.split('/')[-1].startswith("C_"):
        year = static_comm.split('/')[-2]
        base_dir = "/home/c6/Desktop/OpenWPM/jsons/community_tracking/real_graphs"
        print("processing: ", year, static_comm.split('/')[-1])
        api_class = {}
        members_of_static_comm = utilities.read_json(static_comm)
        for api in members_of_static_comm:
            api_class[api] = extract_class(api)
        utilities.write_json(os.path.join(base_dir, "api-class", str(year), static_comm.split('/')[-1]), api_class)


def create_multiprocess_dy_comms(dycm_id, dymc_membr):
    pass

def main():

    # community labeling
    dy_comms = utilities.read_json(
        "/home/c6/Desktop/OpenWPM/jsons/community_tracking/real_graphs/DY_COMM/selected_DY_communities.json")
    static_comm_base = "/home/c6/Desktop/OpenWPM/jsons/community_tracking/real_graphs"
    # api_class = utilities.read_json()
    dy_comm_dic = {}

    for dycm_id, dymc_membr in dy_comms.items():
        dy_comm_dic[dycm_id] = {}
        for static_com in dymc_membr:
            print("start: ", dycm_id, "+", static_com)
            class_of_api = []
            api_class = []
            for api in utilities.read_json(os.path.join(static_comm_base, str(static_com[1]), static_com[0])):
                class_of_api = extract_class(api)
                api_class.append((api, class_of_api))
            dy_comm_dic[dycm_id][(str(static_com[0]), static_com[1], static_com[2])] = {
                "static_comm": static_com[0],
                "year": static_com[1],
                "status": static_com[2],
                "api_class": class_of_api
            }
    utilities.write_json(os.path.join("/home/c6/Desktop/OpenWPM/jsons/community_tracking/real_graphs/DY_COMM",
                                        dycm_id+".json"), dy_comm_dic)
    """time.sleep(60)
    # specify class name to each api
    base_dir = "/home/c6/Desktop/OpenWPM/jsons/community_tracking/real_graphs"
    years = np.arange(2010,2020,1)
    for year in years:
        static_comm_dir = os.path.join(base_dir, str(year))
        static_comms = utilities.get_files_in_a_directory(static_comm_dir)

        cpu_to_relax = 6
        pool = ThreadPool(processes=multiprocessing.cpu_count() - cpu_to_relax)
        results = pool.map(call_execute_class_multiproc, static_comms)
        pool.close()
        pool.join()"""




if __name__ == '__main__':
    main()
