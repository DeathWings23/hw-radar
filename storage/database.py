import json
import os

DATABASE_FILE = "data/seen_products.json"


def load_seen_products():

    if not os.path.exists(DATABASE_FILE):
        return set()

    with open(DATABASE_FILE, "r", encoding="utf-8") as f:
        return set(json.load(f))


def save_seen_products(products):

    with open(DATABASE_FILE, "w", encoding="utf-8") as f:
        json.dump(sorted(products), f, indent=4)