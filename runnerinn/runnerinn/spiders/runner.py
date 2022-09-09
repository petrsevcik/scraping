import scrapy


class RunnerSpider(scrapy.Spider):
    name = 'runner'
    allowed_domains = ['tradeinn.com']
    start_urls = ['https://www.tradeinn.com/runnerinn/en/mens-shoes/10002/f']

    # https://www.tradeinn.com/runnerinn/en/mens-shoes/10002/f - shoes

    def parse(self, response):
        for link in response.css("a.enlace_img::attr(href)"):
            yield response.follow(link.get(), callback=self.parse_categories)

    def parse_categories(self, response):
        # category?
        shoes_info = response.css("h3.BoxPriceName")
        for shoes in shoes_info:
            yield {
                "name": shoes.css("a::text").get().strip(),
                "link": shoes.css("a::attr(href)").get()
            }




