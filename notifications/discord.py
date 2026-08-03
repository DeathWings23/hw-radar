import os
import time

import requests
from dotenv import load_dotenv

from models import Product


load_dotenv()


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

    for attempt in range(3):
        response = requests.post(
            webhook_url,
            json=message,
            timeout=15,
        )

        if response.status_code != 429:
            response.raise_for_status()
            return

        try:
            retry_after = float(
                response.json().get("retry_after", 2)
            )
        except (ValueError, TypeError, requests.JSONDecodeError):
            retry_after = 2

        print(
            f"Discord rate limit reached. "
            f"Waiting {retry_after:.1f} seconds..."
        )
        time.sleep(retry_after + 0.5)

    raise RuntimeError(
        "Discord notification failed after 3 attempts."
    )