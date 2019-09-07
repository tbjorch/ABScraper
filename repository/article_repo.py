# Standard library
import logging

# internal modules
from dto import ArticleDTO
import models
from models import Session, Article


def insert_article(article_dto: ArticleDTO) -> None:
    try:
        session = Session()
        article = Article(
            id=article_dto.id, headline=article_dto.headline, body=article_dto.body
        )
        session.add(article)
        session.commit()
        session.close()
    except Exception as e:
        logging.error("when inserting row in article table: %s" % e)
