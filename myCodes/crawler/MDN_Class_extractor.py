from difflib import SequenceMatcher

from bs4 import BeautifulSoup
import requests
import urllib
import sys
# extract a class for each api in list of all apis
# output: jsons/community_tracking/api_class.json
# dictionary -> "API-keyword:[list of potential classes]"

from myCodes.AST import utilities
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
from multiprocessing import Pool as ThreadPool
import multiprocessing
import numpy as np
#manager = multiprocessing.Manager()
#api_class_dict = manager.dict()


# extract a class for each api in list of all apis
def extract_class(api_name):
    api_class = []
    page_load_timeout = 2
    file_write_timeout = 2

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
            if link.text.split('/')[-1] == api_name or link.text.split('/')[-1] == api_name+"()":
                api_class.append(link.text.split('/')[-2])
        driver.quit()
        return api_class

    except Exception as ex:
        time.sleep(4)
        print(ex)


def call_execute_class_multiproc(api_name, api_class_dict):
    class_list = api_class_dict[api_name]
    if len(class_list) == 0:
        edit_api_class(api_name, api_class_dict)


def call_to_extract_interface():
    try:
        url = 'https://developer.mozilla.org/en-US/docs/Web/API/'
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req, timeout=10)
        content = BeautifulSoup(response.read(), 'html.parser')
        raw_content = content.find_all('a')

        api_list = set()
        for item in raw_content:
            if item['href'].startswith('/en-US/docs/Web/API/'):
                api_list.add(item['href'].replace('/en-US/docs/Web/API/', '').strip())



    except Exception as e:
        print('Something went wrong: ' + str(e))
        return set()
    return api_list


def edit_api_class(api_class_dict):
    for api_name, class_list in api_class_dict.items():
        class_api = set()
        if len(class_list) == 0:
            options = Options()
            options.headless = True
            DRIVER_PATH = '/home/c6/Downloads/chromedriver'

            driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
            driver.set_script_timeout(10)
            if api_name == "storageQuota":
                print("stop")
            try:
                driver.get("https://developer.mozilla.org/en-US/search?q=" + api_name + "+")
                time.sleep(3)
                link_lists = driver.find_elements_by_partial_link_text('/en-US/docs/Web/API/')
                print(len(link_lists))
                for link in link_lists:
                    if link.text.split('/')[-2] == "API":
                        if SequenceMatcher(None, api_name, link.text.split('/')[-1]).ratio() > 0.50:
                            class_api.add(link.text.split('/')[-1])
                    if SequenceMatcher(None, api_name, link.text.split('/')[-1]).ratio() > 0.40 \
                            and SequenceMatcher(None, api_name, link.text.split('/')[-2]).ratio() > 0.40:
                        class_api.add(link.text.split('/')[-2])
                    if link.text.split('/')[-1].lower() == api_name.lower() + "_event":
                        class_api.add(link.text.split('/')[-2])
                    if link.text.split('/')[-1] == api_name or link.text.split('/')[-1] == api_name + "()":
                        class_api.add(link.text.split('/')[-2])
                driver.quit()
                if len(class_api) != 0:
                    api_class_dict[api_name] = list(class_api)
                    print(api_class_dict[api_name], api_name)
                else:
                    print("!!!!!!!!!!!!", api_name)
            except Exception as ex:
                time.sleep(4)
                print(ex)

        for cl in class_list:
            if cl == "API":
                class_list.remove("API")
                class_list.append(api_name)

    utilities.write_json("/home/c6/Desktop/OpenWPM/jsons/community_tracking/api_class.json", api_class_dict)


def address_on_api(api_class_dic):
    for api_name, class_list in api_class_dic.items():
        if api_name.startswith("on"):
            new_key = api_name[2:]
            if new_key in api_class_dic.keys():
                if len(api_class_dic[api_name]) != 0 & len(api_class_dic[new_key]) == 0:
                    api_class_dic[new_key] = api_class_dic[api_name]
                if len(api_class_dic[api_name]) == 0 & len(api_class_dic[new_key]) != 0:
                    api_class_dic[api_name] = api_class_dic[new_key]
    utilities.write_json("/home/c6/Desktop/OpenWPM/jsons/community_tracking/api_class.json", api_class_dic)


