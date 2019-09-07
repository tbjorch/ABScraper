# Data Transfer Objects and support functions
# used to decouple the service modules from SQLAlchemy.
# The service doesn't know what interface is used with the database.
from datetime import datetime


class AddUrlDTO:
    def __init__(self, id: str, url: str, yearmonth: str, undesired_url: bool):
        self.id: str = id
        self.url: str = url
        self.yearmonth: str = yearmonth
        self.undesired_url: bool = undesired_url


class ArticleDTO:
    def __init__(self, id: str, headline: str, body: str):
        self.id: str = id
        self.headline: str = headline
        self.body: str = body


class UrlDTO:
    def __init__(
        self,
        id: str,
        url: str,
        yearmonth: str,
        payed_content: bool,
        undesired_url: bool,
        scraped_at: datetime,
        created_at: datetime,
    ):
        self.id: str = id
        self.url: str = url
        self.yearmonth: str = yearmonth
        self.payed_content: bool = payed_content
        self.undesired_url: bool = undesired_url
        self.scraped_at: datetime = scraped_at
        self.created_at: datetime = created_at

    def __repr__(self) -> str:
        return (
            f"News(id={self.id} "
            f"url={self.url} "
            f"yearmonth={self.yearmonth} "
            f"payed_content={self.payed_content} "
            f"undesired_url={self.undesired_url} "
            f"scraped_at={self.scraped_at} "
            f"created_at={self.created_at})"
        )

