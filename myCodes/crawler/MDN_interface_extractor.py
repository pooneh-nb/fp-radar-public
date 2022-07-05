import urllib.request
from bs4 import BeautifulSoup
from myCodes.AST import utilities
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import re


def collect_interface_list():
    api_class = []
    page_load_timeout = 2
    file_write_timeout = 2

    options = Options()
    options.headless = True
    DRIVER_PATH = '/home/c6/Downloads/chromedriver'

    driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
    driver.set_page_load_timeout(page_load_timeout)

    try:
        url = 'https://developer.mozilla.org/en-US/docs/Web/API/'
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req, timeout=10)
        content = BeautifulSoup(response.read(), 'html.parser')
        raw_content = content.find_all('a')

        api_list = set()
        for item in raw_content:
            if item['href'].startswith('/en-US/docs/Web/API/'):
                api_list.add(item['href'].replace('/en-US/docs/Web/API/', '').strip())

    except Exception as e:
        print('Something went wrong: ' + str(e))
        return set()
    return api_list


def assign_interface_keyword(interface, interfaces_keys):
    try:
        url = 'https://developer.mozilla.org/en-US/docs/Web/API/' + interface
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req, timeout=10)
        content = BeautifulSoup(response.read(), 'html.parser')

        raw_content_href = content.find_all(href=True)
        raw_content_code = content.find_all('code')

        interface_set = set()
        black_list = set()
        # process raw_content_href
        for href in raw_content_href:
            # links have href attribute
            if href['href'].startswith('/en-US/docs/Web/API/'):
                if href['href'].startswith('/en-US/docs/Web/API/' + interface):
                    keyw = href['href'].replace('/en-US/docs/Web/API/', '').strip()
                    if keyw.endswith(".txt"):
                        continue
                        # interface.property
                    if href.getText().strip().startswith(interface + "."):
                        keyw = href.getText().strip().split('.')[-1].split('()')[0]
                        if keyw not in interfaces_keys:
                            interface_set.add(keyw)
                        continue
                    ac = href['href'].split('/')[-1]
                    if '#' in href['href'].split('/')[-1]:
                        keyw = href.getText().strip().split('.')[-1].split('()')[0]
                        if keyw not in interfaces_keys:
                            interface_set.add(keyw)
                            continue
                    else:
                        keyw = href.getText().strip().split('()')[0]
                        if keyw in interfaces_keys:
                            continue
                        interface_set.add(keyw)
                        continue
                else:
                    keyw = href['href'].replace('/en-US/docs/Web/API/', '').strip().split('/')[-1].split('#')[-1]
                    keyText = href.getText().strip().split('/')[-1].split('#')[-1]
                    if href['href'].replace('/en-US/docs/Web/API/', '').strip().split('/')[-1].split('#')[
                        0] != interface:
                        black_list.add(keyw)
                        black_list.add(keyText)
                        continue
                    interface_set.add(keyw)
                    continue
            else:
                if '#' in href['href']:
                    if '()' in href.getText():
                        keyw = href.getText().split('()')[0]
                        interface_set.add(keyw)
        # process raw_content_code
        for code in raw_content_code:
            keyw = code.getText().replace('"', '').split('.')[-1].split('()')[-1]
            if ' ' not in keyw:
                if keyw not in interfaces_keys:
                    if keyw not in black_list:
                        interface_set.add(keyw)
                        continue

    except Exception as e:
        print('Something went wrong: ' + interface + ' - ' + str(e))
        pass
    return interface_set


def clean_processed_items():
    base_dir = "/home/c6/Desktop/OpenWPM/jsons/community_tracking/real_graphs" \
               "/DY_COMM/labeling_clusters"
    interface_dic = utilities.read_json(base_dir + "/interface_dict3.json")
    characters = [';', '-', ':', '<', '>', '*', '=', '{', ',', ' ', '@', '[', ']', '}', '(', ')', '!',
                  '%', '#', '+']

    for clss, member in interface_dic.items():
        for item in member:
            if any(char in item for char in characters):
                interface_dic[clss].remove(item)
            if item == "":
                interface_dic[clss].remove(item)
            if item.isdecimal():
                interface_dic[clss].remove(item)

    utilities.write_json(base_dir + "/interface_dict4.json", interface_dic)


def setify_interface_dict(base_addr):
    interface_dict = utilities.read_json(os.path.join(base_addr, 'interface_dict.json'))
    for interface, member_list in interface_dict.items():
        interface_dict[interface] = list(set(member_list))
    utilities.write_json(os.path.join(base_addr, "interface_dict5.json"), interface_dict)


