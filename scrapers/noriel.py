import requests
from bs4 import BeautifulSoup

from models import Product


BASE_URL = "https://noriel.ro/catalogsearch/result/?q=hot+wheels"


def get_products() -> list[Product]:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/150.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "ro-RO,ro;q=0.9,en;q=0.8",
    }

    all_products = []
    seen_urls = set()
    page_number = 1

    while True:
        page_url = f"{BASE_URL}&p={page_number}"

        print(f"Checking Noriel page {page_number}...")

        response = requests.get(
            page_url,
            headers=headers,
            timeout=30,
        )

        print(f"Noriel status code: {response.status_code}")
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        cards = soup.select("a:has(h2.product-item-name)")
        page_products = []

        for card in cards:
            name_element = card.select_one("h2.product-item-name")
            price_element = card.select_one("span.price")
            url = card.get("href")

            if not name_element or not price_element or not url:
                continue

            if url in seen_urls:
                continue

            product = Product(
                name=name_element.get_text(" ", strip=True),
                price=price_element.get_text(" ", strip=True),
                url=url,
                store="NORIEL",
            )

            page_products.append(product)
            seen_urls.add(url)

        if not page_products:
            print(
                f"No new Noriel products found on page "
                f"{page_number}. Stopping."
            )
            break

        print(
            f"Found {len(page_products)} Noriel products "
            f"on page {page_number}."
        )

        all_products.extend(page_products)
        page_number += 1

    print(f"Found {len(all_products)} Noriel products in total.")

    return all_products