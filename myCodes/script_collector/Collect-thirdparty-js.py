#In this code we remove the duplicate script urls from fingerprinting_donains.json (collection of script_urls, resultof web crawling using fp-inspector)
#input: fingerprinting_domains.json
# outout : thirdparties.json
import json
import tldextract as tld
import os

# collect url+hash all **FP** third parties from fingerprinting_domains.json
# output: all_3rdparty_fp_script_urls.json
def collect_all_fp_thirdparties():
    # collect fp third parties
    with open("/jsons/fingerprinting_domains.json") as read_file:
        data = json.load(read_file)
    thirdparties = {}

    #hashes = set()
    #for key in data.keys():
        #hashes.add(key)

    for hash in data.keys():
        for ind in range(len(data[hash])):
            script_url_domain = tld.extract(data[hash][ind]['script_url']).domain
            top_url_domain = tld.extract(data[hash][ind]['top_url']).domain
            if script_url_domain != top_url_domain:
                script_url = data[hash][ind]['script_url']
                thirdparties[hash] = script_url
                pass
        #if len(listValue) != 0:
            #thirdparties[hash] = listValue
            #listValue = []

    print(str(len(thirdparties)) + " length of all fp urls")
    with open('/jsons/third_parties/all_3rdparty_fp_script_urls.json', 'w') as fp:
        json.dump(thirdparties, fp, sort_keys=True, indent=4)


def collect_all_fp_thirdparties_with_id():
    # collect fp third parties
    with open("/jsons/fingerprinting_domains.json") as read_file:
        data = json.load(read_file)
    thirdparties = {}

    url_id = 1
    for hash in data.keys():
        for ind in range(len(data[hash])):
            script_url_domain = tld.extract(data[hash][ind]['script_url']).domain
            top_url_domain = tld.extract(data[hash][ind]['top_url']).domain
            if script_url_domain != top_url_domain:
                script_url = data[hash][ind]['script_url']
                thirdparties[hash] = {'script_url': script_url, 'url_id': url_id}
                url_id += 1
                pass
        #if len(listValue) != 0:
            #thirdparties[hash] = listValue
            #listValue = []

    print(str(len(thirdparties)) + " length of all fp urls")
    with open('/jsons/third_parties/all_3rdparty_fp_script_urls.json', 'w') as fp:
        json.dump(thirdparties, fp, sort_keys=True, indent=4)

# collect all(fp/nonfp) third party url+hash from mapping_with_hash_20K.json
# output : all_3rdparty_urls_20k.json
def collect_all_thirdparties_20K():
    # collect all third parties from 20 k file
    # this process reduced the number of urls fro 419.801 to 92704
    with open("/jsons/20k/mapping_with_hash_20K.json") as f:
        all_url_20k = json.load(f)
    #print(len(all_url_20k))
    all_script_url_hash_20k = {}
    for key, value in all_url_20k.items():
        script_url_domain = tld.extract(value['new_url_key']).domain
        #top_url_domain = tld.extract(all_url_20k[key]['new_url_key']).domain
        top_url_domain = tld.extract(key.split('|', maxsplit=2)[-2]).domain
        if script_url_domain != top_url_domain:
            if value['content_hash'] != "":
                script_url = value['new_url_key']
                top_url = key.split('|', maxsplit=2)[-2]
                hashi = value['content_hash']
                all_script_url_hash_20k[hashi] = {'script_url': script_url, 'top_url': top_url}

    #print(str(len(all_script_url_hash_20k)), ": length of all  20k urls")

    with open("/jsons/third_parties/all_3rdparty_urls_20k.json", 'w') as th:
        json.dump(all_script_url_hash_20k, th, sort_keys=True, indent=4)

# length of all 3rdparty fp urls (from 100K) : 1663
# length of all 3rdparty urls(fp and nonfp) from 20k: 92.704
# length of 3rdparty fp(20): 495
# length of 3rdparty non-fp(20k): 92.209
def extract_all_fp_and_nonFP_thirdparties_url():
    fp_thirdparties_url_20k = {}
    non_fp_thirdparties_url_20k = {}
    with open("/jsons/third_parties/all_3rdparty_fp_script_urls.json", 'rt') as ur:
        all_fp = json.load(ur)
    with open("/jsons/third_parties/all_3rdparty_urls_20k.json", 'rt') as al:
        all_20 = json.load(al)
    print(str(len(all_fp)) + "length of all fp third party urls")
    print(str(len(all_20)) + "length of all third party urls")
    url_id = 1
    for hash_all_fp in all_fp.keys():
        if hash_all_fp in all_20.keys():
            fp_thirdparties_url_20k[hash_all_fp] = {'url_id': url_id, 'url': all_fp[hash_all_fp]}
            url_id += 1
            del all_20[hash_all_fp]

    url_id = 1
    for key, value in all_20.items():
        print(key, value)
        if key != "":
            non_fp_thirdparties_url_20k[key] = {'url_id': url_id, 'url': value['script_url']}
            url_id += 1

    with open("/jsons/third_parties/fp_3rd_url_20k.json", 'w') as rww:
        json.dump(fp_thirdparties_url_20k, rww, sort_keys=True, indent=4)

    with open("/jsons/third_parties/non_fp_3rd_url_20k.json", 'w') as rd:
        json.dump(non_fp_thirdparties_url_20k, rd, sort_keys=True, indent=4)

    print(str(len(non_fp_thirdparties_url_20k)) + ":length of non fp ")
    print(str(len(fp_thirdparties_url_20k)) + " length of fp")


#collect_all_fp_thirdparties()
#collect_all_thirdparties_20K()
#extract_all_fp_and_nonFP_thirdparties_url()
collect_all_fp_thirdparties_with_id()
# 92209:length of non fp
# 495 length of fp
