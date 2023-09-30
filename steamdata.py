import pandas as pd
import steamreviews
import json

#main function for getting data
def get_data(app_ids):
    save_reviews365(app_ids)
    data_list = get_data_list(app_ids)
    return data_list

# save reviews of last 365 days via steamreviews
def save_reviews365(app_ids):
    request_params = dict()
    request_params['language'] = 'english'
    request_params['num_per_page'] = '100'
    request_params['filter'] = 'recent'
    request_params['day_range'] = '365'

    while True:
        try:
            review_dict, query_count = steamreviews.download_reviews_for_app_id_batch(app_ids, chosen_request_params=request_params)
        except:
            break

# get data_list from json files
def get_data_list(app_ids):
    data_list = []
    for app_id in app_ids:
        file_path = 'data/review_' + str(app_id) + '.json'
        with open(file_path, 'r') as json_file:
            data_json = json.load(json_file)
        for review_id, review_info in data_json['reviews'].items():
            row = {
                'app_id': app_id,
                'recommendationid': review_info['recommendationid'],
                'review': review_info['review'],
                'voted_up': review_info['voted_up'],
                'votes_up': review_info['votes_up'],
                'votes_funny': review_info['votes_funny'],
                'weighted_vote_score': review_info['weighted_vote_score'],
                'comment_count': review_info['comment_count']
            }
            data_list.append(row)
    return data_list

