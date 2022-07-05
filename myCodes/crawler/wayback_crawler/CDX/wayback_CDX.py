import os.path
import shutil
import time
import requests
import os
from multiprocessing import Pool as ThreadPool
import multiprocessing
import itertools
from myCodes.AST import utilities
#import myCodes.AST.utilities as utilities
#import utilities
import pandas as pd
import csv


# input: url_id and url in encoded format. and the path to download json files
# output: for each url, if CDX API has any snapshot, it will return a json file in response
def call_cdx_api(id_script_url, base_cdx_availability_dir):

    cdx_avail_jsons = os.path.join(base_cdx_availability_dir, "cdx_jsons")
    cdx_avail_no = os.path.join(base_cdx_availability_dir, "cdx_jsons/no")
    cdx_avail_error= os.path.join(base_cdx_availability_dir, "error/error_logs.json")
    cdx_avail_error_robot = os.path.join(base_cdx_availability_dir, "error/robots_error.json")
    cdx_avail_error_429 = os.path.join(base_cdx_availability_dir, "error/429.json")

    if not os.path.exists(cdx_avail_error_robot):
        os.makedirs(cdx_avail_error_robot)
    if not os.path.exists(cdx_avail_error_429):
        os.makedirs(cdx_avail_error_429)
    if not os.path.exists(cdx_avail_no):
        os.makedirs(cdx_avail_no)

    script_url = id_script_url.split('|')[-1]
    url_id = id_script_url.split('|')[0]
    #print("Processing: " + script_url+ ":" + url_id + "\n")

    downloaded_files = len(utilities.get_files_in_a_directory(cdx_avail_jsons))
    remaining = 100000 - downloaded_files
    if remaining % 1000 == 0:
        print("Remaining: ", remaining)

    output = "&output=json"
    field_order = "&fl=original,timestamp,mimetype,statuscode,digest"
    date = "&from=2010&to=2021"
    show_dupl = "&showDupeCount=true"
    filter = "&filter=statuscode:200"
    collapse = "&collapse=timestamp:4&collapse=digest"

    try:
        request = "http://web.archive.org/cdx/search/cdx?url=" + script_url + output + field_order + date + filter + collapse
        response = requests.get(request, verify=False)
        if response.status_code == 400:
            utilities.append_file(cdx_avail_error, url_id + "|" + str(response.status_code))
        if not response.ok:
            if response.status_code == 403:
                print(str(url_id) + " : " + str(response.status_code))
                utilities.append_file(cdx_avail_error_robot, url_id + "|" + str(response.status_code))
            if response.status_code == 429:
                utilities.append_file(cdx_avail_error_429, url_id + "|" + str(response.status_code))
                os.remove(os.path.join(cdx_avail_jsons, "no", "no|" + url_id + ".json"))
                time.sleep(10)
        if response.status_code == 200:
            if not response.raise_for_status():
                response_json = response.json()
                if len(response_json) != 0:
                    utilities.write_json(os.path.join(cdx_avail_jsons, "yes|" + url_id) + ".json"
                                         , response_json)
                    os.remove(os.path.join(cdx_avail_jsons, "no", "no|"+url_id+".json"))
                    return True
                else:
                    utilities.write_json(os.path.join(cdx_avail_jsons, "no", "no|" + url_id) + ".json",
                                         response_json)

            # it should say that it doesn't have any background
            else:
                print("no backup")
    except Exception as inst:
        print("OOps: !", inst)
        utilities.append_file(cdx_avail_error, url_id + "|" + str(inst))
        print(inst)
        time.sleep(15)
        pass

    # if noBackground:
    # print(script_url + " doesn't have any background")
    # utilities.write_dill_compressed(
    # os.path.join(downloaded_file_dir, "no|" + url_id), "")


def create_url_queue(unprocessed_url_list, base_cdx_availability_dir):
    cdx_avail_jsons = os.path.join(base_cdx_availability_dir, "cdx_jsons")
    if not os.path.exists(cdx_avail_jsons):
        os.makedirs(cdx_avail_jsons)

    remaining_unprocessed_urls = []
    all_unprocessed_url_list = unprocessed_url_list  # dict hash: url, url_ID
    processed_urls = utilities.get_files_in_a_directory(cdx_avail_jsons)
    processed_url_list = []
    for url in processed_urls:
        processed_url_list.append(url.split('|')[-1].split('.')[0])  # this i just a url_id

    for unprocessed_key, unprocessed_value in all_unprocessed_url_list.items():
        if unprocessed_key not in processed_url_list:
            remaining_unprocessed_urls.append(
                unprocessed_key + "|" + unprocessed_value)

    """for url in remaining_unprocessed_urls:
        call_cdx_api(url, base_cdx_availability_dir)"""

    cpu_to_relax = 3
    pool = ThreadPool(processes=4)
    results = pool.starmap(call_cdx_api,
                           zip(remaining_unprocessed_urls, itertools.repeat(base_cdx_availability_dir)))
    pool.close()
    pool.join()

    # for urlANDid in remaining_unprocessed_non_fp_script_url:
    # call_cdx_api(urlANDid, json_write_directory)


