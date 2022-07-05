import json
import requests
import hashlib as hash
import os.path
import time
import urllib3
#from myCodes.AST import utilities
#import myCodes.AST.utilities as utilities
import utilities

import itertools
from multiprocessing import Pool as ThreadPool
import multiprocessing


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

existing_snapshot_dir = "/home/c6/Desktop/OpenWPM/jsons/CDX_api/dataframe/existing_fp_snapshots.json"

#def availability_api(url_id, downloaded_file_dir, existing_snapshot_dir, completed_file_dir):


def availability_api(url_id, downloaded_file_dir):
    start = time.time()

    existing_snapshot = utilities.read_json(existing_snapshot_dir)
    encoded_url = existing_snapshot[url_id]['encoded_url']
    snapshots = existing_snapshot[url_id]['snapshots']
    digests = existing_snapshot[url_id]['digest']

    idx = 0
    completeness = True
    for requested_time in snapshots:
        try:
            response = requests.get("http://web.archive.org/web/" + requested_time + "0000" + "/" + encoded_url)
            #response = requests.get(
                #"http://archive.org/wayback/available?url=" + encoded_url + "&timestamp=" + requested_time, verify=False)
            if response.status_code == 400:
                utilities.append_file('/home/c6/Desktop/OpenWPM/jsons/CDX_api/error/fp/wayback_crawl_err_logs.json',
                                      str(url_id) + "|" + str(requested_time) + "|" + str(response.status_code))
                completeness = False
                break
            if not response.ok:
                print(str(requested_time) + " : " + str(response.status_code))
                time_to_sleep = int(response.headers["Retry-After"])
                if time_to_sleep:
                    time.sleep(int(response.headers["Retry-After"]))
                else:
                    time.sleep(15)

                #completeness = False
                continue
            if response.status_code == 200:
                js_content = response.text
                if js_content != "":
                    #hash_script = hash.md5(js_content.text.encode()).hexdigest()
                    hash_script = digests[idx]
                    utilities.write_dill_compressed(
                        os.path.join(downloaded_file_dir, "yes|"+hash_script+"|"+requested_time+"|"+url_id), js_content)
                    #print(url_id + " has a snapshot at " + requested_time)
                    #if requested_time[0:6] != response_json['archived_snapshots']['closest']['timestamp'][0:6]:
                        #print(requested_time,  response_json['archived_snapshots']['closest']['timestamp'], url_id)
                else:
                    print(url_id, requested_time, " doesn't have snapshot")
                    utilities.append_file(
                        '/home/c6/Desktop/OpenWPM/jsons/CDX_api/error/fp/no_response_fp.json',
                        url_id + "|" + requested_time)
                    #completeness = False

        except Exception as inst:
            print("OOps: !", inst, url_id)
            utilities.append_file('/home/c6/Desktop/OpenWPM/jsons/CDX_api/error/fp/wayback_crawl_err_logs.json',
                                  str(url_id) + "|" + str(requested_time) + "|" +
                                  str(response.status_code) + "|" + str(inst))
            time.sleep(15)
            #completeness = False
            pass

        idx += 1
    #if completeness:
        #utilities.write_dill_compressed(os.path.join(completed_file_dir, url_id), "")
    end = time.time()
    print(str(url_id), " in ", str(round(end-start, 2)))


def create_queued_files(unprocessed_scripts, js_write_directory, completed_file_dir):
    if not os.path.exists(js_write_directory):
        os.makedirs(js_write_directory)

    remaining_unprocessed_script_url = set()
    all_unprocessed_script_url_list = unprocessed_scripts  # dict url_id: snapshots,origin, encoded_url, digest
    processed_script_directory = utilities.get_files_in_a_directory(js_write_directory)
    processed_script_url_list = []
    for file_name in processed_script_directory:
        #just url_i
        processed_script_url_list.append(file_name.split('/')[-1].split('|')[-1])

    print(len(all_unprocessed_script_url_list.keys()))

    # check processed files to ignored
    for unprocessed_key in all_unprocessed_script_url_list.keys():
        if unprocessed_key not in processed_script_url_list:
            remaining_unprocessed_script_url.add(unprocessed_key)

    leng = len(remaining_unprocessed_script_url)
    print(leng)
    cpu_to_relax = 10
    print(multiprocessing.cpu_count() )
    pool = ThreadPool(processes=multiprocessing.cpu_count() - cpu_to_relax)
    #pool = ThreadPool(processes=1)
    results = pool.starmap(availability_api, zip(remaining_unprocessed_script_url, itertools.repeat(js_write_directory)))
    pool.close()
    pool.join()

    """for url_id in remaining_unprocessed_script_url:
        print(leng)
        start = time.time()
        availability_api(url_id, js_write_directory)
        end = time.time()
        print(str(url_id) + " in " + str(round(end-start, 2)))
        leng -= 1"""


