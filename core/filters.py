from models import Product
from config import IGNORE_KEYWORDS, WATCH_KEYWORDS


def contains_keyword(product_name: str, keywords: list[str]) -> bool:
    normalized_name = product_name.casefold()

    return any(
        keyword.casefold() in normalized_name
        for keyword in keywords
    )


def should_notify(product: Product) -> bool:
    """
    Return True only when a product matches the collector watch list
    and does not match an ignored category.
    """

    if contains_keyword(product.name, IGNORE_KEYWORDS):
        return False

    return contains_keyword(product.name, WATCH_KEYWORDS)