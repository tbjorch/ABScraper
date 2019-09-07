# Standard library
import logging

# 3rd party modules
from sqlalchemy import update

# Internal modules
import models
from models import Session, Url, Article
from dto import AddUrlDTO, UrlDTO


def insert_url(add_url_dto: AddUrlDTO) -> None:
    try:
        url = Url(
            id=add_url_dto.id,
            url=add_url_dto.url,
            yearmonth=add_url_dto.yearmonth,
            undesired_url=add_url_dto.undesired_url,
        )
        session = Session()
        session.add(url)
        session.commit()
        session.close()
    except Exception as e:
        logging.error("During inserting url to db: %s" % e)


def get_all_url_ids() -> []:
    session = Session()
    ids = session.query(Url.id).all()
    return ids


def get_unscraped_urls() -> []:
    session = Session()
    unscraped_urls = (
        session.query(Url)
        .filter(
            Url.scraped_at == None,
            Url.undesired_url == False,
            Url.payed_content == False,
        )
        .all()
    )
    url_list = []
    for url in unscraped_urls:
        url_list.append(_convert_to_url_dto(url))
    return url_list


def update_url(url_dto: UrlDTO) -> None:
    try:
        session = Session()
        url: Url = session.query(Url).filter(Url.id == url_dto.id).first()
        url.payed_content = url_dto.payed_content
        url.scraped_at = url_dto.scraped_at
        session.commit()
        session.close()
    except Exception as e:
        logging.error("When updating row in table Urls: %s" % e)


def _convert_to_url_dto(url: Url) -> UrlDTO:
    return UrlDTO(
        id=url.id,
        url=url.url,
        yearmonth=url.yearmonth,
        payed_content=url.payed_content,
        undesired_url=url.undesired_url,
        scraped_at=url.scraped_at,
        created_at=url.created_at,
    )
