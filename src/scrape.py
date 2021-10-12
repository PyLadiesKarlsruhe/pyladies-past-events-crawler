"""
The scraper module. Responsible for getting all the information of the Meetup site
using requests and BeautifulSoup

Some relevant links about beautiful soup and word clouds:
https://teracrawler.io/blog/scraping-meetup-events-with-python-and-beautiful.php
https://realpython.com/beautiful-soup-web-scraper-python/#explore-the-website
https://www.analyticsvidhya.com/blog/2021/05/how-to-build-word-cloud-in-python/

Possible future extension:
for getting more events, we would have to use selenium, see
https://stackoverflow.com/questions/21006940/how-to-load-all-entries-in-an-infinite-scroll-at-once-to-parse-the-html-in-python
"""
from typing import Dict
import logging
import pickle
import requests
from bs4 import BeautifulSoup

from utils.get_logger import get_logger

logger: logging.Logger = get_logger()


URL_BERLIN = "https://www.meetup.com/de-DE/PyLadies-Berlin/events/past/"
URL_HAMBURG = "https://www.meetup.com/de-DE/PyLadies-Hamburg/events/past/"
URL_KARLSRUHE = "https://www.meetup.com/de-DE/PyLadies-Karlsruhe/events/past/"
URL_MUNICH = "https://www.meetup.com/de-DE/PyLadiesMunich/events/past/"
BASE_URL = "https://www.meetup.com/"


def get_event_texts(group_name: str,
                    url: str, headers: Dict) -> str:
    """
    Get texts (consisting of title + description) of the first meetup events
    listed in url

    :param url: str containing the url to scrape
        (pointing to past events of the respective Meetup group)
    :param headers: headers needed for the request
    :return:
    """
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "lxml")
    text_str = ""
    for item in soup.select(".eventCard--link"):
        title = item.text
        logger.info("%s organized %s", group_name, title)
        text_str += " " + title
        event_url = item.attrs["href"]
        event_response = requests.get(BASE_URL + event_url, headers=headers)
        event_soup = BeautifulSoup(event_response.content, "lxml")
        try:
            event_description = event_soup.select(".event-description")[0].text
            text_str += " " + event_description
        except:
            logger.warning(event_soup.select(".event-description"))
    return text_str


def get_events_dict() -> Dict:
    """
    Gets the events text per meetup group and saves them to a dictionary
    """
    events_dict = {}
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) "
                      "AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9"
    }

    for group_name, url in zip(
            ["Berlin", "Hamburg", "Karlsruhe", "Munich"],
            [URL_BERLIN, URL_HAMBURG, URL_KARLSRUHE, URL_MUNICH],
    ):
        events_dict[group_name] = get_event_texts(group_name, url, headers)

    return events_dict


def main() -> None:
    """
    Get the events dictionary and save it on local disk
    """
    events_dict = get_events_dict()
    # saving and loading
    with open("../data/events_dict.pickle", "wb") as handle:
        pickle.dump(events_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)


if __name__ == "__main__":
    main()
