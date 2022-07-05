import json
import requests
from datetime import date, timedelta, datetime
import hashlib as hash
import os.path
import time
import urllib3
from myCodes.AST import utilities
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
err_logs = {'errors': []}


def availability_api(id_script_url, downloaded_file_dir):
    script_url = id_script_url.split('|')[-1]
    url_id = id_script_url.split('|')[0]
    noBackground = True
    start_date = date(2010, 1, 1)
    end_date = date(2020, 12, 1)
    delta = timedelta(days=30)
    print("Processing: " + script_url)
    while start_date <= end_date:
        hashed_list = []
        try:
            requested_time: str = start_date.strftime("%Y%m%d")
            response = requests.get(
                "http://archive.org/wayback/available?url=" + script_url + "&timestamp=" + requested_time, verify=False)
            if response.status_code == 400:
                break
            if not response.ok:
                print(str(requested_time) + " : " + str(response.status_code))
                time_to_sleep = int(response.headers["Retry-After"])
                if time_to_sleep:
                    time.sleep(int(response.headers["Retry-After"]))
                else:
                    time.sleep(10)
                utilities.append_file('/home/a/Documents/OpenWPM/jsons/error/non_fp_err_logs.json',
                                      script_url + str(response.status_code))
                continue
            if response.status_code == 200:
                if not response.raise_for_status():
                    response_json = response.json()
                    if response_json['archived_snapshots'] != {}:
                        closest_year = int(response_json['archived_snapshots']['closest']['timestamp'][0:4])
                        closest_month = int(response_json['archived_snapshots']['closest']['timestamp'][4:6])
                        closest_day = int(response_json['archived_snapshots']['closest']['timestamp'][6:8])
                        closest_date = response_json['archived_snapshots']['closest']['timestamp'][0:8]
                        requested_year = requested_time[0:4]
                        if requested_year < str(closest_year):
                            start_date = date(closest_year, closest_month, closest_day)
                            continue
                        if requested_time[0:6] == response_json['archived_snapshots']['closest']['timestamp'][0:6]:
                            snapshot = response_json['archived_snapshots']['closest']['url']
                            noBackground = False
                            js_content = requests.get(snapshot)
                            hash_script = hash.md5(js_content.text.encode()).hexdigest()
                            utilities.write_dill_compressed(
                                os.path.join(downloaded_file_dir,
                                             "yes|" + hash_script + "|" + closest_date + "|" + url_id), js_content.text)
                            print(script_url + " has a snapshot at " + closest_date)
                            start_date += delta
                        else:
                            start_date += delta
                    else:  # it should say that it doesn't have any background
                        break

        except Exception as inst:
            print("OOps: !", inst)
            utilities.append_file('/home/pooneh/Desktop/OpenWPM/jsons/error/non_fp_err_logs.json', script_url +
                                  ' Failed at ' + str(requested_time) + " error: " + str(inst))
            time.sleep(10)
            pass

    if noBackground:
        print(script_url + " doesn't have any background")
        utilities.write_dill_compressed(
            os.path.join(downloaded_file_dir, "no|" + url_id), "")
    print(script_url + " is done in: ")


def create_non_fp_queued_files(unprocessed_non_fp_script_url_list, js_write_directory):
    if not os.path.exists(js_write_directory):
        os.makedirs(js_write_directory)
    remaining_unprocessed_non_fp_script_url = []
    all_unprocessed_fp_script_url_list = unprocessed_non_fp_script_url_list  # dict hash: url, url_ID
    processed_fp_script_directory = utilities.get_files_in_a_directory(js_write_directory)
    processed_fp_script_url_list = []
    for a in processed_fp_script_directory:
        # b= a.split('/')[-1].split('|')[-1]
        # url = b.replace('_', "/")
        processed_fp_script_url_list.append(a.split('/')[-1].split('|')[-1])

    for unprocessed_key, unprocessed_value in all_unprocessed_fp_script_url_list.items():
        if str(unprocessed_value['url_id']) not in processed_fp_script_url_list:
            remaining_unprocessed_non_fp_script_url.append(
                str(unprocessed_value['url_id']) + "|" + unprocessed_value['url'])

    for urlANDid in remaining_unprocessed_non_fp_script_url:
        start = time.time()
        availability_api(urlANDid, js_write_directory)
        end = time.time()
        print(end - start)


def main():
    with open("/home/pooneh/Desktop/OpenWPM/jsons/third_parties/non_fp_3rd_url_20k.json") as p:
        unprocessed_non_fp_script_url_list = json.load(p)
    selected_dictionary = dict(list(unprocessed_non_fp_script_url_list.items())[1:8999])
    js_write_directory = "/home/pooneh/Desktop/OpenWPM/jsons/downloaded_files/non_fp_javascripts/1-8999"
    create_non_fp_queued_files(selected_dictionary, js_write_directory)


if __name__ == '__main__':
    main()
