import re
import re
import emoji
from spellchecker import SpellChecker

def get_preprocessed_data(df):
    # spellchecker - takes a very long time
    spell = SpellChecker()
    df["review_preprocessed"] = [' '.join([spell.correction(i) for i in x.split()]) for x in df['review_preprocessed']]

    df['review_preprocessed'] = df['review_preprocessed'].str.replace(r'\d+','') # remove numbers
    df['review_preprocessed'] = df['review_preprocessed'].str.replace(r'\n',' ') # remove line breaks
    df['review_preprocessed'] = df['review_preprocessed'].str.replace(r'\t',' ') # remove tabs
    df['review_preprocessed'] = df['review_preprocessed'].str.replace('[^\w\s]','') #remove punctuation

    df['review_preprocessed'] = emoji.demojize(df['review_preprocessed']) # translate emojis

    df['review_preprocessed'] = df['review'].str.lower() # lowercase
    return df