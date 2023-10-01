from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
from textstat import textstat


def visualize_wordcloud(text, include_stopwords):
    wordcloud = WordCloud(stopwords=([] if include_stopwords else None)).generate(text)
    # display image
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()


def get_word_count(words):
    result = {}

    for word in words:
        if word in result:
            result[word] += 1
        else:
            result[word] = 1

    return result


def visualize_word_count(words, max_words=30, rotation_angle=60):
    df = pd.DataFrame(get_word_count(words).items(), columns=["word", "count"])
    fig, ax = plt.subplots(figsize=(12, 7))
    df.sort_values(by='count', ascending=False, inplace=True)
    df_short = df.iloc[0:max_words]
    plt.bar(df_short["word"].tolist(), df_short["count"].tolist())
    plt.xticks(rotation=rotation_angle)
    plt.show()


def readability_scores(texts: [str], title: str = ""):
    flesch_reading_scores = [textstat.flesch_reading_ease(text) for text in texts]
    automated_readability_indices = [textstat.automated_readability_index(text) for text in texts]

    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(8, 6))
    st = fig.suptitle(title, fontsize=14)

    axes[0, 0].set_title("Flesch Reading Ease")
    axes[0, 1].set_title("Flesch Reading Ease")
    axes[0, 0].boxplot(flesch_reading_scores)
    axes[0, 1].hist(flesch_reading_scores, bins=30)

    axes[1, 0].set_title("Automated Readability Index")
    axes[1, 1].set_title("Automated Readability Index")
    axes[1, 0].boxplot(automated_readability_indices)
    axes[1, 1].hist(automated_readability_indices, bins=30)
    fig.tight_layout()

    st.set_y(0.95)
    fig.subplots_adjust(top=0.85)

    plt.show()
