"""
The text visualization module. Builds wordcloud from the scraped dict of the meetup site
Might be extended by other visualizations
"""
import logging
import pickle
from collections import Counter
from typing import Dict, List

import nltk
from matplotlib import pyplot as plt
from nltk import ngrams
from nltk.corpus import stopwords
from wordcloud import WordCloud, STOPWORDS

from utils.get_logger import get_logger
from utils.text_helpers import _nltk_prep

logger: logging.Logger = get_logger()

CUSTOM_STOPWORDS = ["will", "Meetup", "https", "event", "harassment",
                    "Berlin", "Karlsruhe", "Munich", "Hamburg"] + list(STOPWORDS)


def build_and_show_wordcloud(events_dict: Dict, city_to_plot: str) -> None:
    """

    :param city_to_plot:
    :return:
    """
    # creating wordcloud
    text = events_dict[city_to_plot]
    wordcloud = WordCloud(stopwords=CUSTOM_STOPWORDS, collocations=False,
                          background_color="white").generate(text)
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show(block=False)
    plt.pause(5)
    plt.close()


def build_and_show_mutiple_wordclouds(events_dict: Dict,
                                      list_of_cities_to_plot: List):
    """
    Show 4 subplots of wordclouds together
    Possible TODO: 2x2 plots & random color maps & img size

    :param events_dict:
    :param list_of_cities_to_plot:
    :return:
    """

    fig, axs = plt.subplots(2, 2, figsize=(10, 5))

    for ax, city in zip(axs.reshape(-1), list_of_cities_to_plot):
        text = events_dict[city]
        wordcloud = WordCloud(stopwords=CUSTOM_STOPWORDS, collocations=False,
                              background_color="white", max_words = 40).generate(text)
        ax.imshow(wordcloud, interpolation="bilinear")
        # ax.set_aspect(2)
        ax.set_title(city.capitalize())
        ax.axis("off")
        ax.grid(True)

    plt.show()


def get_top_x_ngrams(events_dict: Dict, top_x: int, city_to_plot: str, most_common_x: int) -> None:
    """

    :param top_x:
    :param city_to_plot:
    :return:
    """
    # prepare nltk for usage
    _nltk_prep()
    # Further nltk prep
    words_per_city = events_dict[city_to_plot]
    tokens = nltk.word_tokenize(words_per_city)
    # Remove punctuation
    tokens = [word.lower() for word in tokens if word.isalpha()]
    # Remove stopwords
    filtered_words = [word for word in tokens if word not in stopwords.words('english')]
    created_ngrams = ngrams(filtered_words, top_x)
    # Count the occurences of most common ngrams
    most_common_counts = Counter(created_ngrams).most_common(most_common_x)
    for count in most_common_counts:
        logger.info("Most common combinations %s for %s", count, city_to_plot)


if __name__ == "__main__":
    with open("../data/events_dict.pickle", "rb") as handle:
        events_dict_from_disk = pickle.load(handle)

    # build_and_show_wordcloud(events_dict_from_disk, city_to_plot="Hamburg")

    # get_top_x_ngrams(events_dict_from_disk, top_x=2, city_to_plot="Hamburg", most_common_x=20)

    build_and_show_mutiple_wordclouds(events_dict_from_disk, ["Karlsruhe",
                                                              "Berlin",
                                                              "Hamburg",
                                                              "Munich"])
