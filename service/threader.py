# builtin packages
import threading
from queue import Queue
from datetime import datetime
from time import sleep
import logging

# 3P packages
import requests

# local modules
from service import content_scraper
from repository import url_repo


db_lock = threading.Lock()


def scraper_thread():
    while True:
        url = scrape_q.get()
        logging.debug("scraping %s" % url.url)
        content_scraper.get_news_content(url)
        scrape_q.task_done()


def set_scrape_queue():
    global scrape_q
    scrape_q = Queue()
    url_list = url_repo.get_unscraped_urls()
    for url in url_list:
        scrape_q.put(url)


def start_scraper(num_of_threads):
    set_scrape_queue()
    for x in range(num_of_threads):
        t = threading.Thread(target=scraper_thread)
        t.daemon = True
        t.start()
    scrape_q.join()
