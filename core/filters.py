from models import Product
from config import IGNORE_KEYWORDS, WATCH_KEYWORDS


def contains_keyword(product_name: str, keywords: list[str]) -> bool:
    normalized_name = product_name.casefold()

    return any(
        keyword.casefold() in normalized_name
        for keyword in keywords
    )


def is_pokemon_tcg(product: Product) -> bool:
    """
    Return True only for products that appear to be
    Pokemon trading card products.
    """

    normalized_name = product.name.casefold()

    pokemon_keywords = [
        "pokemon",
        "pokémon",
    ]

    tcg_keywords = [
        "tcg",
        "trading card",
        "carti de joc",
        "carti de colectie",
        "booster",
        "booster pack",
        "booster bundle",
        "elite trainer box",
        "etb",
        "collection box",
        "collector chest",
        "mini tin",
        "battle deck",
        "checklane",
        "blister",
        "sleeved booster",
        "30th celebration",
        "30th anniversary",
        "30 anniversary",
        "30 aniversare",
    ]

    has_pokemon = any(
        keyword.casefold() in normalized_name
        for keyword in pokemon_keywords
    )

    has_tcg_keyword = any(
        keyword.casefold() in normalized_name
        for keyword in tcg_keywords
    )

    return has_pokemon and has_tcg_keyword


def should_notify(product: Product) -> bool:
    """
    Return True for Pokemon TCG products or when a product
    matches the existing Hot Wheels collector watch list.
    """

    # Pokemon TCG has its own independent detection.
    if is_pokemon_tcg(product):
        return True

    # ORIGINAL HOT WHEELS LOGIC BELOW
    if contains_keyword(product.name, IGNORE_KEYWORDS):
        return False

    return contains_keyword(product.name, WATCH_KEYWORDS)