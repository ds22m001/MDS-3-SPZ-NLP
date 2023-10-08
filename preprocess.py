import re
from nltk.corpus import stopwords
from nltk import word_tokenize
import num2words
from nltk.stem.wordnet import WordNetLemmatizer
import emoji
import contractions
from spellchecker import SpellChecker
import langid

# Pre-processing

def preProcessData(df):

    stop_words = set(stopwords.words('english'))
    spell = SpellChecker()
    lemmatizer = WordNetLemmatizer()

    index = 0

    clean_col = []
    for word in df["review"]:

        # contractions 
        clean_word = contractions.fix(word)

        # emojis
        clean_word = emoji.demojize(clean_word)

        # lowercase
        clean_word = clean_word.lower()

        # Special characters cleaning
        clean_word = re.sub(r'[^\w\s]','', clean_word)
        clean_word = re.sub('_', '', clean_word)

        # Additional spaces cleaning
        clean_word = clean_word.strip()
        clean_word = re.sub(' {2,}', ' ', clean_word)

        # Tokenization -> Word by word processing
        words = word_tokenize(clean_word)
        clean_words = []
        for word in words:
            # Convert numbers to words
            if word.isdigit():
                try:
                    word = num2words.num2words(word)
                except:
                    continue
                
            # Lemmatize
            word = lemmatizer.lemmatize(word)

            # Spell Check
            #if spell.unknown(word):
            #    word = spell.correction(word)

            # Clean stop_words
            if (word not in stop_words):
                clean_words.append(word)

        clean_col.append(" ".join(clean_words))

    df["review_clean"] = clean_col
    return df


def cleanLanguages(data):
    # Generate estimated language and its probability
    data["lanList"] = data["review"].apply(lambda x: langid.classify(x))
    data["lan"] = data["lanList"].apply(lambda x: x[0])
    data["lanProb"] = data["lanList"].apply(lambda x: x[1])
    data.drop(["lanList"], axis=1, inplace = True)

    # Criteria for considering a review in other language
    language = []
    for index, row in data.iterrows():
        if (row["lan"] != "en") & (row["lanProb"] < 16.0):
            language.append("other")
        else:
            language.append("en")
    data["language"] = language
    
    # Drop support columns
    data.drop(['lan'], axis=1, inplace = True)
    data.drop(['lanProb'], axis=1, inplace = True)
    return data