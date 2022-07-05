from myCodes.AST import utilities


def existing_non_fp_snapshots_CDX():
    #non_fp

    #yes/no snapshots
    existing_non_fp = utilities.get_files_in_a_directory("/home/c6/Desktop/OpenWPM/jsons/CDX_api/CDX_jsons/non_fp_jsons")
    yes_response = []
    no_response = []
    for file_name in existing_non_fp:
        if file_name.split('/')[-1].split('|')[0] == 'no':
            no_response.append(file_name)
        if file_name.split('/')[-1].split('|')[0] == 'yes':
            yes_response.append(file_name)

    num_of_existing_non_fp = len(yes_response)
    num_non_existing_non_fp = len(no_response)

    ### aborted_urls
    aborted_urls = open("/home/c6/Desktop/OpenWPM/jsons/CDX_api/CDX_jsons/CDX_errors/non_fp_aborted_err.txt", "r")
    Lines = aborted_urls.readlines()
    error_unique = set()

    for line in Lines:
        error_unique.add(line.split('|')[0])
    # ('Connection aborted.', RemoteDisconnected('Remote end closed connection without response'))
    number_of_aborted_non_fp = len(error_unique)

    ### 404 error
    retry_urls = open("/home/c6/Desktop/OpenWPM/jsons/CDX_api/CDX_jsons/CDX_errors/non_fp_404_err.txt", "r")
    retry_line = retry_urls.readlines()
    error_404_unique = set()

    for lnn in retry_line:
        error_line_404 = lnn.split('|')[0]
        error_404_unique.add(error_line_404)
    number_of_retry_non_fp = len(error_404_unique)

    print(num_of_existing_non_fp)
    print(num_non_existing_non_fp)
    print(number_of_aborted_non_fp)
    print(number_of_retry_non_fp)


def existing_fp_snapshots_CDX():
    #FP

    #yes/no snapshots
    existing_non_fp = utilities.get_files_in_a_directory("/home/c6/Desktop/OpenWPM/jsons/CDX_api/CDX_jsons/fp_jsons")
    yes_response = []
    no_response = []
    for file_name in existing_non_fp:
        if file_name.split('/')[-1].split('|')[0] == 'no':
            no_response.append(file_name)
        if file_name.split('/')[-1].split('|')[0] == 'yes':
            yes_response.append(file_name)

    num_of_existing_fp = len(yes_response)
    num_non_existing_fp = len(no_response)

    ### aborted_urls
    aborted_urls = open("/home/c6/Desktop/OpenWPM/jsons/CDX_api/CDX_jsons/CDX_errors/fp_aborted_err.txt", "r")
    Lines = aborted_urls.readlines()
    error_unique = set()

    for line in Lines:
        error_unique.add(line.split('|')[0])
    # ('Connection aborted.', RemoteDisconnected('Remote end closed connection without response'))
    number_of_aborted_fp = len(error_unique)

    ### 404 error
    retry_urls = open("/home/c6/Desktop/OpenWPM/jsons/CDX_api/CDX_jsons/CDX_errors/fp_404_err.txt", "r")
    retry_line = retry_urls.readlines()
    error_404_unique = set()

    for lnn in retry_line:
        error_line_404 = lnn.split('|')[0]
        error_404_unique.add(error_line_404)
    number_of_retry_fp = len(error_404_unique)

    print(num_of_existing_fp)
    print(num_non_existing_fp)
    print(number_of_aborted_fp)
    print(number_of_retry_fp)


existing_non_fp_snapshots_CDX()