def no_response_double_ckeck(existing_snapshot_dir, downloaded_file_dir):
    existing_snapshot = utilities.read_json(existing_snapshot_dir)
    no_respose = open("/home/c6/Desktop/OpenWPM/jsons/CDX_api/error/no_response_non_fp.txt", "r")
    Lines = no_respose.readlines()
    for line in Lines:
        url_id = line.split('|')[0]
        encoded_url = existing_snapshot[url_id]['encoded_url']
        time_stamp = line.split('|')[-1].replace('\n',"")
        try:
            response = requests.get(
                "http://archive.org/wayback/available?url=" + encoded_url + "&timestamp=" + time_stamp, verify=False)
            response = requests.get("http://web.archive.org/web/"+ time_stamp+ "/" + encoded_url)
            if response.status_code == 400:
                utilities.append_file('/jsons/CDX_api/error/non_fp_c6/wayback_crawl_err_logs.json',
                                      url_id + str(response.status_code))
                break
            if not response.ok:
                print(str(time_stamp) + " : " + str(response.status_code))
                time_to_sleep = int(response.headers["Retry-After"])
                if time_to_sleep:
                    time.sleep(int(response.headers["Retry-After"]))
                else:
                    time.sleep(10)
                utilities.append_file('/jsons/CDX_api/error/non_fp_c6/wayback_crawl_err_logs.json',
                                      url_id + str(response.status_code))
                continue
            if response.status_code == 200:
                if not response.raise_for_status():
                    response_json = response.json()
                    if response_json['archived_snapshots'] != {}:
                        snapshot_add = response_json['archived_snapshots']['closest']['url']
                        js_content = requests.get(snapshot_add)
                        hash_script = hash.md5(js_content.text.encode()).hexdigest()
                        utilities.write_dill_compressed(
                            os.path.join(downloaded_file_dir, "yes|"+hash_script+"|"+time_stamp+"|"+url_id), js_content.text)
                        #print(url_id + " has a snapshot at " + requested_time)
                        if time_stamp[0:6] != response_json['archived_snapshots']['closest']['timestamp'][0:6]:
                            print(time_stamp,  response_json['archived_snapshots']['closest']['timestamp'], url_id)
                    else:
                        print(url_id, time_stamp, " doesn't have snapshot")
                        print(response_json)
                else:  # it should say that it doesn't have any background
                    break

        except Exception as inst:
            print("OOps: !", inst)
            utilities.append_file('/jsons/CDX_api/error/non_fp_c6/wayback_crawl_err_logs.json', url_id +
                                  ' Failed at ' + str(time_stamp) + " error: " + str(inst))
            time.sleep(15)
            pass


def main():
    """"
    path_to_non_fp_existing_snapshots = "/home/c6/Desktop/OpenWPM/jsons/CDX_api/dataframe/existing_non_fp_snapshots.json"
    with open(path_to_non_fp_existing_snapshots) as p:
        unprocessed_non_fp_scripts = json.load(p)
    selected_dictionary = dict(list(unprocessed_non_fp_scripts.items())[50000:])
    js_write_directory = "/home/c6/Desktop/OpenWPM/jsons/CDX_api/downloaded_files/non_fp_javascripts"
    completed_file_dir = "/home/c6/Desktop/OpenWPM/jsons/CDX_api/downloaded_files/completed_files"
    create_queued_files(selected_dictionary, js_write_directory, completed_file_dir)"""

    path_to_fp_existing_snapshots = "/home/c6/Desktop/OpenWPM/jsons/CDX_api/dataframe/existing_fp_snapshots.json"
    with open(path_to_fp_existing_snapshots) as p:
        unprocessed_fp_scripts = json.load(p)
    #selected_dictionary = dict(list(unprocessed_non_fp_scripts.items())[50000:])
    js_write_directory = "/home/c6/Desktop/OpenWPM/jsons/CDX_api/downloaded_files/fp_javascripts"
    completed_file_dir = "/home/c6/Desktop/OpenWPM/jsons/CDX_api/downloaded_files/completed_files"
    create_queued_files(unprocessed_fp_scripts, js_write_directory, completed_file_dir)

    #js_write_directory = "/home/c6/Desktop/OpenWPM/jsons/CDX_api/downloaded_files/non_fp_javascripts"
    #existing_snapshots = "/home/c6/Desktop/OpenWPM/jsons/CDX_api/dataframe/existing_non_fp_snapshots.json"
    #no_response_double_ckeck(existing_snapshots, js_write_directory)


if __name__ == '__main__':
    main()
