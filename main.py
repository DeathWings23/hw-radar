from core.filters import should_notify
from notifications.discord import send_discord_notification
from scrapers.smyk import get_products
from storage.database import load_seen_products, save_seen_products

print("🚗 HW Radar Starting...\n")

products = get_products()

print(f"Found {len(products)} products")

seen_products = load_seen_products()

new_products = []

# Find new products
for product in products:
    if product.url not in seen_products:
        new_products.append(product)
        seen_products.add(product.url)

print(f"Found {len(new_products)} new products\n")

# Notify only for products that match our watch list
for product in new_products:

    print(product.name)

    if should_notify(product):
        print("🚨 Sending Discord notification...")
        send_discord_notification(product)

# Save the updated database
save_seen_products(seen_products)

print("\nDatabase updated successfully.")