import random
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import csr_matrix

random.seed(42)

def get_tfidf_score_for_words(df):
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(df['review_clean'])
    feature_names = tfidf_vectorizer.get_feature_names_out()

    tfidf_scores_df = pd.DataFrame({'Word': feature_names, 'TF-IDF-Score': tfidf_matrix.mean(axis=0).tolist()[0]})
    tfidf_scores_df = tfidf_scores_df.sort_values(by='TF-IDF-Score', ascending=False)
    return tfidf_scores_df

def get_random_reviews_per_appid(df, n=5):
    app_ids = df['app_id'].unique().tolist()
    random_app_ids = random.sample(app_ids, n)
    df_random_app_ids = df[df['app_id'].isin(random_app_ids)]
    return df_random_app_ids

def print_tfidf_score_for_words_per_appid(df, n_ids=5, n_words=10):
    df_random_app_ids = get_random_reviews_per_appid(df, n_ids)
    app_ids = df_random_app_ids['app_id'].unique().tolist()
    for app_id in app_ids:
        print(f'app_id: {app_id}')
        tfidf_scores_df = get_tfidf_score_for_words(df_random_app_ids[df_random_app_ids['app_id'] == app_id])
        print(tfidf_scores_df.head(n_words))