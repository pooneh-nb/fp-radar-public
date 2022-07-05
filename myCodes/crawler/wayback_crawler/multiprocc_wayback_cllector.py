import json
import requests
from datetime import date, timedelta
import pandas as pd
import urllib as lib
import hashlib as hash
import os.path
import time
import urllib3
from multiprocessing import Pool

err_logs = {'errors': []}


# availability API, check the previous snapshots of a url
def availability_api(script_url):
    print(str(len(queued_non_fp_urls)) + " sites remains to be crawled ---")
    print(str(len(crawled_non_fp_urls)) + " sites has been crawled  +++")
    noBackground = True
    start_date = date(2010, 1, 1)
    end_date = date(2020, 12, 1)
    delta = timedelta(days=30)
    print("requested url: " + script_url)

    start = time.time()
    while start_date <= end_date:
        try:
            requested_time = start_date.strftime("%Y%m%d")
            start_date += delta
            response = requests.get(
                "http://archive.org/wayback/available?url=" + script_url + "&timestamp=" + requested_time, verify=False)
            # print("requested time" + requested_time)
            # time.sleep(2)

            # print(response.raise_for_status())
            if response.status_code == 200:
                response_json = response.json()
                if response_json['archived_snapshots'] != {}:
                    if requested_time[0:6] == response_json['archived_snapshots']['closest']['timestamp'][0:6]:
                        closest_date = response_json['archived_snapshots']['closest']['timestamp'][0:8]
                        url = response_json['archived_snapshots']['closest']['url'][42:]
                        noBackground = False
                        url_time = {"url": url,
                                    "requestedDate": requested_time,
                                    "closestDate": closest_date,
                                    "noBackup": noBackground}
                        wayback_url.append(url_time)
                        print(script_url + " has a snapshot at " + closest_date)

        except requests.exceptions.HTTPError as errh:
            print("Http Error:", errh)
            err_logs['errors'].append(
                {"script_url": script_url, "requested_time": requested_time, "error": "Http Error"})
            with open('/jsons/error/err_logs.json', 'w') as fp:
                json.dump(err_logs, fp, sort_keys=True, indent=4)
            pass
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
            err_logs['errors'].append(
                {"script_url": script_url, "requested_time": requested_time, "error": "Error Connecting"})
            with open('/jsons/error/err_logs.json', 'w') as fp:
                json.dump(err_logs, fp, sort_keys=True, indent=4)
            pass
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
            err_logs['errors'].append(
                {"script_url": script_url, "requested_time": requested_time, "error": "Timeout Error"})
            with open('/jsons/error/err_logs.json', 'w') as fp:
                json.dump(err_logs, fp, sort_keys=True, indent=4)
            pass
        except requests.exceptions.RequestException as errn:
            print("OOps: another request error", errn)
            err_logs['errors'].append(
                {"script_url": script_url, "requested_time": requested_time, "error": "another request error"})
            with open('/jsons/error/err_logs.json', 'w') as fp:
                json.dump(err_logs, fp, sort_keys=True, indent=4)
            pass
        except Exception as inst:
            print("OOps: unexpected!", inst)
            err_logs['errors'].append(
                {"script_url": script_url, "requested_time": requested_time, "error": "unexpected"})
            with open('/jsons/error/err_logs.json', 'w') as fp:
                json.dump(err_logs, fp, sort_keys=True, indent=4)
            time.sleep(15)
            pass

    if noBackground:
        url_time = {"url": script_url,
                    "noBackup": noBackground}
        wayback_url.append(url_time)

    with open('/home/pooneh/Desktop/OpenWPM/jsons/wayback_js_url_time.json', 'w') as pp:
        json.dump(wayback_url, pp, sort_keys=True, indent=4)

    # update crawled urls
    crawled_non_fp_urls.append(script_url)
    with open('/jsons/fp-non-fp/crawled_nonFP.json', 'w') as crr:
        json.dump(crawled_non_fp_urls, crr, sort_keys=True, indent=4)
    # updaye queued urls
    queued_non_fp_urls.remove(script_url)
    with open('/jsons/fp-non-fp/queued_nonFP.json', 'w') as qqq:
        json.dump(queued_non_fp_urls, qqq, sort_keys=True, indent=4)
    end = time.time()
    print(end - start)


with open("/home/pooneh/Desktop/OpenWPM/jsons/wayback_js_url_time.json", 'rt') as way:
    wayback_url = json.load(way)

# load queued urls
with open("/jsons/fp-non-fp/queued_nonFP.json", 'rt') as que:
    queued_non_fp_urls = json.load(que)

# load crawled urls
with open("/jsons/fp-non-fp/crawled_nonFP.json", 'rt') as ccc:
    crawled_non_fp_urls = json.load(ccc)

p = Pool(3)
p.map(availability_api, queued_non_fp_urls)
p.terminate()
p.join()
