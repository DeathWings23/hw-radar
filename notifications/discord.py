import os

import requests

from models import Product


def send_discord_notification(product: Product) -> None:
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")

    if not webhook_url:
        raise RuntimeError(
            "DISCORD_WEBHOOK_URL is missing from the environment."
        )

    message = {
        "embeds": [
            {
                "title": "🚗 New Hot Wheels product found!",
                "description": product.name,
                "url": product.url,
                "fields": [
                    {
                        "name": "Store",
                        "value": product.store,
                        "inline": True,
                    },
                    {
                        "name": "Price",
                        "value": product.price,
                        "inline": True,
                    },
                ],
            }
        ]
    }

    response = requests.post(
        webhook_url,
        json=message,
        timeout=15,
    )

    response.raise_for_status()