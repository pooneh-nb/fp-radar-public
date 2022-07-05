from myCodes.AST import utilities
import os


def non_fp_mapping():
    # non_fp
    script_urls = utilities.read_json("/home/c6/Desktop/OpenWPM/jsons/third_parties/non_fp_3rd_url_20k.json")
    top_domains = utilities.read_json("/home/c6/Desktop/OpenWPM/jsons/third_parties/all_3rdparty_urls_20k.json")

    top_script = {}
    for _, value in script_urls.items():
        script_url = value["url"]
        for hash, top_value in top_domains.items():
            if script_url == top_value["script_url"]:
                top_script[value["url_id"]] = {"script_url": script_url, "top_domain": top_value["top_url"]}
                break
    utilities.write_json(os.path.join("/home/c6/Desktop/OpenWPM/jsons/third_parties/", "topDomain_map_script_URL,json"), top_script)
    print(len(top_script.keys()))
    print(len((script_urls.keys())))

    utilities.write_json(os.path.join("/home/c6/Desktop/OpenWPM/jsons/third_parties/", "topDomain_map_script_URL,json"), top_script)


def fp_mapping():
    # fp
    script_urls = utilities.read_json("/home/c6/Desktop/OpenWPM/jsons/third_parties/all_3rdparty_fp_script_urls.json")
    top_domains = utilities.read_json("/home/c6/Desktop/OpenWPM/jsons/third_parties/all_3rdparty_urls_20k.json")

    top_script = {}
    for _, value in script_urls.items():
        script_url = value["script_url"]
        for hash, top_value in top_domains.items():
            if script_url == top_value["script_url"]:
                top_script[value["url_id"]] = {"script_url": script_url, "top_domain": top_value["top_url"]}
                break
    utilities.write_json(os.path.join("/home/c6/Desktop/OpenWPM/jsons/third_parties/", "FP_topDomain_map_script_URL,json"), top_script)
    print(len(top_script.keys()))
    print(len((script_urls.keys())))


#fp_mapping()
non_fp_mapping()
