import json
import requests
from datetime import date, timedelta
import pandas as pd
import urllib as lib
import hashlib as hash
import os.path
import time
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# empty dataframe- log of script urls in 10yrs
history_df = pd.DataFrame(columns=['requestedDate', 'closestDate', 'URL'])


err_logs = {'errors': []}


# availability API, check the previous snapshots of a url
def availability_api():
    with open("/home/pooneh/Desktop/OpenWPM/jsons/wayback_js_url_time.json", 'rt') as way:
        wayback_url = json.load(way)
    #wayback_url = []
    # load queued urls
    with open("/jsons/fp-non-fp/queued_nonFP.json", 'rt') as que:
        queued_non_fp_urls = json.load(que)

    # load crawled urls
    with open("/jsons/fp-non-fp/crawled_nonFP.json", 'rt') as ccc:
        crawled_non_fp_urls = json.load(ccc)

    for script_url in queued_non_fp_urls:
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
                #print("requested time" + requested_time)
                #time.sleep(2)
                # response.ok returns True if status.code is less than 400, False if not
                if not response.ok:
                    print(str(requested_time) + " : " + str(response.status_code))
                    print(response.headers["Retry-After"])
                    time.sleep(int(response.headers["Retry-After"]))
                #print(response.raise_for_status())
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
                err_logs['errors'].append({"script_url": script_url, "requested_time": requested_time, "error": "unexpected"})
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
        # update queued urls
        queued_non_fp_urls.remove(script_url)
        with open('/jsons/fp-non-fp/queued_nonFP.json', 'w') as qqq:
            json.dump(queued_non_fp_urls, qqq, sort_keys=True, indent=4)
        end = time.time()
        print(end - start)


# API detecting url change
def url_archive(script_url):
    times = {'2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020'}
    for time in times:
        response = requests.get(
            "https://web.archive.org/web/2019*/" + script_url + "*")
        print(response)


def js_content_download():
    with open("/home/pooneh/Desktop/OpenWPM/jsons/wayback_js_url_time.json", "rt") as wb:
        historical_url_list = json.load(wb)

    with open("/home/pooneh/Desktop/OpenWPM/jsons/wayback_hashed_url.json", "rt") as h:
        hashed_wb = json.load(h)
    #hashed_wb = {}

    try:
        for diction in historical_url_list:
            if not diction['noBackup']:
                script_url = diction['url']
                requested_time = diction['requestedDate']
                closest_date = diction['closestDate']

                response = requests.get(script_url, allow_redirects=True, verify=False)
                if response.status_code == 200:
                    hash_script = hash.md5(response.content).hexdigest()
                    if hash_script not in hashed_wb.keys():
                        path = os.path.join("/home/pooneh/Desktop/OpenWPM/non_fp_javascript_files", hash_script)
                        open(path, 'wb').write(response.content)
                        hashed_wb[hash_script] = {"requestedDate": requested_time,
                                                  "closestDate": closest_date,
                                                  "url": script_url}
                        with open("/home/pooneh/Desktop/OpenWPM/jsons/wayback_hashed_url.json", "w") as fp:
                            json.dump(hashed_wb, fp, sort_keys=True, indent=4)

    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
        err_logs['errors'].append(
            {"script_url": script_url, "requested_time": requested_time, "error": "Http Error"})
        with open('/jsons/error/js_download_errs.json', 'w') as fp:
            json.dump(err_logs, fp, sort_keys=True, indent=4)
        pass
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
        err_logs['errors'].append(
            {"script_url": script_url, "requested_time": requested_time, "error": "Error Connecting"})
        with open('/jsons/error/js_download_errs.json', 'w') as fp:
            json.dump(err_logs, fp, sort_keys=True, indent=4)
        pass
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
        err_logs['errors'].append(
            {"script_url": script_url, "requested_time": requested_time, "error": "Timeout Error"})
        with open('/jsons/error/js_download_errs.json', 'w') as fp:
            json.dump(err_logs, fp, sort_keys=True, indent=4)
        pass
    except requests.exceptions.RequestException as errn:
        print("OOps: another request error", errn)
        err_logs['errors'].append(
            {"script_url": script_url, "requested_time": requested_time, "error": "another request error"})
        with open('/jsons/error/js_download_errs.json', 'w') as fp:
            json.dump(err_logs, fp, sort_keys=True, indent=4)
        pass
    except Exception as aa:
        print("OOps: unexpected!", aa)
        err_logs['errors'].append({"script_url": script_url, "requested_time": requested_time, "error": "unexpected"})
        with open('/jsons/error/js_download_errs.json', 'w') as fp:
            json.dump(err_logs, fp, sort_keys=True, indent=4)
        time.sleep(15)
        pass


def wayback_changes_api():
    script_url = "https://web.archive.org/web/changes/https://www.kelete.com/statics/js/common.js"
    response = requests.get("https://web.archive.org/web/changes/" + script_url)
    print(response.content)


def test():
    with open("/home/pooneh/Desktop/OpenWPM/jsons/wayback_js_ds.json", "rt") as wb:
        historical_url_list = json.load(wb)

    with open("/home/pooneh/Desktop/OpenWPM/jsons/wayback_hashed_url.json", "rt") as h:
        hashed_wb = json.load(h)

    for diction in historical_url_list:
        script_url = diction['url']
        requested_time = diction['requestedDate']
        closestDate = diction['closestDate']

        response = requests.get(script_url, allow_redirects=True, verify=False)
        if response.status_code == 200:
            hash_script = hash.md5(response.content).hexdigest()
            if hash_script not in hashed_wb.keys():
                path = os.path.join("/home/pooneh/Desktop/OpenWPM/javascript_files", hash_script + ".js")
                open(path, 'wb').write(response.content)
                hashed_wb[hash_script] = {"requestedDate": requested_time,
                                            "closestDate": closestDate,
                                            "url": script_url}
                with open("/home/pooneh/Desktop/OpenWPM/jsons/wayback_hashed_url.json", "w") as fp:
                    json.dump(hashed_wb, fp, sort_keys=True, indent=4)


def create_non_fp_queued_files():
    if not os.path.exists("/jsons/fp-non-fp/queued_nonFP.json"):
        queued = []
        with open("/jsons/fp-non-fp/non_fp_script_urls.json", "rt") as q:
            queued = json.load(q)

        with open("/jsons/fp-non-fp/queued_nonFP.json", "w") as n:
            json.dump(queued, n, sort_keys=True, indent=4)

    with open("/jsons/fp-non-fp/queued_nonFP.json", "rt") as c:
        queued = json.load(c)
    print(len(queued))



        #with open("/home/pooneh/Desktop/OpenWPM/jsons/crawled.json", "w") as qq:
            #json.dump(queued, qq, indent=4)


#create_non_fp_queued_files()
#availability_api()
js_content_download()
# wayback_changes_api()
#test()
