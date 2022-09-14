import scrapy
from itemloaders.processors import MapCompose


def process_price(price_array):
    price = price_array.get("value", "not specified")
    if price[:2] == "ab":
        price = price.replace("ab", "from")
    return price


def process_labels(raw_data):
    labels_array = raw_data["badges"]
    return [x["value"] for x in labels_array]


def process_company(raw_data):
    try:
        company = raw_data["realtorContact"]["company"]
    except KeyError:
        company = "private"
    return company


def process_rooms(raw_data):
    key_facts_array = raw_data["mainKeyFacts"]
    for fact in key_facts_array:
        if fact["label"] == "Zimmer":
            return fact.get("value", "not specified")
    return "error"


def process_area(raw_data):
    key_facts_array = raw_data["mainKeyFacts"]
    for fact in key_facts_array:
        if fact["label"] == "Fläche":
            return fact.get("value", "not specified")
    return "error"


class Immoscout24Item(scrapy.Item):
    full_address = scrapy.Field()
    labels = scrapy.Field(input_processor=MapCompose(process_labels))
    description = scrapy.Field()
    property_link = scrapy.Field()
    rooms = scrapy.Field(input_processor=MapCompose(process_rooms))
    area = scrapy.Field(input_processor=MapCompose(process_area))
    price = scrapy.Field(input_processor=MapCompose(process_price))
    contact = scrapy.Field()
    company = scrapy.Field(input_processor=MapCompose(process_company))
