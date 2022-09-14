import json

import scrapy
from ..items import Immoscout24Item
from scrapy.loader import ItemLoader

BASE_URL = "http://www.immobilienscout24.at"


class RealestateSpider(scrapy.Spider):
    name = 'realestate'
    allowed_domains = ['www.immobilienscout24.at']
    start_urls = ['https://www.immobilienscout24.at/regional/wien/wien/wohnung-mieten']

    def parse(self, response):

        # extract script from html and formatting -> not executing via browser to speed it up
        raw_script = response.css("script::text").get().replace("window.__INITIAL_STATE__=", "")
        script_body = raw_script.split("\nwindow")[0]

        # raw json data
        realestate_data = json.loads(script_body)
        properties = realestate_data["reduxAsyncConnect"]["pageData"]["results"]["hits"]

        item = Immoscout24Item
        for property in properties:
            l = ItemLoader(item=Immoscout24Item(), selector=property)

            l.add_value("full_address", property["addressString"])
            l.add_value("price", property["priceKeyFacts"])
            l.add_value("description", property["headline"])
            l.add_value("labels", property)
            l.add_value("property_link", BASE_URL + property["links"]["targetURL"])
            l.add_value("contact", property["realtorContact"]["name"])
            l.add_value("company", property)
            l.add_value("rooms", property)
            l.add_value("area", property)

            yield l.load_item()

        next_page = BASE_URL + realestate_data["reduxAsyncConnect"]["pageData"]["results"]["pagination"]["nextURL"]
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
