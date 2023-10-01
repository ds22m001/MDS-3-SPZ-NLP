import re
import emoji
import inflect

from spellchecker import SpellChecker

def get_preprocessed_data(df):
    


    df = turn_lowercase(df) # turn lowercase
    
    # spellchecker - takes a very long time
    spell = SpellChecker()
    df["review_preprocessed"] = [' '.join([spell.correction(i) for i in x.split()]) for x in df['review_preprocessed']]

    df['review_preprocessed'] = df['review_preprocessed'].str.replace(r'\d+','') # remove numbers
    df['review_preprocessed'] = df['review_preprocessed'].str.replace(r'\n',' ') # remove line breaks
    df['review_preprocessed'] = df['review_preprocessed'].str.replace(r'\t',' ') # remove tabs
    df['review_preprocessed'] = df['review_preprocessed'].str.replace('[^\w\s]','') #remove punctuation

    df['review_preprocessed'] = emoji.demojize(df['review_preprocessed']) # translate emojis


    return df

# Convert characters to lower case
def turn_lowercase(df):
    return df['review'].str.lower()

def convert_number_to_text(df):
    return 