from bs4 import BeautifulSoup
import requests
import pickle
from wordcloud import WordCloud
from matplotlib import pyplot as plt

# Some relevant links about beautiful soup and word clouds:
# https://teracrawler.io/blog/scraping-meetup-events-with-python-and-beautiful.php
# https://realpython.com/beautiful-soup-web-scraper-python/#explore-the-website
# https://www.analyticsvidhya.com/blog/2021/05/how-to-build-word-cloud-in-python/

# for getting more events, we would have to use selenium, see
# https://stackoverflow.com/questions/21006940/how-to-load-all-entries-in-an-infinite-scroll-at-once-to-parse-the-html-in-pytho

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9"
}
url_berlin = "https://www.meetup.com/de-DE/PyLadies-Berlin/events/past/"
url_hamburg = "https://www.meetup.com/de-DE/PyLadies-Hamburg/events/past/"
url_karlsruhe = "https://www.meetup.com/de-DE/PyLadies-Karlsruhe/events/past/"
url_munich = "https://www.meetup.com/de-DE/PyLadiesMunich/events/past/"
base_url = "https://www.meetup.com/"


def get_event_texts(url):
    """Get texts (consisting of title + description) of the first meetup events
    listed in url"""
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "lxml")
    text_str = ""
    for item in soup.select(".eventCard--link"):
        title = item.text
        print(title)
        text_str += " " + title
        event_url = item.attrs["href"]
        event_response = requests.get(base_url + event_url, headers=headers)
        event_soup = BeautifulSoup(event_response.content, "lxml")
        try:
            event_description = event_soup.select(".event-description")[0].text
            text_str += " " + event_description
        except:
            print(event_soup.select(".event-description"))
    return text_str


events_dict = {}

for group_name, url in zip(
    ["berlin", "hamburg", "karlsruhe", "munich"],
    [url_berlin, url_hamburg, url_karlsruhe, url_munich],
):
    events_dict[group_name] = get_event_texts(url)

# print(events_dict)

# saving and loading
with open("events_dict.pickle", "wb") as handle:
    pickle.dump(events_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open("events_dict.pickle", "rb") as handle:
    events_dict = pickle.load(handle)


# creating wordcloud
text = events_dict["munich"]
wordcloud = WordCloud(collocations=False, background_color="white").generate(text)
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()
