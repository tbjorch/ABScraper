# standard library
from datetime import datetime
from time import sleep
import logging

# internal modules
from service import threader, sitemap_scraper
from repository import url_repo

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level="INFO")


def start_service():
    logging.info("Starting scraper service")
    while True:
        now = datetime.now()
        if now.minute % 1 == 0:
            logging.info("Starting sitemap scraper")
            sitemap_scraper.start(f"{now:%Y%m}")
            unscraped_urls = url_repo.get_unscraped_urls()
            if len(unscraped_urls) > 0:
                logging.info(
                    "Starting content scraper to scrape %s articles"
                    % len(unscraped_urls)
                )
                threader.start_scraper(20)
        sleep(60)

