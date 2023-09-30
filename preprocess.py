import re

def get_preprocessed_data(df):
    df['review_preprocessed'] = df['review'] # copy column
    df['review_preprocessed'] = df['review'].str.lower() # lowercase
    df['review_preprocessed'] = df['review_preprocessed'].str.replace(r'\d+','') # remove numbers
    df['review_preprocessed'] = df['review_preprocessed'].str.replace(r'\n',' ') # remove line breaks
    return df