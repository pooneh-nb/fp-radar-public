import sqlite3 as lite
from sqlite3 import Error
import tldextract
import pandas as pd
import json
import tldextract as tld
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats


NROWS = 15

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

    requested_third_parties = pd.DataFrame(columns=['visit_id', 'url', 'name', 'value'])
    url_vis_DF = pd.DataFrame(columns=['visit_id', 'url', 'name', 'value'])
    ru = []

    cur = conn.cursor()
    cur.execute("SELECT visit_id, host, name, value FROM javascript_cookies")
    rows = cur.fetchall()
    for i in range(len(rows)):
        if (rows[i][1][0] == '.'):
            rows[i] = (rows[i][0], rows[i][1][1:])

    url_vis_DF = pd.DataFrame(rows, columns=['visit_id', 'url', 'name', 'value'])

    for vis_id in range(NROWS):
        vis_id = vis_id + 1
        main_domain = []
        requested_URL = []
        cookie_df_temp = url_vis_DF.loc[url_vis_DF['visit_id'] == vis_id]

        if (not cookie_df_temp.empty):
            # extracting the main domain
            main_domain = tld.extract(cookie_df_temp.iloc[0]['url'])

            # extracting the main domain
            main_domain = tld.extract(rows[0][1])

            # extracting list of requested domains
            for inx, url in cookie_df_temp['url'].iteritems():
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
                            ru = [(vis_id, ext.registered_domain, cookie_df_temp.loc[inx]['name'], cookie_df_temp.loc[inx]['value'])]
                            requested_URL = pd.DataFrame(ru, columns=['visit_id', 'url', 'name', 'value'])
                            requested_third_parties = requested_third_parties.append(requested_URL, ignore_index=True)
                    else:
                        ru = [(vis_id, ext.registered_domain, cookie_df_temp.loc[inx]['name'], cookie_df_temp.loc[inx]['value'])]
                        requested_URL = pd.DataFrame(ru, columns=['visit_id', 'url', 'name', 'value'])
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
        'Distribution of # of 3rd-party Cookie requests in “vanilla mode"')
    else:
        plt.title(
            'Distribution of # of 3rd-party Cookies requests in “adBlocked mode"')
    plt.xlabel('Number of requests')
    plt.ylabel('')
    if mode == 'vanilla':
        plt.savefig('cookies_dist_vanilla.png')
    else:
        plt.savefig('cookies_dist_ad_blocked.png')
    plt.clf()
def extract_top_ten_3rdparties(df_third_parties, mode):
    # List the top-10 most popular third-party domains requested by http protocol
    # input: a dataframe from collect_third_parties('visit_id', '3rd_party_url') function, mode(vanilla/adblocked)
    # output: plot top 10 3rdparties
    df_third_parties = df_third_parties.groupby('url').count().reset_index()
    df_third_parties =df_third_parties.rename(columns={'url':'3rdparties','visit_id':'number'})
    df_third_parties = df_third_parties.sort_values(by=['number'], ascending=False)

    #print(df_third_parties)
    if mode == 'vanilla':
        print("list of top 10 third parries in vanilla mode--Cookies")
    else:
        print("list of top 10 third parries in vanilla mode--Cookies")
    print(df_third_parties.head(10))


def main():
    database_vanilla = "/home/pooneh/PycharmProjects/OpenWPM/datasets/250-vanila/250-vanilla-crawl-data.sqlite"
    database_adBlocked = "/home/pooneh/PycharmProjects/OpenWPM/datasets/250-adblocked/250-adblocked-crawl-data.sqlite"
    # create a database connection
    conn = create_connection(database_vanilla)
    conn2 = create_connection(database_adBlocked)

    #Vanilla mode
    with conn:

        print("collect_third_parties - vanilla mode--Cookies")
        df_third_parties_vanilla = collect_third_parties(conn)
        df_third_parties_vanilla.to_csv('cookie_df_third_parties_vanilla')

        print("distribution of number of third-party cookie requests made by Alexa top 250 websites-vanilla mode")
        plot_accumulate_third_parties(df_third_parties_vanilla, mode = 'vanilla')

        print("List the top-10 most popular third-party domains requested by cookie --vanilla mode")
        extract_top_ten_3rdparties(df_third_parties_vanilla, mode = 'vanilla')

     #adBlocked mode
    with conn2:
        print("collect_third_parties -- adblocked mode--JS")
        df_third_parties_adblocker = collect_third_parties(conn2)


        print("distributionofnumberof third-party cookie requests made by Alexa top 250 websites-- Adblocked mode")
        plot_accumulate_third_parties(df_third_parties_adblocker, mode ='adBlocked')

        print("List the top-10 most popular third-party domains requested by cookie -- Adblocked mode")
        extract_top_ten_3rdparties(df_third_parties_adblocker,  mode ='adBlocked')





if __name__ == '__main__':
    main()

