from core.filters import should_notify
from notifications.discord import send_discord_notification
from scrapers.smyk import get_products
from storage.database import load_seen_products, save_seen_products


print("🚗 HW Radar Starting...\n")

products = get_products()

print(f"Found {len(products)} products")

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
        print(f"🚨 Collector item detected: {product.name}")

        try:
            send_discord_notification(product)
            notification_count += 1
            print("✅ Discord notification sent.")
        except Exception as error:
            print(f"❌ Discord notification failed: {error}")
    else:
        ignored_count += 1
        print(f"⏭️ Ignored: {product.name}")

print(f"\nNotifications sent: {notification_count}")
print(f"Products ignored: {ignored_count}")

# Save every seen URL, including ignored products
save_seen_products(seen_products)

print("\nDatabase updated successfully.")