import urllib.parse as url
import json

with open("/home/pooneh/Desktop/OpenWPM/jsons/third_parties/non_fp_3rd_url_20k.json") as non:
    non_fp = json.load(non)

with open("/home/pooneh/Desktop/OpenWPM/jsons/third_parties/all_3rdparty_fp_script_urls.json") as fp:
    fp = json.load(fp)

encoded_non_fp_3rd_url_20k = {}
for hash_key, value in non_fp.items():
    try:
        print(value['url'])
        encoded_url = url.quote(value['url'])
        encoded_non_fp_3rd_url_20k[hash_key] = {"url": encoded_url, "url_id": value['url_id']}
    except Exception as ee:
        print(ee)

with open("/home/pooneh/Desktop/OpenWPM/jsons/third_parties/encoded_url/encoded_non_fp_3rd_url_20k.json", 'w') as non_fp:
    json.dump(encoded_non_fp_3rd_url_20k, non_fp, indent=4)


encoded_fp_3rd_url_20k = {}
for hash_key, value in fp.items():
    encoded_url = url.quote(value['script_url'])
    encoded_fp_3rd_url_20k[hash_key] = {"url": encoded_url, "url_id": value['url_id']}

with open("/home/pooneh/Desktop/OpenWPM/jsons/third_parties/encoded_url/encoded_fp_3rd_url_20k.json", 'w') as fp_u:
    json.dump(encoded_fp_3rd_url_20k, fp_u, indent=4)