import requests
from bs4 import BeautifulSoup

from models import Product


def get_products():

    url = "https://www.smyk.com/ro/ro/brand/hot-wheels"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")

    cards = soup.find_all("a", class_="complex-product__link-wrapper")

    products = []

    for card in cards:

        name = card.find("div", class_="complex-product__name")
        price = card.find("span", class_="price--new")
        link = card.get("href")

        if name and price and link:

            products.append(
                Product(
                    name=name.get_text(strip=True),
                    price=price.get_text(strip=True),
                    url="https://www.smyk.com" + link,
                    store="SMYK"
                )
            )

    return products