import requests
from bs4 import BeautifulSoup

from models import Product


SMYK_SOURCES = [
    {
        "name": "Hot Wheels",
        "url": "https://www.smyk.com/ro/ro/brand/hot-wheels",
    },
    {
        "name": "Pokemon",
        "url": "https://www.smyk.com/ro/ro/personaj/pokemon",
    },
]


def scrape_source(source_name: str, base_url: str) -> list[Product]:
    all_products = []
    seen_urls = set()
    page_number = 1

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    while True:
        page_url = f"{base_url}?p={page_number}"

        print(
            f"Checking SMYK {source_name} "
            f"page {page_number}..."
        )

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

            if link.startswith("http"):
                full_url = link
            else:
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
            print(
                f"No new SMYK {source_name} products "
                f"found on page {page_number}. Stopping."
            )
            break

        print(
            f"Found {len(page_products)} SMYK "
            f"{source_name} products on page {page_number}."
        )

        all_products.extend(page_products)
        page_number += 1

    print(
        f"Found {len(all_products)} SMYK "
        f"{source_name} products in total."
    )

    return all_products


def get_products() -> list[Product]:
    all_products = []
    global_seen_urls = set()

    for source in SMYK_SOURCES:
        products = scrape_source(
            source["name"],
            source["url"],
        )

        for product in products:
            if product.url not in global_seen_urls:
                all_products.append(product)
                global_seen_urls.add(product.url)

    print(
        f"Found {len(all_products)} SMYK products "
        f"across all monitored categories."
    )

    return all_products