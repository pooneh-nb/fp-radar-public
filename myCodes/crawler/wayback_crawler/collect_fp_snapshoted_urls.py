import pandas as pd
import json
import webbrowser
import tldextract as tld
import requests


def create_list_of_fp_urls_with_snapshot():
    fp_df = pd.read_pickle("/home/pooneh/Desktop/OpenWPM/jsons/dataframes/fp_df.pkl")
    temp_fp_df = fp_df[fp_df['is_backup'] != 'No_snapshot']

    print(len(temp_fp_df))

    with open("/home/pooneh/Desktop/OpenWPM/jsons/third_parties/all_3rdparty_fp_script_urls.json") as fp:
        fp_urls = json.load(fp)

    #print(fp_urls)
    list_of_fp_urls_with_snapshot = set()
    list_of_fp_urls_with_snapshot ={}
    idx = 0
    for url_id in temp_fp_df['url_id']:
        for hash_key, value in fp_urls.items():
            if value['url_id'] == int(url_id):
                list_of_fp_urls_with_snapshot[url_id] = value['script_url']
                #list_of_fp_urls_with_snapshot.add(value['script_url'])

    print(list_of_fp_urls_with_snapshot)

    with open("/home/pooneh/Desktop/OpenWPM/jsons/list_of_fp_urls_with_snapshot.json", 'w') as lis:
        json.dump(list_of_fp_urls_with_snapshot, lis, indent=4)


def create_change_url():
    with open("/home/pooneh/Desktop/OpenWPM/jsons/list_of_fp_urls_with_snapshot.json", 'rt') as lis:
        url_list = json.load(lis)
    wayback_url = []
    for url in url_list:
        wayback_url.append("https://web.archive.org/web/*/"+ url+"*")

    with open("/home/pooneh/Desktop/OpenWPM/jsons/wayback_change_url.json", 'w') as way:
        json.dump(wayback_url, way, indent=4)

def open_bowser():
    with open("/home/pooneh/Desktop/OpenWPM/jsons/wayback_change_url.json", 'rt') as lis:
        wayback_url = json.load(lis)
    print(len(wayback_url))
    for url in wayback_url[50:60]:
        webbrowser.open(url, new=2)

def test():
    with open("/home/pooneh/Desktop/OpenWPM/jsons/list_of_fp_urls_with_snapshot.json", 'rt') as lis:
        url_list = json.load(lis)

    for id_key, url in url_list.items():
        domain = tld.extract(url).fqdn
        #"/&matchType=prefix&filter=mimetype:application/javascript
        wayback_query = "http://web.archive.org/cdx/search/cdx?url=http://"+domain+\
                        "/&output=json&matchType=prefix&filter=mimetype:application/javascript&" \
                        "filter=mimetype:text/javascript&from=2010&to=2020"
        print(wayback_query)
        response = requests.get(wayback_query, verify=False)
        if response.status_code == 200:
            if len(response.content) != 0:
                response_json = response.json()
                if len(response_json) != 0:
                    print("has data")




#create_list_of_fp_urls_with_snapshot()
#create_change_url()
#open_bowser()
test()
