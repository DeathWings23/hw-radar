import requests
from bs4 import BeautifulSoup

from models import Product


BASE_URL = "https://www.smyk.com/ro/ro/brand/hot-wheels"


def get_products() -> list[Product]:
    all_products = []
    seen_urls = set()
    page_number = 1

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    while True:
        page_url = f"{BASE_URL}?p={page_number}"

        print(f"Checking SMYK page {page_number}...")

        response = requests.get(
            page_url,
            headers=headers,
            timeout=20,
        )

        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        cards = soup.find_all(
            "a",
            class_="complex-product__link-wrapper",
        )

        page_products = []

        for card in cards:
            name = card.find(
                "div",
                class_="complex-product__name",
            )
            price = card.find(
                "span",
                class_="price--new",
            )
            link = card.get("href")

            if not name or not price or not link:
                continue

            full_url = "https://www.smyk.com" + link

            if full_url in seen_urls:
                continue

            product = Product(
                name=name.get_text(strip=True),
                price=price.get_text(" ", strip=True),
                url=full_url,
                store="SMYK",
            )

            page_products.append(product)
            seen_urls.add(full_url)

        if not page_products:
            print(f"No new products found on page {page_number}. Stopping.")
            break

        print(f"Found {len(page_products)} products on page {page_number}.")

        all_products.extend(page_products)
        page_number += 1

    return all_products