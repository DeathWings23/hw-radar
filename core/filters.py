from config import WATCH_KEYWORDS, IGNORE_KEYWORDS


def should_notify(product):

    name = product.name.lower()

    # Ignore unwanted products first
    for keyword in IGNORE_KEYWORDS:
        if keyword.lower() in name:
            return False

    # Notify only for watched keywords
    for keyword in WATCH_KEYWORDS:
        if keyword.lower() in name:
            return True

    return False