def address_similar_api(api_class_dic):
    api_list = [api_name for api_name, class_list in api_class_dic.items()]
    key_index = 0
    for api_name, class_list in api_class_dic.items():
        if SequenceMatcher(None, api_name, api_list[key_index+1]).ratio() > 0.80:
            a = api_list[key_index+1]
            if len(api_class_dic[api_name]) != 0 and len(api_class_dic[api_list[key_index+1]]) == 0:
                api_class_dic[api_list[key_index+1]] = api_class_dic[api_name]
            if len(api_class_dic[api_name]) == 0 and len(api_class_dic[api_list[key_index+1]]) != 0:
                api_class_dic[api_name] = api_class_dic[api_list[key_index+1]]
        key_index += 1
    utilities.write_json("/home/c6/Desktop/OpenWPM/jsons/community_tracking/api_class.json", api_class_dic)


def address_global_objects(drive_path, api_class_dict):

    page_load_timeout = 2
    file_write_timeout = 2

    options = Options()
    options.headless = True
    DRIVER_PATH = drive_path

    driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
    driver.set_page_load_timeout(page_load_timeout)

    try:
        url_of_glob_obj = "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference"
        req = urllib.request.Request(url_of_glob_obj, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req, timeout=10)
        content = BeautifulSoup(response.read(), 'html.parser')
        raw_content = content.find_all('code')

        ref_obj = set()
        for item in raw_content:
            ref_obj.add(item.getText().strip())

        for api_name, class_list in api_class_dict.items():
            if len(class_list) == 0:
                if api_name in ref_obj:
                    api_class_dict[api_name] = "Global_objects"
                    print(api_name)

        utilities.write_json("/home/c6/Desktop/OpenWPM/jsons/community_tracking/api_class.json", api_class_dict)

    except Exception as e:
        return set()


def check_empty_apis(api_class_dict):
    empty_list = []
    for api_name, class_lit in api_class_dict.items():
        if len(class_lit) == 0:
            empty_list.append(api_name)
    empty_list.sort()
    utilities.write_json("/home/c6/Desktop/OpenWPM/jsons/community_tracking/empty_api_class.json", empty_list)
    print(len(empty_list))


def main():
    DRIVE_PATH = '/home/c6/Downloads/chromedriver'
    api_class_dict = utilities.read_json("/home/c6/Desktop/OpenWPM/jsons/community_tracking/api_class.json")


    # assign class to cleaned_apis_unique
    """all_api_keys = utilities.read_file("/home/c6/Desktop/OpenWPM/myCodes/AST/jsons/cleaned_apis_unique.txt")
    api_list = []
    for api_i in all_api_keys:
        api_list.append(api_i.split('\n')[0])

    print("Total APIs: ", len(api_list))

    cpu_to_relax = 6
    pool = ThreadPool(processes=multiprocessing.cpu_count() - cpu_to_relax)
    results = pool.map(call_execute_class_multiproc, api_list)
    pool.close()
    pool.join()

    #utilities.write_json(os.path.join("/home/c6/Desktop/OpenWPM/jsons/community_tracking", "api_class.json"),
                         #dict(api_class))"""

    # Extract interface APIs
    #call_to_extract_interface()
    """api_list = []
    for api_name, class_list in api_class_dict.items():
        api_list.append(api_name)
    cpu_to_relax = 6
    pool = ThreadPool(processes=multiprocessing.cpu_count() - cpu_to_relax)
    results = pool.starmap(call_execute_class_multiproc, zip(api_list, api_class_dict))
    pool.close()
    pool.join()"""

    #edit_api_class(api_class_dict)
    #address_on_api(api_class_dict)
    #address_api_class(api_class_dict)

    #address_global_objects(DRIVE_PATH, api_class_dict)
    address_similar_api(api_class_dict)


if __name__ == '__main__':
    main()