def collect_APIs(interface_list):
    interface_list = utilities.read_json(interface_list)
    page_load_timeout = 2

    options = Options()
    options.headless = True
    DRIVER_PATH = '/home/c6/Downloads/chromedriver'

    driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
    driver.set_page_load_timeout(page_load_timeout)

    try:
        url = 'https://developer.mozilla.org/en-US/docs/Web/API/'
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req, timeout=10)
        content = BeautifulSoup(response.read(), 'html.parser')
        raw_content = content.find_all('a')

        api_list = set()
        for item in raw_content:
            if item['href'].startswith('/en-US/docs/Web/API/'):
                potential_link = item['href'].replace('/en-US/docs/Web/API/', '').strip()
                if potential_link not in interface_list:
                    api_list.add(potential_link)

    except Exception as e:
        print('Something went wrong: ' + str(e))
    return api_list


def assign_api_to_interfaces(base_addr):
    api_list = utilities.read_json(os.path.join(base_addr, "APIs.json"))
    interface_list = utilities.read_json(os.path.join(base_addr, "interfaces.json"))
    api_dict = {}
    try:
        for api in api_list:
            api_dict[api] = set()
            url = 'https://developer.mozilla.org/en-US/docs/Web/API/' + api
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            response = urllib.request.urlopen(req, timeout=10)
            content = BeautifulSoup(response.read(), 'html.parser')
            raw_content_href = content.find_all(href=True)

            # process raw_content_href
            for href in raw_content_href:
                # links have href attribute
                if href['href'].startswith('/en-US/docs/Web/API/'):
                    for interface in interface_list:
                        if href['href'].startswith('/en-US/docs/Web/API/' + interface):
                            api_dict[api].add(interface)
                        if href['href'].startswith('/en-US/docs/Web/API/' + interface + '#'):
                            api_dict[api].add(interface)
            api_dict[api] = list(api_dict[api])
        utilities.write_json(os.path.join(base_addr, "api_interface_dict.json"), api_dict)

    except Exception as e:
        print('Something went wrong: ' + api + ' - ' + str(e))
        pass


def report_unassigned_interfaces(base_dir):
    base_dir = "/home/c6/Desktop/OpenWPM/jsons/community_tracking/real_graphs" \
               "/DY_COMM/labeling_clusters"
    interfaces = utilities.read_json(base_dir + "/interfaces.json")
    api_interface_dict = utilities.read_json(base_dir + "/API_interface_dict.json")

    list_of_interfaces_in_glossary = set(
        [interface for api, interface_list in api_interface_dict.items() for interface in interface_list])

    count = 0
    unassigned_interfaces = set()
    for interface in interfaces:
        if interface not in list_of_interfaces_in_glossary:
            count += 1
            unassigned_interfaces.add(interface)
    print(count)
    return unassigned_interfaces


def report_membership_numbers_of_unassigned_interfaces(unassigned_interfaces, base_addr):
    interface_dict = utilities.read_json(os.path.join(base_addr, "interface_dict.json"))
    count = 0
    for unassigned_interface in unassigned_interfaces:
        if len(interface_dict[unassigned_interface]) == 0:
            count += 1
            # print(unassigned_interface + ":" + str(len(interface_dict[unassigned_interface])))
    print(count)


def create_unknown_api_group_for_unassigned_interfaces(unassigned_interfaces, base_addr):
    api_interface_dict = utilities.read_json(os.path.join(base_addr, "api_interface_dict.json"))
    api_interface_dict["unknown_api"] = unassigned_interfaces
    utilities.write_json(os.path.join(base_addr, "api_interface_dict2.json"), api_interface_dict)


def main():
    # base directory to safe files
    base_addr = '/home/c6/Desktop/OpenWPM/jsons/community_tracking/real_graphs/DY_COMM/labeling_clusters'
    # list of all interfaces in main page of MDN
    interface_address = os.path.join(base_addr, 'interfaces.json')

    # 1. Collect list of interfaces
    # mdn_api_list = list(collect_interface_list())
    # utilities.write_json(interface_address, mdn_api_list)

    # 2. assign keyword to interfaces
    """interfaces = utilities.read_json(interface_address)
    interface_dic = {}
    for interface in interfaces:
        interface_dic[interface] = list(assign_interface_keyword(interface, interfaces))
    utilities.write_json(os.path.join(base_addr, "interface_dict2.json"), interface_dic)"""

    # 3. clean the data
    # clean_processed_items()

    # 4. setify memberList
    # setify_interface_dict(base_addr)

    # 5. collect APIs out of MDN
    # APIs = list(collect_APIs(interface_address))
    # utilities.write_json(os.path.join(base_addr, "APIs.json"), APIs)

    # 6. collect High lever API of interfaces
    # assign_api_to_interfaces(base_addr)

    # 7. List of Interface without any API (310 out of 1029 interfaces doesn't have any API)
    # unassigned_interfaces = list(report_unassigned_interfaces(base_addr))

    # 8. Report number of keywords in each unassigned interface (13 of unassigned interfaces, doesn't have any member)
    # report_membership_numbers_of_unassigned_interfaces(unassigned_interfaces, base_addr)

    # 9 assign unassigned interfaces to an unknown api_group
    # create_unknown_api_group_for_unassigned_interfaces(unassigned_interfaces, base_addr)


if __name__ == '__main__':
    main()
