import json

import scrapy
from scrapy_playwright.page import PageMethod
from ..items import ImageItem




class PicturesSpider(scrapy.Spider):
    name = 'pictures'
    allowed_domains = ['www.tradeinn.com']
    start_urls = ['http://www.tradeinn.com/']

    def __init__(self):
        self.start_urls = self.load_links_from_json()

    def start_requests(self):

        for link in self.start_urls:
            for i in range(1,4):
                if i == 1:
                    yield scrapy.Request(url=link, callback=self.parse)
                else:
                    decomposed_link = link.split('/')
                    # add to fifth element _2/_3
                    decomposed_link[5] = decomposed_link[5] + f'_{i}'
                    new_link = '/'.join(decomposed_link)
                    yield scrapy.Request(url=new_link, callback=self.parse)



    def parse(self, response):
        item = ImageItem()
        item['image_name'] = response.url.split('/')[-1].replace(".jpg", "") + response.url.split('/')[5] + ".jpg"
        item['image_urls'] = [response.url]
        yield item

    def load_links_from_json(self, file="road_shoes.json"):
        links = []
        with open(file, 'r') as f:
            data = json.load(f)
            for item in data:
                links.append(item['picture'])
        return links
