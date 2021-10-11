"""
The text visualization module. Builds wordcloud from the scraped dict of the meetup site
Might be extended by other visualizations
"""
import pickle
from matplotlib import pyplot as plt
from wordcloud import WordCloud, STOPWORDS


def build_and_show_wordcloud(city_to_plot: str):
    """

    :param city_to_plot:
    :return:
    """
    with open("../data/events_dict.pickle", "rb") as handle:
        events_dict = pickle.load(handle)

    # creating wordcloud
    text = events_dict[city_to_plot]
    stopwords_extended = ["PyLadies", "Python", "will",
                          "Meetup", "https", "event",
                          "Berlin", "Karlsruhe", "Munich", "Hamburg"] + list(STOPWORDS)
    wordcloud = WordCloud(stopwords=stopwords_extended,
        collocations=False, background_color="white").generate(text)
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()


if __name__ == "__main__":
    build_and_show_wordcloud("Karlsruhe")