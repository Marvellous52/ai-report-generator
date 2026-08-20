"""
Seeds data/business.db with sample sales data so the project runs
out of the box without needing a real dataset.

Usage:
    python seed_data.py
"""

import os
import random
import sqlite3
from datetime import datetime, timedelta

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "business.db")

REGIONS = ["Lagos", "Rivers", "Abuja", "Kano", "Remote/Online"]
PRODUCTS = [
    "Consulting Package",
    "Automation Setup",
    "Training Session",
    "Support Retainer",
    "Custom Integration",
]


def seed(num_rows=400, seed_value=42):
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            region TEXT NOT NULL,
            product TEXT NOT NULL,
            units_sold INTEGER NOT NULL,
            unit_price REAL NOT NULL,
            revenue REAL NOT NULL
        )
    """)

    cur.execute("DELETE FROM sales")

    random.seed(seed_value)
    start = datetime(2025, 1, 1)
    rows = []
    for _ in range(num_rows):
        date = start + timedelta(days=random.randint(0, 210))
        region = random.choice(REGIONS)
        product = random.choice(PRODUCTS)
        units = random.randint(1, 12)
        price = round(random.uniform(50, 500), 2)
        revenue = round(units * price, 2)
        rows.append((date.strftime("%Y-%m-%d"), region, product, units, price, revenue))

    cur.executemany(
        "INSERT INTO sales (date, region, product, units_sold, unit_price, revenue) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        rows,
    )
    conn.commit()
    conn.close()
    print(f"Seeded {num_rows} rows into {DB_PATH}")


if __name__ == "__main__":
    seed()
