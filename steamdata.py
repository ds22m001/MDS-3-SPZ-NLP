import pandas as pd
import steamtable
from bs4 import BeautifulSoup
import requests
import database
import time
from urllib.parse import quote


#get app_ids from steamtable.py
def get_app_ids():
    html = steamtable.html
    soup = BeautifulSoup(html, 'html.parser')
    rows = soup.find_all('tr', class_='weeklytopsellers_TableRow_2-RN6')
    app_ids = []

    for row in rows:
        app_number = row.find_all('td')[2].find('a')['href'].split('/')[-2]
        app_ids.append(app_number)
    return app_ids



# save reviews of last 365 days via steamreviews
def get_data_from_steam(app_ids):
    language = 'english'
    num_per_page = 100
    day_range = 365
    filters = ['all', 'recent', 'updated']

    total_reviews_to_download = 400

    print('total expected reviews to download: ' + str(total_reviews_to_download*len(filters)*len(app_ids)))

    data_all = pd.DataFrame()
    data_sum = pd.DataFrame()

    for app_id in app_ids:
        for filter in filters:
            reviews_downloaded = 0
            cursor = '*'

            while reviews_downloaded < total_reviews_to_download:
                try:
                    url = 'https://store.steampowered.com/appreviews/' + str(app_id) + '?json=1' + '&cursor=' + str(cursor) + '&language=' + str(language) + '&num_per_page=' + str(num_per_page) + '&filter=' + str(filter) + '&day_range=' + str(day_range)
                    response = requests.get(url)

                    cursor_new = quote(response.json()['cursor'])

                    data_tmp = pd.DataFrame(response.json()['reviews'])
                    data_tmp['app_id'] = app_id
                    data_all = pd.concat([data_all, data_tmp], ignore_index=True)
                    reviews_downloaded += len(data_tmp)

                    if cursor_new == cursor:
                        break
                    else:  
                        cursor = cursor_new

                except:
                    break
            #time.sleep(1)
            if reviews_downloaded < total_reviews_to_download:
                print('fewer downloads than expected - app_id index: ' + str(app_ids.index(app_id)) + ', app_id: ' + str(app_id) + ', filter: ' + str(filter) + ', reviews downloaded: '  + str(reviews_downloaded) + ', url: ' + url)
    
    print('total downloaded: ' + str(len(data_all)))

    return data_all

# get data_list from json files
def get_data_cols(df):
    data = pd.DataFrame()
    data = df[['app_id', 'recommendationid', 'review', 'voted_up', 'votes_up', 'votes_funny', 'weighted_vote_score']]
    return data

#main function for update data
def update_data():
    app_ids = get_app_ids()
    df = get_data_from_steam(app_ids)
    data = get_data_cols(df)
    database.send_to_database(data)


