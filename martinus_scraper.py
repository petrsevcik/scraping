from datetime import datetime
import json
import logging

import scrapy
from scrapy.crawler import CrawlerProcess

# from database import upload_data_to_db # for later use

BASE_URL = 'https://www.lindex.com/'


class IamYourSpider(scrapy.spiders.CrawlSpider):
    name = "spidermans_spider"
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    headers = {
        'authority': 'www.lindex.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-GB,en;q=0.9',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
    }

    def start_requests(self):
        url = "https://www.l.com/uk"
        yield scrapy.Request(url=url, headers=self.headers, callback=self.parse)

    def parse(self, response):
        pass


if __name__ == "__main__":
    date_now = datetime.now().strftime("%d_%m_%Y_%H_%M")
    filename = f'{date_now}_file.csv'
    process = CrawlerProcess(settings={
        'FEED_URI': filename,
        'FEED_FORMAT': 'csv'
    })
    process.crawl(IamYourSpider)
    process.start()

    # upload_data_to_db(filename)
