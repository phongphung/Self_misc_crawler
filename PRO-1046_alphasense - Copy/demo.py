import httplib2
import yaml
import json
import logging
from datetime import datetime
from datetime import timedelta
from imp import reload
from pytz import timezone
import pause
import calendar
import pandas as pd
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
#from utils.database import get_pg_connection
#from utils.database import upsert_blogging_candidates

reload(logging)
logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', \
                    level=logging.INFO, datefmt='%I:%M:%S')


def google_custom_search(query, sort_criteria, api_key, cse_id, **kwargs):
    http = httplib2.Http()
    service = build('customsearch', 'v1', developerKey=api_key, http=http)
    try:
        res = service.cse().list(q=query, cx=cse_id, sort=sort_criteria, \
                         **kwargs).execute()
        return res, True
    except HttpError as e:
        logger.info('HTTP Error')
        logger.info(e)
        if json.loads(e.content.decode())['error']['code'] == 403:
            logger.info('Key threshold reached')
            return None, False
        else:
            return None, True
    except Exception as e:
        return None, True


def parse_search_result(search_result, query, gl):
    link = search_result.get('link', '')
    title = search_result.get('title', '')
    pagemap = search_result.get('pagemap', '')
    des_0 = ''
    if type(pagemap) is dict:
        metatags = pagemap.get('metatags', '')
        if metatags:
            des_0 = metatags[0].get('og:description', '')

    if 'blogspot.com' in link:
        rss_url = '{}/feeds/posts/default'.format(link)
    elif 'wordpress.com' in link:
        rss_url = '{}/feed'.format(link)
    else:
        rss_url = ''

    candiate = dict(link=link,
                    title=title,
                    description=des_0,
                    rss=rss_url,
                    payload=search_result,
                    query=query,
                    gl=gl)
    return candiate


def my_search(idx, query, sort_criteria, max_page_num, google_keys, gl):
    active_key = 0

    blogging_candidates = []
    start_position = 1
    total_results_count = 0
    dup_count = 0
    current_results_batch = []
    while True:

        api_key = google_keys[active_key]['api_key']
        cse_id = google_keys[active_key]['cse_id']
        google_keys[active_key]['status'] = 1
        logger.info('Crawling from {}'.format(start_position))
        search_results, key_valid = google_custom_search(query, sort_criteria,
                                            api_key, cse_id,
                                            start=start_position,                                             num=10)
        
            
        if not key_valid:
            active_key = rotate_keys(google_keys)
            logger.info('Key rotated: {}'.format(active_key))
            if active_key == None:
                reset_keys(google_keys)
                logger.info('No key to use. Prepare to sleep')
                logger.info('Stuck at {}'.format(idx))
                wait_for_tomorrow()
                reset_keys(google_keys)
                active_key = 0          
        else:
            if search_results:
                try:
                    total_results_count = \
                        int(search_results['searchInformation']\
                                            ['totalResults'])
                    if total_results_count < 100:
                        max_page_num = int(total_results_count / 10) + 1
                    if total_results_count == 0:
                        logger.info('Empty results')
                        break

                    if 'items' in search_results:
                        blogging_candidates.extend(search_results['items'])

                        if search_results['items'] == current_results_batch:
                            dup_count += 1
                        if dup_count == 3:
                            break
                        current_results_batch = search_results['items']

                    logger.info("max page num: {}".format(max_page_num))
                    if (start_position / 10 + 1) < max_page_num:
                        start_position = int(
                                search_results['queries']['nextPage'][0][
                                    'startIndex'])
                    else:
                        logger.info("Done")
                        break
                except Exception as e:
                    logger.info(e)
            else:
                break
        
    return blogging_candidates, key_valid

    
def reset_keys(google_keys):
    for key in google_keys:
        key['status'] = 0
    
        
def rotate_keys(google_keys):
    """
    Disble current key.
    Return next available key.
    """
    for key in google_keys:
        if key['status'] == 1:
            key['status'] = -1 
        
    for idx, key in enumerate(google_keys):
        if key['status'] == 0:
            key['status'] = 1 
            return idx
    return None
   
    
