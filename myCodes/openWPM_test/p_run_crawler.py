from automation import TaskManager, CommandSequence
import tempfile
import time
import os
import copy
import json
import csv
import pandas as pd

NUM_BROWSERS = 1
NUM_ROWS = 1

# The list of sites that we wish to crawl
#df = pd.read_csv('~/Desktop/OpenWPM/myCodes/openWPM_test/test.csv', nrows= NUM_ROWS)
####sites = ['https://joinhoney.com']

#sites = []
#for row in range(df.shape[0]):
    #sites.append("https://"+df.loc[row][1])
site='https://davidwalsh.name/demo/window-post-message.php'

#Loads the default manager preferences and #NUM_BROWSERS copies of the default browser dictionaries
manager_params, browser_params = TaskManager.load_default_params(NUM_BROWSERS)

#update browser configuration (use this for per-browser settings)

for i in range(NUM_BROWSERS):
    browser_params[i]['http_instrument'] = True
    browser_params[i]['cookie_instrument'] = True
    browser_params[i]['ublock-origin'] = False  # vanilla/adblocker mode (default false)
    #Javascript Calls
    #Records all method calls (with arguments) and property accesses for configured APIs
    browser_params[i]['js_instrument'] = True  # Data is saved to the javascript table
    browser_params[i]['js_instrument_settings'] = ['Window','targetWindow','postMessage','addEventListener','postMessage'] # Data is saved to the javascript table




#update TaskManager configuration (use this for crawl-wide settings
manager_params['data_directory'] = '~/Desktop'
manager_params['log_directory'] = '~/Desktop'


# Instantiates the measurement platform
# Commands time out by default after 60 seconds
manager = TaskManager.TaskManager(manager_params, browser_params)

# Visits the sites with all browsers simultaneously
#for site in sites:
command_sequence = CommandSequence.CommandSequence(site, reset=True)
command_sequence.get(sleep=30, timeout=60)
manager.execute_command_sequence(command_sequence)


#Shuts down the browsers and waits for the data to finish logging
manager.close()

