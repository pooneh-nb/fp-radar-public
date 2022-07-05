#In this code we extract fp and non-fp urls from 20k file
import json

all_script_urls = []
#open the  20K file
with open("/jsons/third_parties/all_3rdparty_urls_20k.json", "rt") as twn:
    all_20k_url = json.load(twn)
with open("/jsons/third_parties/all_3rdparty_fp_script_urls.json", "rt") as fp:
    all_fp = json.load(fp)

fp_url_scripts = []
for hash, value in all_fp:
    if hash in all_20k_url.keys():
        fp_url_scripts.append(value['script_url'])
        del all_fp[hash]

#create list of urls in 20K file
for hash, value in all_20k_url.items():
    url = value['new_url_key']
    #hashi = url_hash[i]['content_hash']
    #all_script_urls[hashi] = url
    all_script_urls.append(url)

all_FP_script_uls = []
#open list of all FP urls
with open("/jsons/20k/all_fp_script_urls.json", "rt") as fp:
    fp_url_jsonobj = json.load(fp)
all_FP_script_uls = fp_url_jsonobj

print(len(all_script_urls))
# extract fp urls from 20k
fp_url_scripts = []
for fp_url in all_FP_script_uls:
    if fp_url in all_script_urls:
        fp_url_scripts.append(fp_url)
        all_script_urls.remove(fp_url)

non_fp_url_scripts = []
non_fp_url_scripts = list(filter(None, all_script_urls))

#write FP and non-FP scripts to a json file
with open('/jsons/fp-non-fp/fp_script_urls.json', 'w') as fp:
    json.dump(fp_url_scripts, fp, sort_keys=True, indent=4)
with open('/jsons/fp-non-fp/non_fp_script_urls.json', 'w') as p:
    json.dump(non_fp_url_scripts, p, sort_keys=True, indent=4)

print(len(fp_url_scripts))
print(len(non_fp_url_scripts))
