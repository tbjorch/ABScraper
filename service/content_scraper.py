# standard library
from datetime import datetime
from threading import Lock
import logging

# 3p
import requests
from bs4 import BeautifulSoup

# Internal modules
from dto import ArticleDTO, UrlDTO
from repository import article_repo, url_repo
from service.error import UnwantedArticleException

db_lock = Lock()


def _create_html_soup_object(url: str) -> BeautifulSoup:
    try:
        page = requests.get(url, timeout=3)
        soup = BeautifulSoup(page.content, "html.parser")
        return soup
    except Exception as e:
        logging.error("during get call to url %s" % url)
        logging.error(e)


def _get_news_headline(soup: BeautifulSoup) -> str:
    try:
        headline = soup.find("h1", {"data-test-id": "headline"}).get_text()
    except Exception as e:
        raise e
    return headline


def _get_news_body_text(soup: BeautifulSoup) -> str:
    news_text = ""
    # news body text at p classes c-Cz1 _2ZkCB
    try:
        paragraph_list = soup.find_all("p", class_="c-Cz1") + soup.find_all(
            "p", class_="_2ZkCB"
        )
        for paragraph in paragraph_list:
            if (
                paragraph.find(class_="abBlueLink")
                or paragraph.find(class_="abSymbPi")
                or paragraph.get_text()
                == "Denna text är skapad av Aftonbladets textrobot"
            ):
                continue
            else:
                news_text += paragraph.get_text() + " "
    except Exception as e:
        raise e
    return news_text


def _assert_not_payed_content(soup: BeautifulSoup) -> None:
    sportbladet_paywall = soup.find(
        style="background-image:url(//wwwe.aftonbladet.se/ab-se/hyperion/gfx/logo-sportbladet-plus-2019.svg)"
    )
    aftonbladet_paywall = soup.find(
        style="background-image:url(//wwwe.aftonbladet.se/ab-se/hyperion/gfx/logo-aftonbladet-plus-2019.svg)"
    )
    if aftonbladet_paywall or sportbladet_paywall:
        raise UnwantedArticleException()


def get_news_content(url_dto: UrlDTO) -> None:
    soup: BeautifulSoup = _create_html_soup_object(url_dto.url)
    try:
        _assert_not_payed_content(soup)
        headline = _get_news_headline(soup)
        body = _get_news_body_text(soup)
        article = ArticleDTO(id=url_dto.id, headline=headline, body=body)
        with db_lock:
            article_repo.insert_article(article)
            url_dto.scraped_at = datetime.now()
            url_repo.update_url(url_dto)
    except UnwantedArticleException:
        url_dto.payed_content = True
        with db_lock:
            url_repo.update_url(url_dto)
        logging.warning(
            "Payed content article does not allow complete scraping of %s" % url_dto.url
        )
    except Exception as e:
        logging.error("when scraping article %s: %s" % (url_dto.url, e))