def create_retried_url_queue(base_cdx_availability_dir, top_urls):
    cdx_avail_error = os.path.join(base_cdx_availability_dir, "error/429.json")
    cdx_error_file = utilities.read_file_newline_stripped(cdx_avail_error)
    retied_error_urls = []
    for record in cdx_error_file:
        url_id = str(record.split('|')[0])
        url = top_urls[url_id]
        retied_error_urls.append(url_id+"|"+url)

    pool = ThreadPool(processes=4)
    results = pool.starmap(call_cdx_api,
                           zip(retied_error_urls, itertools.repeat(base_cdx_availability_dir)))
    pool.close()
    pool.join()


def create_no_script_url_queue(base_cdx_availability_dir, top_urls):
    cdx_non_avail_jsons = utilities.get_files_in_a_directory(os.path.join(base_cdx_availability_dir, "cdx_jsons/no"))
    non_processes_urls = []
    for record in cdx_non_avail_jsons:
        url_id = record.split('/')[-1].split('|')[-1].split('.')[0]
        url = top_urls[url_id]
        non_processes_urls.append(url_id+"|"+url)

    pool = ThreadPool(processes=4)
    results = pool.starmap(call_cdx_api,
                           zip(non_processes_urls, itertools.repeat(base_cdx_availability_dir)))
    pool.close()
    pool.join()


def create_url_id_dict(top_urls_csv, outdir):
    id_url_dict = {}
    with open(top_urls_csv) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            id_url_dict[row[0]] = row[1]
    utilities.write_json(os.path.join(outdir, "top_urls.json"), id_url_dict)


def create_missed_urls(base_cdx_availability_dir, top_urls):
    yes_files = utilities.get_files_in_a_directory(os.path.join(base_cdx_availability_dir, "cdx_jsons"))
    no_files = utilities.get_files_in_a_directory(os.path.join(base_cdx_availability_dir, "cdx_jsons/no"))
    robot_error = utilities.read_file_newline_stripped(os.path.join(base_cdx_availability_dir, "error/robots_error.json"))
    yes_url_ids = [yes.split('/')[-1].split('|')[-1].split('.')[0] for yes in yes_files]
    no_url_ids = [no.split('/')[-1].split('|')[-1].split('.')[0] for no in no_files]
    robot_url_ids = [robot.split('|')[0] for robot in robot_error]

    unprocessed_urls = []
    for url_id, url in top_urls.items():
        if url_id not in yes_url_ids:
            if url_id not in no_url_ids:
                if url_id not in robot_url_ids:
                    unprocessed_urls.append(url_id + "|" + url)

    pool = ThreadPool(processes=4)
    results = pool.starmap(call_cdx_api,
                           zip(unprocessed_urls, itertools.repeat(base_cdx_availability_dir)))
    pool.close()
    pool.join()


def main():
    # assign top-1million urls an Id
    """out_dir = "/home/c6/Desktop/OpenWPM/jsons/top_million_urls"
    top_urls_csv = os.path.join(out_dir, "top-1m.csv")
    create_url_id_dict(top_urls_csv, out_dir)"""

    base_cdx_availability_dir = "/home/c6/Desktop/OpenWPM/jsons/top_million_urls/Wayback/CDX_API"

    if not os.path.exists(base_cdx_availability_dir):
        os.makedirs(base_cdx_availability_dir)
    # call wayback to check top urls availability
    top_urls = dict(
        list(utilities.read_json("/home/c6/Desktop/OpenWPM/jsons/top_million_urls/top_urls.json").items())[0:100000])
    """top_urls = dict(
        list(utilities.read_json("/home/c6/Desktop/OpenWPM/jsons/top_million_urls/top_urls.json").items())[0:100000])
    
    create_url_queue(top_urls, base_cdx_availability_dir)"""

    # Call back again urls with 'retry error' or 429
    """cdx_avail_error_429 = os.path.join(base_cdx_availability_dir, "error/429.json")
    cdx_avail_error_helper = os.path.join(base_cdx_availability_dir, "error/429_2.json")
    print(len(utilities.read_file_newline_stripped(cdx_avail_error_429)))
    while len(utilities.read_file_newline_stripped(cdx_avail_error_429)) != 0:
        shutil.copy(cdx_avail_error_429, cdx_avail_error_helper)
        utilities.write_content(cdx_avail_error_429, "")
        create_retried_url_queue(base_cdx_availability_dir, top_urls)"""

    # Call back urls with no response
    # create_no_script_url_queue(base_cdx_availability_dir, top_urls)

    # Call missed urls
    #create_missed_urls(base_cdx_availability_dir, top_urls)

    """ Sanity checking
    Yes urls: 92065
    No urls: 7575
    403: 360
    sum: 100.000
    yes_files = utilities.get_files_in_a_directory(os.path.join(base_cdx_availability_dir, "cdx_jsons"))
    no_files = utilities.get_files_in_a_directory(os.path.join(base_cdx_availability_dir, "cdx_jsons/no"))
    robot_error = utilities.read_file_newline_stripped(
        os.path.join(base_cdx_availability_dir, "error/robots_error.json"))

    yes_url_ids = [yes.split('/')[-1].split('|')[-1].split('.')[0] for yes in yes_files]
    no_url_ids = [no.split('/')[-1].split('|')[-1].split('.')[0] for no in no_files]
    robot_url_ids = [robot.split('|')[0] for robot in robot_error]

    for url_id in no_url_ids:
        if url_id in robot_url_ids:
            print(url_id)
            os.remove(os.path.join(base_cdx_availability_dir, "cdx_jsons", "no", "no|" + url_id + ".json"))"""

if __name__ == '__main__':
    main()
