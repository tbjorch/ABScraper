# standard library
from datetime import datetime

# 3rd party modules
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Column,
    String,
    DateTime,
    Text,
    Boolean,
    create_engine,
    ForeignKey,
)
from sqlalchemy.orm import relationship, sessionmaker


Base = declarative_base()


class Url(Base):  # type: ignore
    __tablename__ = "Urls"
    id: str = Column(String(6), primary_key=True)
    url: str = Column(String(200), nullable=False, unique=True)
    yearmonth: str = Column(String(6), nullable=False)
    payed_content: bool = Column(Boolean, nullable=False, default=False)
    undesired_url: bool = Column(Boolean, nullable=False, default=False)
    scraped_at: datetime = Column(DateTime, nullable=True)
    created_at: datetime = Column(DateTime, nullable=False, default=datetime.utcnow)
    article = relationship("Article", uselist=False)

    def __repr__(self) -> str:
        return (
            f"Url(id={self.id} "
            f"url={self.url} "
            f"yearmonth={self.yearmonth} "
            f"payed_content={self.payed_content} "
            f"undesired_url={self.undesired_url} "
            f"scraped_at={self.scraped_at} "
            f"created_at={self.created_at})"
        )


class Article(Base):  # type: ignore
    __tablename__ = "Articles"
    id: str = Column(String(6), ForeignKey("Urls.id"), primary_key=True)
    headline: str = Column(String(300), nullable=False)
    body: str = Column(Text, nullable=False)
    created_at: datetime = Column(DateTime, nullable=False, default=datetime.utcnow)


# engine = create_engine("sqlite:///:memory:", echo=True)
engine = create_engine("postgresql://root:asd123@localhost:5432/newsdata")
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
