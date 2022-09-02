``product_box = response.css("div.products-box")
``

``
products = product_box.css("div.info") # element + .get()
``

```
name = item.css("a.link-color::text").get().strip()
link = item.css("a.link-color::attr(href)").get()
price = item.css("span.price::text")[1].get().strip()
```