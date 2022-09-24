# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem

class RunnerinnPipeline:
    def process_item(self, item, spider):
        return item

class CustomImagesPipeline(ImagesPipeline):

    def file_path(self, request, response=None, info=None, *, item=None):
        image_name = item.get('image_name')
        return f'full/{image_name}'