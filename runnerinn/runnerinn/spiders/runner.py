import json

import scrapy


class RunnerSpider(scrapy.Spider):
    name = 'runner'
    allowed_domains = ['tradeinn.com']
    start_urls = ['https://www.tradeinn.com/runnerinn/en/mens-shoes/10002/f']

    CATEGORIES = {
        "trail": {"id_subfamilia": "10005"},
        "road": {"id_subfamilia": "10005"}
    }

    NO_OF_PRODUCTS = {
        "sample": "10",
        "standard": "48",
        "all": "1000",
        "custom": "48"
    }

    def __init__(self):
        self.category = "trail"
        self.no_of_producs = "all"
        self.brands = ""


    def start_requests(self):
        url = 'https://www.tradeinn.com/index.php?action=get_info_elastic_listado&id_tienda=10&idioma=eng'

        headers = {
            "authority": "www.tradeinn.com",
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "origin": "https://www.tradeinn.com",
            "referer": "https://www.tradeinn.com/runnerinn/en/mens-shoes-trail-running-shoes/10005/s",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
            "x-requested-with": "XMLHttpRequest"
        }

        body = f'vars%5B%5D=id_familia%3D10002&vars%5B%5D=atributos_e%3D5091%2C6017&vars%5B%5D=model.eng%3Bmodel.eng%3Bvideo_mp4%3Bid_marca%3Bprecio_tachado%3Bsostenible%3Bproductes.talla2%3Bproductes.talla_usa%3Bproductes.talla_jp%3Bproductes.talla_uk%3Btres_sesenta%3Batributos_padre.atributos.id_atribut_valor%3Bproductes.v360%3Bproductes.v180%3Bproductes.v90%3Bproductes.v30%3Bproductes.exist%3Bproductes.stock_reservat%3Bproductes.pmp%3Bproductes.id_producte%3Bproductes.color%3Bproductes.referencia%3Bproductes.brut%3Bproductes.desc_brand%3Bimage_created%3Bid_modelo%3Bfamilias.eng%3Bfamilias.eng%3Bfamilias.id_familia%3Bfamilias.subfamilias.eng%3Bfamilias.subfamilias.eng%3Bfamilias.subfamilias.id_tienda%3Bfamilias.subfamilias.id_subfamilia%3Bproductes.talla%3Bproductes.baja%3Bproductes.rec%3Bprecio_win_209%3Bproductes.sellers.id_seller%3Bproductes.sellers.precios_paises.precio%3Bproductes.sellers.precios_paises.id_pais%3Bfecha_descatalogado%3Bmarca%3Bproductes.talla_uk&vars%5B%5D=v30_sum%3Bdesc%40tm10%3Basc&vars%5B%5D=1448&vars%5B%5D=productos&vars%5B%5D=search&vars%5B%5D=id_subfamilia%3D10004&vars%5B%5D=96&texto_search='
        data = {
            'vars[]': [
                'id_familia=10002',
                'atributos_e=5091,6017',
                'model.eng;model.eng;video_mp4;id_marca;precio_tachado;sostenible;productes.talla2;productes.talla_usa;productes.talla_jp;productes.talla_uk;tres_sesenta;atributos_padre.atributos.id_atribut_valor;productes.v360;productes.v180;productes.v90;productes.v30;productes.exist;productes.stock_reservat;productes.pmp;productes.id_producte;productes.color;productes.referencia;productes.brut;productes.desc_brand;image_created;id_modelo;familias.eng;familias.eng;familias.id_familia;familias.subfamilias.eng;familias.subfamilias.eng;familias.subfamilias.id_tienda;familias.subfamilias.id_subfamilia;productes.talla;productes.baja;productes.rec;precio_win_209;productes.sellers.id_seller;productes.sellers.precios_paises.precio;productes.sellers.precios_paises.id_pais;fecha_descatalogado;marca;productes.talla_uk',
                'v30_sum;desc@tm10;asc',
                '48',
                'productos',
                'search',
                'id_subfamilia=10005',
                '96',
            ],
            'texto_search': '',
        }

        yield scrapy.http.Request(url=url, headers=headers, body=body, method="POST")

    # https://www.tradeinn.com/runnerinn/en/mens-shoes/10002/f - shoes

    def parse(self, response):
        data = json.loads(response.body)["id_modelos"]
        for item in data:
            model_brand = self.parse_shoes(item)
            yield model_brand


    @staticmethod
    def parse_shoes(data):
        brand = data.get("marca")
        model = data.get("nombre_modelo")
        model_id = data.get("id_modelo")
        picture = f"https://www.tradeinn.com/f/{model_id[:5]}/{model_id}/{brand}-{model}.jpg".replace(" ", "-")
        availability = RunnerSpider.parse_size_price_color(data)
        return {
            "brand": brand,
            "model": model,
            "picture": picture,
            "availability": availability
        }

    @staticmethod
    def parse_size_price_color(data):
        all_sizes = data.get("productes")
        availability = []
        for item in all_sizes:
            price = item.get("sellers")  # if not price -> sold out
            if price:
                price = price[0]["precio_producte"]
                in_stock = True
            else:
                price = 0
                in_stock = False

            size = item["talla"]
            color = item["color"]
            size_price_color = {"size": size,
                                "in_stock": in_stock,
                                "color": color,
                                "price": price}
            availability.append(size_price_color)
        return availability

    @staticmethod
    def get_brand_id(brand_name):
        #TODO doctrings
        brand_str = ""

        with open("../../brands.json") as file:
            brand_data = json.load(file)

        brands = brand_name.split(",")
        for i, brand in enumerate(brands):
            for item in brand_data:
                if brand.lower() == item["brand_name"]:
                    brand_id = item["brand_id"]
                    if i:
                        brand_str += f",{brand_id}"
                    else:
                        brand_str += brand_id
        return brand_str