def wait_for_tomorrow():
    """
    Sleep until midnight based on Pacific timezone.
    """
    
    pacific = timezone('US/Pacific')
    tomorrow_pacific = datetime.now(pacific) + timedelta(days=1)
    restart_at = tomorrow_pacific.replace(
                                hour=0, minute=0, second=10, microsecond=0)
#    restart_at_utc= restart_at.astimezone(utc)
    restart_at_unix_timestamp = calendar.timegm(restart_at.utctimetuple())
    pause.until(restart_at_unix_timestamp)
    

def transform_candidates_data(search_results, query, gl):
    candidates = [parse_search_result(result, query, gl) for result \
                                                          in search_results]

    return candidates     
    
    
def persist_candidates(conn, candidates):
    upsert_blogging_candidates(conn, candidates)
    return    
     
if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    with open('conf/settings.yml', 'rb') as f:
        settings = yaml.load(f)

    sql = settings.get('SQL', '')
    sort_criteria = settings.get('SORT_CRITERIA', '')
    max_page_num = settings.get('MAX_PAGE_NUM', 0)
    keyword_file_path = settings.get('KEYWORD_FILE', '')

    kw_df = pd.read_excel(keyword_file_path, coding='utf-8')
    urls = kw_df['keywords'].values.tolist()
    urls = ["yolasite.com",
            "typepad.com",
            "wix.com",
            ]
    kws = kw_df['keywords'].dropna().values.tolist()
    keywords = [dict(query='site:{} {}'.format(url, kw.encode("utf-8")))
                for url in urls for kw in kws]

    # # Free-edition keys
    # # status: 0 - valid, ready to use. 1 - being used. -1 limit reached.
    # # Hung
    # g_key1 = dict(api_key='AIzaSyBiluBxWUik4sBm82p-Nezr-bZB1yVB0Sg',
    #               cse_id='007234815836235761893:1lkpzg3a_ck', status=0)
    # # Chi
    # g_key6 = dict(api_key='AIzaSyBPkfkXkC3JRV3eTWMzC6RyDAt7j6EDJFQ',
    #               cse_id='007457294470260374074:pflo3uejxku', status=0)
    # # Phong
    # g_key11 = dict(api_key='AIzaSyB5unEtBzttnQ0tJ3B_LbTpm4WfEO6iSKI',
    #                 cse_id = '015458923067084818477:799qjartqou', status=0)
    # g_key12 = dict(api_key='AIzaSyAtb8Lnu0VdpXvGhJqCOpZXe-q8LwRV-sE',
    #                 cse_id = '003546909602338648873:bqhrdgcrpy4', status=0)
    # g_key13 = dict(api_key='AIzaSyBphxo-SVOHyrz06RyiG7sMH8fseRMLaiM',
    #                 cse_id = '000519485165825485187:iz_tshgvcrm', status=0)
    # g_key14 = dict(api_key='AIzaSyBKryTarv_6CL_FLOegeCPxP3ulP1cQtgk',
    #                 cse_id = '012057603104391785746:zsy1fmbgig4', status=0)
    # google_keys = [g_key1, g_key6, g_key11, g_key12, g_key13, g_key14]

    comm_key = dict(api_key='AIzaSyCMGfdDaSfjqv5zYoS0mTJnOT3e9MURWkU',
                    cse_id='007234815836235761893:1lkpzg3a_ck', status=0)
    google_keys = [comm_key]
    
    conn = get_pg_connection(sql['DB'], 
                                sql['USER'], sql['PASSWORD'],
                                sql['HOST'], sql['PORT'])
    
    for idx, kw in enumerate(keywords[:]):
        max_page_num = settings.get('MAX_PAGE_NUM', 0)
        query = kw['query']
        gl = ''
        
        logger.info('Prepare to search: {}-{}'.format(query, gl))
        results, key_valid = my_search(idx, query, sort_criteria, \
                                       max_page_num, google_keys, gl)

        with open('log.txt', 'a') as f:
            f.write(query + ' ' + gl + '\n')
            
        if results:
            candidates = transform_candidates_data(results, query, gl)
            candidates = pd.DataFrame(candidates)
            candidates.drop_duplicates(subset='link', inplace=True)
            
            persist_candidates(conn, candidates)
            
        else:
            logger.info('Empty search result')
        logger.info('Crawl successful {}'.format(idx))
