import csv
import json
from datetime import time

from pprint import pprint

import requests

#TODO categories - men, women, trail, road
#TODO sample mode
#TODO brands
"""curl 'https://www.tradeinn.com/index.php?action=get_marcas_buscador&idioma=eng&id_tienda=10' \
  -X 'POST' \
  -H 'authority: www.tradeinn.com' \
  -H 'accept: application/json, text/javascript, */*; q=0.01' \
  -H 'accept-language: en-GB,en-US;q=0.9,en;q=0.8' \
  -H 'content-length: 0' \
  -H 'cookie: _ALGOLIA=anonymous-e8114e3f-82f9-480e-9759-e435cf851f5b; _fbp=fb.1.1660681167382.585918009; mail_cliente=petrsevcik93%40gmail.com; ga_uid_ras=11362081; up=4; user_name=petr; cid=%24argon2id%24v%3D19%24m%3D65536%2Ct%3D4%2Cp%3D1%24VXVDSEVvYVE3MEtvYXFIQg%24jL1ihMLhYXoSmzQb168dqn7CiUe%2BkfqzR9nHzPynZrE; ip=185.24.238.131; rurl=https://www.tradeinn.com/runnerinn/; OptanonAlertBoxClosed=2022-09-09T19:18:16.331Z; barra_cookies=1; _gcl_au=1.1.1279465505.1662751398; oneT=,C0001,C0002,C0003,C0004,C0005,; PHPSESSID=bt69m7g0mcfpa67b4ucog97st6; data_user=12-9-2022; _gid=GA1.2.110840479.1663011496; recommendation_products_last=10005; id_tienda=10; gclid_ds=undefined; usizy.sk=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzaWQiOiJhMDQ4OWIwODYzM2IxMWVjYWE1YWE2ZjQ4ZWE5MDMwZCIsInZAZSI6WzE4XX0.ytDTt5k2yg74ycodZJeFkV-VgJcHj5Ieyvce_-esHsg; id_pais=54; nrw=3; change_domain=0; recommendation_products={"10004":26,"10005":25,"10008":1,"10023":1,"10027":2,"10004_1312":1,"10004_284":10,"10004_365":3,"10005_1312":9,"10008_1312":1,"10005_482":1,"10027_365":1,"10005_365":1,"10005_1648":3,"10005_179":2}; OptanonConsent=isGpcEnabled=0&datestamp=Mon+Sep+12+2022+23%3A21%3A11+GMT%2B0200+(Central+European+Summer+Time)&version=6.32.0&isIABGlobal=false&hosts=&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1%2CC0005%3A1&AwaitingReconsent=false&geolocation=%3B; _ga_VS2KTMJQTJ=GS1.1.1663016080.3.1.1663017671.58.0.0; _ga=GA1.1.1723782809.1660850163; _dc_gtm_UA-17685316-2=1' \
  -H 'origin: https://www.tradeinn.com' \
  -H 'referer: https://www.tradeinn.com/runnerinn/en/mens-shoes/10002/f' \
  -H 'sec-ch-ua: "Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "macOS"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-origin' \
  -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36' \
  -H 'x-requested-with: XMLHttpRequest' \
  --compressed"""

class RunnerInnScraper:

    url = 'https://www.tradeinn.com/index.php'

    headers = {
        #'authority': 'www.tradeinn.com',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://www.tradeinn.com',
        'referer': 'https://www.tradeinn.com/runnerinn/en/mens-shoes-trail-running-shoes/10005/s',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    params = {
        'action': 'get_info_elastic_listado',
        'id_tienda': '10',
        'idioma': 'eng',
    }

    data = {
        'vars[]': [
            'id_familia=10002',
            'atributos_e=5091,6017',
            'model.eng;model.eng;video_mp4;id_marca;precio_tachado;sostenible;productes.talla2;productes.talla_usa;productes.talla_jp;productes.talla_uk;tres_sesenta;atributos_padre.atributos.id_atribut_valor;productes.v360;productes.v180;productes.v90;productes.v30;productes.exist;productes.stock_reservat;productes.pmp;productes.id_producte;productes.color;productes.referencia;productes.brut;productes.desc_brand;image_created;id_modelo;familias.eng;familias.eng;familias.id_familia;familias.subfamilias.eng;familias.subfamilias.eng;familias.subfamilias.id_tienda;familias.subfamilias.id_subfamilia;productes.talla;productes.baja;productes.rec;precio_win_209;productes.sellers.id_seller;productes.sellers.precios_paises.precio;productes.sellers.precios_paises.id_pais;fecha_descatalogado;marca;productes.talla_uk',
            'v30_sum;desc@tm10;asc',
            '1500',
            'productos',
            'search',
            'id_subfamilia=10005',
            '96',
        ],
        'texto_search': '',
    }

    def get_category(self):  # TODO category
        response = requests.post(url=self.url, params=self.params, headers=self.headers, data=self.data)
        return response.json()

    def parse_data(self, json_response):
        data = []
        columns = ["model", "brand", "availability"]
        data.append(columns)
        shoes_list = json_response["id_modelos"]
        for shoes in shoes_list:
            brand = shoes.get("marca")
            model = shoes.get("nombre_modelo")
            all_sizes = shoes.get("productes")
            availability = []
            for item in all_sizes:
                size = item["talla"]
                color = item["color"]
                price = item.get("sellers")
                if price:
                    price = price[0]["precio_producte"]
                else:
                    price = 0
                size_to_price_color = {"size": size,
                                       "color": color,
                                       "price": price}
                availability.append(size_to_price_color)
            data.append([model, brand, availability])
        return data

    def write_to_csv(self, data):
        with open("data.csv", "a") as file:
            writer = csv.writer(file)
            writer.writerows(data)
            print("Data saved to csv!")
        return True



if __name__ == '__main__':
    scraper = RunnerInnScraper()
    data = scraper.get_category()
    shoes = scraper.parse_data(data)
    scraper.write_to_csv(shoes)

