import socket
from urllib.request import urlopen, HTTPError
from urllib.error import URLError
import pandas as pd
import http.client
import tldextract as tld

socket.setdefaulttimeout(5)  # timeout in seconds

a = pd.read_csv('final_fix_ctry_code_avatar.csv')


def ping(url):
    try:
        urlopen(url)

    except HTTPError as e:
        return e

    except URLError as e:
        return e

    except:
        return 'error'

    else:
        return 1


temp = pd.DataFrame(list(set(a['payload_url'])))
temp['check_ping'] = ''
temp.columns = ['payload_url', 'check_ping']

for i in range(0, len(temp), 200):
    print(i)

    temp.loc[i:i+200, 'check_ping'] = \
        temp['payload_url'][i:i+200].apply(ping)


def check_ping2(x):
    try:
        print(x)
        url = '.'.join(filter(None, tld.extract(x)))
        a = http.client.HTTPConnection(url)
        a.connect()
        return 1
    except http.client.HTTPException:
        return 'error'
    except:
        return 'error2'

temp = pd.read_csv('temp.csv')
temp = temp[temp['check_ping'] != '1']
temp.reset_index(drop=True, inplace=True)

temp.to_csv('checked_ping_2.csv')
