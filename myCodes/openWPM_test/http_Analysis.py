import sqlite3 as lite
from sqlite3 import Error
import tldextract
import pandas as pd
import json
import tldextract as tld
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
import time
#from fuzzywuzzy import fuzz


NROWS = 250

# jason file of forwarded domains to a unique website
with open('../disconnect-tracking-protection/entities.json') as f:
  forwarded_domains = json.load(f)
#mydict_in_str = json.dumps(forwarded_domains)
#forwarded_domains = json.loads(mydict_in_str.lower())


def create_connection(db_file):
    # creat a database connection to SQLite database
    # input: address to the database
    #output: connection object
    conn = None
    try:
        conn = lite.connect(db_file)
    except Error as e:
        print(e)
    return conn


def query_table_names(conn):
    # return table names
    #inut connection object
    #output: list of table names

    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    return cur.fetchall()


def collect_third_parties(conn):
    # collect all the third_party domains for 250 ALexa top websites
    # input: connection object
    # output: a dataframe (columns=['visit_id', '3rd_party_url']) contains the urls of 3rd party site requested from 250 Alexa websites

    requested_third_parties = pd.DataFrame(columns=['visit_id', 'url'])
    url_vis_DF = pd.DataFrame(columns={'visit_id', 'url'})
    ru =[]

    cur = conn.cursor()
    cur.execute("SELECT visit_id, url FROM http_requests")
    rows = cur.fetchall()
    url_vis_DF = pd.DataFrame(rows, columns=['visit_id', 'url'])

    #df = pd.DataFrame(columns=['visit_id', 'url'])
    #requested_third_parties = pd.DataFrame(columns=['visit_id', 'url'])
    
    for vis_id in range(NROWS):
        vis_id = vis_id + 1
        print(vis_id)
        main_domain = []
        requested_URL = []
        #cur = conn.cursor()
        #cur.execute("SELECT visit_id,url FROM http_requests WHERE visit_id=?", (vis_id,))
        https_df_temp = url_vis_DF.loc[url_vis_DF['visit_id'] == vis_id]
        if (not https_df_temp.empty):
            #temp_df = pd.DataFrame(rows, columns=['visit_id', 'url'])
            #df = df.append(temp_df, ignore_index=True)
            # extracting the main domain
            main_domain = tld.extract(https_df_temp.iloc[0]['url'])

            # extracting list of requested domains
            for url in https_df_temp['url']:
                ext = tld.extract(url)
                if (
                        ext.domain != main_domain.domain):  # check the requested link of a domain, if they are not same, it is probably a 3rd party
                    # for key, value in forwarded_domains.items():  # check whether the 3rd-party one of the forwarded links
                    if main_domain.domain in forwarded_domains:
                        # if all(key in forwarded_domains for key in (main_domain.domain)):
                        # if main_domain.domain in value:
                        if ext.registered_domain not in forwarded_domains[main_domain.domain][
                            'properties'] and ext.registered_domain not in \
                                forwarded_domains[main_domain.domain][
                                    'resources']:
                            ru = [(vis_id, ext.registered_domain)]
                            requested_URL = pd.DataFrame(ru, columns=['visit_id', 'url'])
                            requested_third_parties = requested_third_parties.append(requested_URL, ignore_index=True)
                    else:
                        ru = [(vis_id, ext.registered_domain)]
                        requested_URL = pd.DataFrame(ru, columns=['visit_id', 'url'])
                        requested_third_parties = requested_third_parties.append(requested_URL, ignore_index=True)
    return (requested_third_parties)


def plot_accumulate_third_parties(df_third_parties, mode):
    # accumulate the number of requested 3rdparty domains from each Alexa website. plot the distribution of the data
    #input: a dataframe from collect_third_parties('visit_id', '3rd_party_url') function, mode(vanilla/adblocked)
    #output: plot the distribution of data
    accumulate_df = pd.DataFrame()
    accumulate_df = df_third_parties.groupby(['visit_id']).count()

    # seaborn histogram
    sns.distplot(accumulate_df['url'], hist=True, kde=False,
                 bins=int(180/5), color='blue',
                 hist_kws={'edgecolor': 'black'})
    # Add labels
    if mode=='vanilla':
        plt.title(
        'Distribution of # of 3rd-party HTTP requests in “vanilla mode"')
    else:
        plt.title(
            'Distribution of # of 3rd-party HTTP requests in “adBlocked mode"')
    plt.xlabel('Number of requests')
    plt.ylabel('')
    if mode == 'vanilla':
        plt.savefig('https_dist_vanilla.png')
    else:
        plt.savefig('https_dist_ad_blocked.png')

    plt.clf()
def extract_top_ten_3rdparties(df_third_parties, mode):
    # List the top-10 most popular third-party domains requested by http protocol
    # input: a dataframe from collect_third_parties('visit_id', '3rd_party_url') function, mode(vanilla/adblocked)
    # output: plot top 10 3rdparties
    df_third_parties = df_third_parties.groupby('url').count().reset_index()
    df_third_parties = df_third_parties.rename(columns={'url':'3rdparties','visit_id':'number'})
    df_third_parties = df_third_parties.sort_values(by=['number'], ascending=False)

    #print(df_third_parties)
    if mode == 'vanilla':
        print("list of top 10 third parries in vanilla mode -HTTP")
    else:
        print("list of top 10 third parries in vanilla mode - HTTP")

    print(df_third_parties[['3rdparties']].head(10))


def main():
    database_vanilla = "/media/pooneh/Pouneh/Desktop/Summer/shafiq/OpenWPM/OpenWPM/datasets/250-vanila/250-vanilla-crawl-data.sqlite"
    database_adBlocked = "/media/pooneh/Pouneh/Desktop/Summer/shafiq/OpenWPM/OpenWPM/datasets/250-adblocked/250-adblocked-crawl-data.sqlite"
    # create a database connection
    conn = create_connection(database_vanilla)
    conn2 = create_connection(database_adBlocked)

    #Vanilla mode
    with conn:
        #print("query table names")
        #query_table_names(conn)
        tic =time.process_time()
        print("collect_third_parties - vanilla mode")
        df_third_parties_vanilla = collect_third_parties(conn)
        #print(df_third_parties)
        toc = time.process_time()

        print(toc-tic)

        print("distribution of number of third-party HTTP(S)requestsmade by Alexa top 250 websites-vanilla mode")
        plot_accumulate_third_parties(df_third_parties_vanilla, mode = 'vanilla')

        print("List the top-10 most popular third-party domains requested by http protocol--vanilla mode")
        extract_top_ten_3rdparties(df_third_parties_vanilla, mode = 'vanilla')

     #adBlocked mode
    with conn2:
        print("collect_third_parties -- adblocked mode")
        df_third_parties_adblocked = collect_third_parties(conn2)


        print("distribution of number of third-party HTTP requestsmade by Alexa top 250 websites-- Adblocked mode")
        plot_accumulate_third_parties(df_third_parties_adblocked, mode ='adBlocked')

        print("List the top-10 most popular third-party domains requested by http protocol-- Adblocked mode")
        extract_top_ten_3rdparties(df_third_parties_adblocked,  mode ='adBlocked')


if __name__ == '__main__':
    main()

