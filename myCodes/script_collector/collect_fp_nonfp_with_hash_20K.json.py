#In this code we extract fp and non-fp urls from 20k file with their hash
import json

all_url_hash_20k = {}
all_fp_url_hash_100k = {}

fp_url_hash = {}
non_fp_url_hash = {}

# all_script_urls = []
# open the  20K file


def make_all_url_hash_20k():
    with open("/jsons/20k/mapping_with_hash_20K.json", "rt") as twn:
        url_hash = json.load(twn)
    # create list of urls in 20K file with hash
    for key, value in url_hash.items():
        if url_hash[key]['content_hash'] != "":
            url = url_hash[key]['new_url_key']
            hash = url_hash[key]['content_hash']
            all_url_hash_20k[hash] = url

    with open('/jsons/with_hash/all_url_hash_20k.json', 'w') as aa:
        json.dump(all_url_hash_20k, aa, sort_keys=True, indent=4)


def make_all_fp_url_hash_100k():
    with open("/jsons/fingerprinting_domains.json", "rt") as f:
        all_fp_100k = json.load(f)
    for key, value in all_fp_100k.items():
        url = all_fp_100k[key][0]['script_url']
        hashi = key
        all_fp_url_hash_100k[hashi] = url
    with open('/jsons/with_hash/all_fp_url_hash_100k.json', 'w') as aa:
        json.dump(all_fp_url_hash_100k, aa, sort_keys=True, indent=4)


def make_fp_non_fp_url_hash():
    with open("/jsons/with_hash/all_fp_url_hash_100k.json", "rt") as au:
        all_fp = json.load(au)

    with open('/jsons/with_hash/all_url_hash_20k.json', 'rt') as fu:
        all_url = json.load(fu)

    for fp_url_key, value in all_fp.items():
        if fp_url_key in all_url.keys():
            fp_url_hash[fp_url_key] = value
            # print(len(all_url))
            del all_url[fp_url_key]
            # print(len(all_url))

    with open('/jsons/with_hash/fp_url_hash.json', 'w') as ffp:
        json.dump(fp_url_hash, ffp, sort_keys=True, indent=4)

    with open('/jsons/with_hash/non_fp_url_hash.json', 'w') as nfp:
        json.dump(all_url, nfp, sort_keys=True, indent=4)


    # non_fp_url_scripts = []
    # non_fp_url_scripts = list(filter(None, all_script_urls))
""" open list of all fp url-hash file
with open("home/pooneh/Desktop/OpenWPM/jsons/jsons/20k/all_fp_script_urls.json", "rt") as f:
    all_fp = json.load(f)

# create a list of all fp urls with hash
all_FP_script_uls = {}
for key, value in all_fp:
    url = all_fp[key]['new_url_key']
    hashk = key
    all_FP_script_uls [hashk] = url
make_all_url_hash_20k():
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
with open('/jsons/fp-non-fp/nfp_script_urls.json', 'w') as fp:
    json.dump(fp_url_scripts, fp, sort_keys=True, indent=4)
with open('/jsons/fp-non-fp/non_fp_script_urls.json', 'w') as p:
    json.dump(non_fp_url_scripts, p, sort_keys=True, indent=4)

print(len(fp_url_scripts))
print(len(non_fp_url_scripts))"""

#make_all_url_hash_20k()
#make_all_fp_url_hash_100k()
#make_fp_non_fp_url_hash()

with open('/jsons/with_hash/all_fp_url_hash_100k.json', 'rt') as aa:
    a = json.load(aa)

with open('/jsons/with_hash/all_url_hash_20k.json', 'rt') as bb:
    b = json.load(bb)
    
with open('/jsons/with_hash/fp_url_hash.json', 'rt') as cc:
    c = json.load(cc)
        
with open('/jsons/with_hash/non_fp_url_hash.json', 'rt') as dd:
    d = json.load(dd)
    
print(len(a))
print(len(b))
print(len(c))
print(len(d))
