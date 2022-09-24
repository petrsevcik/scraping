# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from scrapy import Field
from scrapy import Item


class RunnerinnItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class ImageItem(Item):
    image_name = Field()
    image_urls = Field()
    images = Field()