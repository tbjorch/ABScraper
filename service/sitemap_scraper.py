# standard library
from datetime import datetime
import logging


# 3rd party modules
import requests
from bs4 import BeautifulSoup

# internal modules
from dto import AddUrlDTO
from repository import url_repo
from service.error import UnwantedArticleException


def get_news_urls_from_sitemap(date: str):
    sitemap_url: str = "https://www.aftonbladet.se/sitemaps/files/" + date + "-articles.xml"
    soup = _create_xml_soup_object(sitemap_url)
    value_list = []
    # find all loc tags and extract the news url value into a list
    for item in soup.find_all("loc"):
        try:
            add_url_dto = AddUrlDTO(
                id=item.get_text().split("/")[
                    item.get_text().split("/").index("a") + 1
                ],
                url=item.get_text(),
                yearmonth=date,
                undesired_url=False,
            )
            add_url_dto = _check_if_undesired_url(add_url_dto)
            value_list.append(add_url_dto)
        except UnwantedArticleException as e:
            logging.warning(e)
        except Exception as e:
            logging.error("when scraping sitemap for url %s" % item.get_text())
    return value_list


def start(date):
    url_list = get_news_urls_from_sitemap(date)
    counter = 0
    existing_news = url_repo.get_all_url_ids()
    for url in url_list:
        if (url.id,) not in existing_news:
            url_repo.insert_url(url)
            counter += 1
    logging.info("Inserted %s URLs to database" % counter)


def _check_if_undesired_url(add_url_dto: AddUrlDTO):
    undesired_urls = [
        "www.aftonbladet.se/autotest",
        "special.aftonbladet.se",
        "www.aftonbladet.se/nyheter/trafik",
        "www.aftonbladet.se/sportbladet"
    ]
    for string in undesired_urls:
        if string in add_url_dto.url:
            add_url_dto.undesired_url = True
    return add_url_dto


def _create_xml_soup_object(url: str) -> BeautifulSoup:
    page = requests.get(url, timeout=3)
    soup = BeautifulSoup(page.content, "lxml")
    return soup


#if __name__ == "__main__":
    # date = input("Input date in YYYYMM format: ")
    # start(date)