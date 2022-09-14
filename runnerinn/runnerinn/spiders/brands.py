import json

import scrapy


class BrandsSpider(scrapy.Spider):
    name = 'brands'
    allowed_domains = ['www.tradeinn.com']
    start_urls = ['https://www.tradeinn.com/index.php?action=get_marcas_buscador&idioma=eng&id_tienda=10']
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",

    def parse(self, response):
        data = json.loads(response.body)
        for brand in data:
            yield {
                "brand_id": brand["id_marca"],
                "brand_name": brand["marca"]
            }


