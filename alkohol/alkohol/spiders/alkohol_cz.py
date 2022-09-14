import scrapy

BASE_URL = "https://www.alkohol.cz"


class GetDrunk(scrapy.Spider):
    name = "alkohol"
    start_urls = ["https://www.alkohol.cz/produkty/whisky/kategorie/"]

    def format_price(self, raw_price):
        if not raw_price:
            return 0
        price = ""
        for el in raw_price:
            if el.isdigit(): # tmp solution
                price += el
        return int(price)

    def parse(self, response):
        product_box = response.css("div.products-box")
        products = product_box.css("div.info")

        for product in products:
            name = product.css("a.link-color::text").get().strip()
            link = BASE_URL + product.css("a.link-color::attr(href)").get()
            price_text = product.css("span.price::text")
            if len(price_text) > 2:  # bottle in sale
                raw_price = product.css("span.price::text")[1].get().strip()
                price = self.format_price(raw_price)
                sale = True
            else:
                raw_price = product.css("span.price::text").get().strip()
                price = self.format_price(raw_price)
                sale = False
            item = {
                "name": name,
                "price": price,
                "sale": sale,
                "link": link
            }
            yield item

        next_page = BASE_URL + response.css("a.noAjaxHistory.link.paging-button.paging-button-last::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)


