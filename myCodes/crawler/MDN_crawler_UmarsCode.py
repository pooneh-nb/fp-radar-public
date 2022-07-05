from bs4 import BeautifulSoup
import urllib.request
import urllib
import sys
import time
import os
from os import listdir
from os.path import isfile, join
import re


def append_file(file_addr, content):
    with open(file_addr, 'a') as myfile:
        for line in content:
            myfile.write(line + '\n')


def write_file(file_addr, content):
    with open(file_addr, 'w') as myfile:
        for line in content:
            myfile.write(line + '\n')


def read_file(file_path):
    with open(file_path) as f:
        content = f.readlines()
    return content


def get_simple_files(file_path):
    only_files = [f for f in listdir(file_path) if isfile(join(file_path, f))]
    only_files = [os.path.join(file_path, f) for f in only_files]
    return only_files


def extract_apis_from_main_page():
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

        api_list = process_api_list(api_list)

    except Exception as e:
        print('Something went wrong: ' + str(e))
        return set()
    return api_list


def extract_requests(api_name):
    try:
        url = 'https://developer.mozilla.org/en-US/docs/Web/API/' + api_name
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req, timeout=10)
        content = BeautifulSoup(response.read(), 'html.parser')
        raw_content = content.find_all('code')

        api_list = set()
        for item in raw_content:
            api_list.add(item.getText().strip())

        api_list = process_api_list(api_list)

    except Exception as e:
        print('Something went wrong: ' + api_name + ' - ' + str(e))
        return set()
    return api_list


def process_api_list(api_list):
    identifiers = set()

    for api in api_list:
        api = re.sub('\\(.*?\\)', '', api)

        api = api.split('.')
        for item in api:
            if not item.strip().isdigit():
                identifiers.add(item.strip())

    return identifiers


def clean_processed_items(post_processing, api_addr_unique):
    all_items = read_file(api_addr_unique)

    cleaned = set()
    characters = ['\"', '\'', ';', ':', '<', '>', '/', '*', '=', '{', ',', ' ', '-', '@', '[', ']', '}', '(', ')', '!',
                  '%', '#', '+', '−']

    for item in all_items:
        if any(x in item.strip() for x in characters):
            continue
        elif len(item.strip()) == 1:
            continue
        else:
            cleaned.add(item.strip())

    write_file(post_processing, cleaned)

    return


def crawl_apis(api_addr, api_addr_unique):
    api_list = extract_apis_from_main_page()
    # write down all api classes from mdn
    append_file(api_addr, api_list)
    all_unique_apis = api_list.copy()

    for api in api_list:
        print('processing API: ' + api.strip())
        api_temp_list = set()
        api_temp_list = extract_requests(api.strip())
        all_unique_apis |= api_temp_list
        append_file(api_addr, api_temp_list)
        time.sleep(1)
        # break

    append_file(api_addr_unique, all_unique_apis)


#base_addr = '/Users/uiqbal/Documents/work/data/js_apis/'

# base directory to safe files
base_addr = '/home/c6/Desktop/OpenWPM/jsons/js_apis/'

# list of all apis in main page of MDN
api_addr = base_addr + 'all_apis_duplicates.txt'

api_addr_unique = base_addr + 'all_apis_unique.txt'
post_processing = base_addr + 'cleaned_apis_unique.txt'
crawl_apis(api_addr, api_addr_unique)
clean_processed_items(post_processing, api_addr_unique)