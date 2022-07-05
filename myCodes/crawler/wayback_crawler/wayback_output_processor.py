from myCodes.AST import utilities
import os


def create_existing_urls_dataframe(positive_log, top_urls, outdir):
    available_urls = {}
    for pos in positive_log:
        url_id = pos.split('/')[-1].split('.')[0].split('|')[-1]
        url = top_urls[url_id]
        info = utilities.read_json(pos)
        timestamps = []
        for record in info:
            if record[0] != "original":
                timestamps.append(record[1])
        available_urls[url_id] = {"url": url, "timestamps": timestamps}

    utilities.write_json(os.path.join(outdir, "available_urls.json"), available_urls)


def create_wayback_available_urls(available_urls, outdir):
    callable_urls = []
    for url_id, value in available_urls.items():
        url = value["url"]
        timestamps = value["timestamps"]
        for requested_time in timestamps:
            callable_urls.append("http://web.archive.org/web/" + requested_time + "/" + url)
    utilities.write_json(os.path.join(outdir, "callable_urls.json"), callable_urls)


def main():
    positive_log = utilities.get_files_in_a_directory("/home/c6/Desktop/OpenWPM/jsons/top_million_urls/Wayback/CDX_API/cdx_jsons")
    top_urls = utilities.read_json("/home/c6/Desktop/OpenWPM/jsons/top_million_urls/top_urls.json")
    outdir = "/home/c6/Desktop/OpenWPM/jsons/top_million_urls"
    #create_existing_urls_dataframe(positive_log, top_urls, outdir)
    available_urls = utilities.read_json(os.path.join(outdir, "available_urls.json"))
    create_wayback_available_urls(available_urls, outdir)


if __name__ == '__main__':
    main()
