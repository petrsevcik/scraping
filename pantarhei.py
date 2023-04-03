import logging
import json
import csv
import os

import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
}


def test_save_page(page_name, html_page):
    with open(f'{page_name}.html', 'w') as f:
        f.write(html_page)


def get_subcategories():
    r = requests.get("https://www.pantarhei.sk/", headers=HEADERS)
    logging.info(f"Status code: {r.status_code}")

    soup = BeautifulSoup(r.text, 'html.parser')

    subcategories = {}
    dropdown_menu = soup.find('div', class_='row px-md-0')
    _subcategories = dropdown_menu.find_all('div', class_='cat-wrap col-md-3 col-xl-3 mt-4 mb-0')
    logging.info(f"Found {len(_subcategories)} subcategories")
    count = 0
    for sub in _subcategories:
        subcategory = sub.find('h3')
        subcategory_name = subcategory.text.strip()
        link = subcategory.find('a').get('href')
        subcategories[count] = {"name": subcategory_name, "link": link}
        count += 1
    logging.info(f"Subcategories: {json.dumps(subcategories, indent=4)}")
    return subcategories


def get_book_links_from_category(category_link, pages=5):
    for i in range(1, pages):
        logging.info(f"Getting book links from page: {i}")
        category_link = f"{category_link}?p={i}"
        r = requests.get(category_link, headers=HEADERS)
        logging.info(f"Status code: {r.status_code}")
        soup = BeautifulSoup(r.text, 'html.parser')
        books = soup.find_all('a', class_='title')
        book_links = [book.get('href') for book in books]
        logging.info(f"Found {len(book_links)} book links")
        yield book_links


def get_book_details(book_link, subcategory=None):
    r = requests.get(book_link, headers=HEADERS)
    logging.info(f"Status code: {r.status_code}")
    soup = BeautifulSoup(r.text, 'html.parser')

    try:
        title = soup.find('h1').text.strip()
    except:
        title = None
    logging.info(f"Book title: {title}")


    subtitle = None
    logging.info(f"No book subtitle on Pantarhei.sk")

    try:
        author = soup.find('a', class_='author').text.strip()
        author_url = soup.find('a', class_='author').get('href')
    except:
        author = None
        author_url = None
    logging.info(f"Book author: {author}")
    logging.info(f"Book author link: {author_url}")

    try:
        price = float(soup.find('div', class_='text-primary').text.strip().replace(',', '.').replace('€', ''))
    except:
        price = None
    logging.info(f"Book price: {price}")

    try:
        description = soup.find('div', class_='product-text short').text.strip()
    except:
        description = None
    # logging.info(f"Book details: {json.dumps(book_details, indent=4)}")

    try:
        raw_details = soup.find('ul', class_='list-info')
        details = _get_details(raw_details)
    except:
        details = None

    try:
        isbn = _get_isbn(details)
    except:
        isbn = None
    logging.info(f"Book isbn: {isbn}")

    details = {
        "description": description,
        "details": details
    }

    book_details = {
        "title": title,
        "subtitle": subtitle,
        "book_url": book_link,
        "author": author,
        "author_url": author_url,
        "price": price,
        "isbn": isbn,
        "shop": "Pantarhei.sk",
        "category": subcategory,
        "details": details
    }
    logging.info(f"Book details: {json.dumps(book_details, indent=4)}")
    return book_details


def _format_price(price_string):
    # 16,40&nbsp;€ -> 16.40
    price_string = price_string.replace(',', '.')
    price_string = price_string.replace('&nbsp;', '')
    price_string = price_string.replace('€', '')
    try:
        price_string = float(price_string)
    except:
        logging.info(f"Price {price_string} is not a float number")
    return price_string


def _get_details(card_content):
    content = {}
    fields = card_content.find_all('li')
    # example element "<li class="row no-gutters"><strong class="col-auto">Počet strán:</strong> 248</li>"
    # key is text before '<strong>' tag, value is text after 'strong>'
    for i, field in enumerate(fields):
        key = field.find('strong').text.replace(':', '').strip()
        value = field.text.replace(key, '').strip()
        content[i] = {"name": key, "value": value}
    return content


def _get_isbn(card_content):
    isbn = None
    for detail in card_content.values():
        if detail['name'] == 'ISBN':
            isbn = detail['value'].replace('-', '')
            break
    return isbn

def save_book_to_csv(book_details: dict, filename: str = 'pantarhei_books.csv'):
    if not os.path.exists(filename):
        with open('pantarhei_books.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(book_details.keys())

    with open('pantarhei_books.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(book_details.values())
        logging.info(f"Saved book to csv: {book_details['title']}")


def scrape():
    sub = get_subcategories()
    for subcategory in sub.values():
        subcategory_name = subcategory['name']
        book_links = get_book_links_from_category(subcategory['link'])
        for item in book_links:
            for book_link in item:
                book_details = get_book_details(book_link, subcategory_name)
                save_book_to_csv(book_details)


if __name__ == '__main__':
    scrape()
