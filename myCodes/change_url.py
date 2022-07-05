import json
import requests

with open("/jsons/script_urls.json", "rt") as f:
    json_obj = json.load(f)

url_list = set()
for url in json_obj:
    url_list.add(url)
years = {'2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020'}
def investigate_url_change():
    for script_url in url_list:
        for year in years:
            response = requests.get("https://web.archive.org/web/" +year+ "*/" +script_url+ "*")
            if response.status_code == 200:
                print(response.text)
                print(year)


investigate_url_change()

