from myCodes.AST import utilities
import os

# provide the list of fingerprinting scripts URLs for each year.
def fp_report():
    years = ["2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019"]
    fp_script_urls = utilities.read_json("/home/c6/Desktop/OpenWPM/jsons/third_parties/all_3rdparty_fp_script_urls.json")
    fp_files_dir =  "/home/c6/Desktop/OpenWPM/jsons/CDX_api/gathered_downloaded_files/fp_date_organized"

    fp_report = {}
    for year in years:
        fp_report[year] = []
        fp_dated_files = utilities.get_files_in_a_directory(os.path.join(fp_files_dir, year, "all"))
        for file in fp_dated_files:
            script_id = int(file.split('/')[-1].split('|')[-1])
            for _, value in fp_script_urls.items():
                if value["url_id"] == script_id:
                    fp_report[year].append(value["script_url"])

    for year in years:
        fp_report[year] = list(set(fp_report[year]))
    fp_count_report = {}
    for year in years:
        fp_count_report[year] = len(fp_report[year])

    utilities.write_json(os.path.join("/home/c6/Desktop/OpenWPM/jsons/third_parties/paper_report",
                                      "annual_fp_script_urls.json"), fp_report)

    utilities.write_json(
        os.path.join("/home/c6/Desktop/OpenWPM/jsons/third_parties/paper_report", "annual_fp_count_report.json"),
        fp_count_report)


# provide the list of non_fingerprinting scripts URLs for each year.
def non_fp_report():
    years = ["2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019"]
    non_fp_script_urls = utilities.read_json(
        "/home/c6/Desktop/OpenWPM/jsons/third_parties/non_fp_3rd_url_20k.json")
    non_fp_files_dir = "/home/c6/Desktop/OpenWPM/jsons/CDX_api/gathered_downloaded_files/non_fp_date_organized"

    non_fp_report = {}
    for year in years:
        print(year)
        non_fp_report[year] = []
        dated_files = utilities.get_files_in_a_directory(os.path.join(non_fp_files_dir, year+"_unique", "all"))
        for file in dated_files:
            script_id = int(file.split('/')[-1].split('|')[-1])
            for _, value in non_fp_script_urls.items():
                if value["url_id"] == script_id:
                    non_fp_report[year].append(value["url"])

    for year in years:
        non_fp_report[year] = list(set(non_fp_report[year]))

    non_fp_count_report = {}
    for year in years:
        non_fp_count_report[year] = len(non_fp_report[year])

    utilities.write_json(os.path.join("/home/c6/Desktop/OpenWPM/jsons/third_parties/paper_report",
                                      "annual_non_fp_script_urls.json"), non_fp_report)
    utilities.write_json(
        os.path.join("/home/c6/Desktop/OpenWPM/jsons/third_parties/paper_report", "annual_non_fp_count_report.json"),
        non_fp_count_report)


#fp_report()
non_fp_report()
