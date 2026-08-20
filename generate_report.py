"""
AI-Powered Business Report Generator
--------------------------------------
Queries a SQL database of business data, computes key operational metrics,
and uses the Claude API to generate a written executive summary report.

Usage:
    python generate_report.py

Requires:
    ANTHROPIC_API_KEY environment variable set.
    pip install anthropic
"""

import os
import sqlite3
import sys
from datetime import datetime

import anthropic

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "business.db")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
MODEL = "claude-sonnet-4-6"


def get_connection():
    if not os.path.exists(DB_PATH):
        sys.exit(f"Database not found at {DB_PATH}. Run seed_data.py first.")
    return sqlite3.connect(DB_PATH)


def fetch_metrics(conn):
    """Run a set of SQL queries to build a metrics dictionary for the report."""
    cur = conn.cursor()

    metrics = {}

    cur.execute("SELECT ROUND(SUM(revenue), 2), COUNT(*), SUM(units_sold) FROM sales")
    total_revenue, total_orders, total_units = cur.fetchone()
    metrics["total_revenue"] = total_revenue
    metrics["total_orders"] = total_orders
    metrics["total_units"] = total_units

    cur.execute("""
        SELECT region, ROUND(SUM(revenue), 2) AS rev
        FROM sales
        GROUP BY region
        ORDER BY rev DESC
    """)
    metrics["revenue_by_region"] = cur.fetchall()

    cur.execute("""
        SELECT product, ROUND(SUM(revenue), 2) AS rev, SUM(units_sold) AS units
        FROM sales
        GROUP BY product
        ORDER BY rev DESC
    """)
    metrics["revenue_by_product"] = cur.fetchall()

    cur.execute("""
        SELECT strftime('%Y-%m', date) AS month, ROUND(SUM(revenue), 2) AS rev
        FROM sales
        GROUP BY month
        ORDER BY month
    """)
    metrics["monthly_revenue"] = cur.fetchall()

    return metrics


def build_prompt(metrics):
    """Turn raw metrics into a structured prompt for Claude."""
    lines = []
    lines.append(f"Total revenue: ${metrics['total_revenue']:,}")
    lines.append(f"Total orders: {metrics['total_orders']}")
    lines.append(f"Total units sold: {metrics['total_units']}")
    lines.append("")
    lines.append("Revenue by region:")
    for region, rev in metrics["revenue_by_region"]:
        lines.append(f"  - {region}: ${rev:,}")
    lines.append("")
    lines.append("Revenue by product:")
    for product, rev, units in metrics["revenue_by_product"]:
        lines.append(f"  - {product}: ${rev:,} ({units} units)")
    lines.append("")
    lines.append("Monthly revenue trend:")
    for month, rev in metrics["monthly_revenue"]:
        lines.append(f"  - {month}: ${rev:,}")

    data_block = "\n".join(lines)

    prompt = f"""You are a business analyst preparing a concise executive summary
for leadership based on the operational data below. Write a professional
report with these sections:

1. Executive Summary (2-3 sentences)
2. Key Highlights (3-5 bullet points)
3. Regional Performance (short paragraph)
4. Product Performance (short paragraph)
5. Recommendation (1-2 actionable suggestions based on the data)

Use a clear, confident, business-appropriate tone. Do not invent numbers
that aren't in the data below. Format the output in Markdown.

DATA:
{data_block}
"""
    return prompt


def generate_report(prompt):
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        sys.exit("Set the ANTHROPIC_API_KEY environment variable before running.")

    client = anthropic.Anthropic(api_key=api_key)

    response = client.messages.create(
        model=MODEL,
        max_tokens=1200,
        messages=[{"role": "user", "content": prompt}],
    )

    return response.content[0].text


def main():
    conn = get_connection()
    metrics = fetch_metrics(conn)
    conn.close()

    prompt = build_prompt(metrics)
    print("Querying data and generating report with Claude...")
    report_text = generate_report(prompt)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    out_path = os.path.join(OUTPUT_DIR, f"report_{timestamp}.md")

    with open(out_path, "w") as f:
        f.write(f"# Business Performance Report\n")
        f.write(f"_Generated {datetime.now().strftime('%Y-%m-%d %H:%M')}_\n\n")
        f.write(report_text)

    print(f"Report saved to {out_path}")


if __name__ == "__main__":
    main()
