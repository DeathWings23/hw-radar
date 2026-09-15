import requests
from bs4 import BeautifulSoup

from models import Product


NORIEL_SEARCHES = [
    {
        "name": "Hot Wheels",
        "query": "hot+wheels",
    },
    {
        "name": "Pokemon",
        "query": "pokemon",
    },
]


def scrape_search(search_name: str, query: str) -> list[Product]:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/150.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "ro-RO,ro;q=0.9,en;q=0.8",
    }

    base_url = (
        "https://noriel.ro/catalogsearch/result/"
        f"?q={query}"
    )

    all_products = []
    seen_urls = set()
    page_number = 1

    while True:
        page_url = f"{base_url}&p={page_number}"

        print(
            f"Checking Noriel {search_name} "
            f"page {page_number}..."
        )

        response = requests.get(
            page_url,
            headers=headers,
            timeout=30,
        )

        print(
            f"Noriel {search_name} status code: "
            f"{response.status_code}"
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser",
        )

        cards = soup.select(
            "a:has(h2.product-item-name)"
        )

        page_products = []

        for card in cards:
            name_element = card.select_one(
                "h2.product-item-name"
            )

            price_element = card.select_one(
                "span.price"
            )

            url = card.get("href")

            if (
                not name_element
                or not price_element
                or not url
            ):
                continue

            if url in seen_urls:
                continue

            product = Product(
                name=name_element.get_text(
                    " ",
                    strip=True,
                ),
                price=price_element.get_text(
                    " ",
                    strip=True,
                ),
                url=url,
                store="NORIEL",
            )

            page_products.append(product)
            seen_urls.add(url)

        if not page_products:
            print(
                f"No new Noriel {search_name} "
                f"products found on page "
                f"{page_number}. Stopping."
            )
            break

        print(
            f"Found {len(page_products)} Noriel "
            f"{search_name} products on page "
            f"{page_number}."
        )

        all_products.extend(page_products)
        page_number += 1

    print(
        f"Found {len(all_products)} Noriel "
        f"{search_name} products in total."
    )

    return all_products


def get_products() -> list[Product]:
    all_products = []
    global_seen_urls = set()

    for search in NORIEL_SEARCHES:
        products = scrape_search(
            search["name"],
            search["query"],
        )

        for product in products:
            if product.url not in global_seen_urls:
                all_products.append(product)
                global_seen_urls.add(product.url)

    print(
        f"Found {len(all_products)} Noriel products "
        f"across all monitored searches."
    )

    return all_products