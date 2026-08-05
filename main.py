import os
from datetime import UTC, datetime

from core.filters import should_notify
from notifications.discord import send_discord_notification
from scrapers.noriel import get_products as get_noriel_products
from scrapers.smyk import get_products as get_smyk_products
from storage.database import load_seen_products, save_seen_products


print("=" * 60)
print("🚗 HW Radar Starting...")
print(f"Triggered by: {os.getenv('GITHUB_EVENT_NAME', 'local')}")
print(f"Started at: {datetime.now(UTC).isoformat()}")
print("=" * 60)
print()

smyk_products = get_smyk_products()
noriel_products = get_noriel_products()

products = smyk_products + noriel_products

print()
print(f"Found {len(smyk_products)} SMYK products")
print(f"Found {len(noriel_products)} Noriel products")
print(f"Found {len(products)} products in total")

seen_products = load_seen_products()
new_products = []

# Find products that were not present in the previous scan
for product in products:
    if product.url not in seen_products:
        new_products.append(product)
        seen_products.add(product.url)

print(f"Found {len(new_products)} new products\n")

notification_count = 0
ignored_count = 0

# Notify only for products matching the collector watch list
for product in new_products:
    if should_notify(product):
        print(
            f"🚨 Collector item detected: "
            f"{product.store} | {product.name}"
        )

        try:
            send_discord_notification(product)
            notification_count += 1
            print("✅ Discord notification sent.")
        except Exception as error:
            print(f"❌ Discord notification failed: {error}")
    else:
        ignored_count += 1
        print(f"⏭️ Ignored: {product.store} | {product.name}")

print()
print("=" * 60)
print("📊 Scan Summary")
print(f"SMYK products: {len(smyk_products)}")
print(f"Noriel products: {len(noriel_products)}")
print(f"Total products: {len(products)}")
print(f"New products: {len(new_products)}")
print(f"Notifications sent: {notification_count}")
print(f"Products ignored: {ignored_count}")
print("=" * 60)

# Save every seen URL, including ignored products
save_seen_products(seen_products)

print("\nDatabase updated successfully.")