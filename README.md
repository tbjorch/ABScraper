# ABScraper
Threaded scraper fetching news from Swedish news website Aftonbladet.

The scraper fetches news articles, transforms the data, and inserts it to a db using an ORM.

# Keywords
- Threading
- Web Scraping
- BeautifulSoup4
- Requests
- SqlAlchemy ORM

# Software Architecture
The architecture is layered using a service layer and a repo layer. The service contains all business logic to fetch the desired data from Aftonbladet. It then uses a python class representing e.g. an article as a DTO (data transfer object), which is used for integrating the layers with each other. The DTO sent to the repo layer which then translates it into an object that can be sent to the database for crud operations. This creates a modular software allowing for replacing or updating any of the layers without affecting the other layer. 
