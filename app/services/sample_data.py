"""Utility helpers to seed the SQLite database with demo records."""

# Bu modül, demo ortamı için ilişkili ürün, fiyat, yorum ve RFQ kayıtlarını
# birbirine bağlayarak uçtan uca senaryo sağlar.

import json
from datetime import datetime, timedelta, timezone

from sqlite3 import Connection


def seed_demo_data(conn: Connection) -> None:
    """Insert demo data if products table is empty."""

    cursor = conn.execute("SELECT COUNT(1) AS count FROM products")
    if cursor.fetchone()["count"]:
        return

    now = datetime.now(timezone.utc)

    # Ürünleri ekleyip kimliklerini saklıyoruz.
    conn.executemany(
        """
        INSERT INTO products (gtin, upc, brand, title, category, specs_json)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        [
            (
                "0860001234567",
                None,
                "Luna Labs",
                "HydraGlow Night Serum",
                "Beauty & Personal Care",
                json.dumps({"volume_ml": 50, "ingredients": ["Hyaluronic Acid", "Vitamin C"]}),
            ),
            (
                "0860007654321",
                None,
                "Aurora Botanics",
                "Aurora Mist Hydrating Toner",
                "Beauty & Personal Care",
                json.dumps({"volume_ml": 120, "ingredients": ["Rose Water", "Niacinamide"]}),
            ),
        ],
    )

    product_rows = conn.execute("SELECT id, brand FROM products ORDER BY id").fetchall()
    serum_id = product_rows[0]["id"]
    toner_id = product_rows[1]["id"]

    # Fiyat teklifleri farklı kanallar için eklenir.
    conn.executemany(
        """
        INSERT INTO offers (product_id, channel, seller, price, currency, stock, ship_from, last_seen_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [
            (
                serum_id,
                "Amazon",
                "Luna Labs Official",
                49.99,
                "USD",
                120,
                "USA",
                (now - timedelta(hours=2)).isoformat(),
            ),
            (
                serum_id,
                "Sephora",
                "Glow Collective",
                54.0,
                "USD",
                80,
                "USA",
                (now - timedelta(hours=5)).isoformat(),
            ),
            (
                toner_id,
                "Amazon",
                "Aurora Botanics Store",
                32.5,
                "USD",
                200,
                "USA",
                (now - timedelta(hours=1)).isoformat(),
            ),
            (
                toner_id,
                "Etsy",
                "Indie Glow Retail",
                34.99,
                "USD",
                45,
                "UK",
                (now - timedelta(hours=3)).isoformat(),
            ),
        ],
    )

    # Yorumlar; farklı kaynaklardan duygu skoru içerir.
    conn.executemany(
        """
        INSERT INTO reviews (product_id, source, rating, text, lang, date, sentiment, topics)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [
            (
                serum_id,
                "Amazon",
                4.6,
                "Skin feels hydrated and plump after a week of use!",
                "en",
                now.date().isoformat(),
                "positive",
                json.dumps(["hydration", "texture"]),
            ),
            (
                serum_id,
                "Sephora",
                3.8,
                "Great glow but packaging could be sturdier.",
                "en",
                (now - timedelta(days=2)).date().isoformat(),
                "neutral",
                json.dumps(["packaging"]),
            ),
            (
                toner_id,
                "Amazon",
                4.9,
                "Refreshing scent and instant hydration boost!",
                "en",
                now.date().isoformat(),
                "positive",
                json.dumps(["scent", "hydration"]),
            ),
        ],
    )

    # Anahtar kelime setleri kanal bazlı araştırmayı temsil eder.
    conn.executemany(
        """
        INSERT INTO keywords (product_id, term, intent, volume, difficulty, cpc_est)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        [
            (
                serum_id,
                "best night serum",
                "commercial",
                5400,
                0.38,
                2.45,
            ),
            (
                serum_id,
                "vitamin c hyaluronic serum",
                "transactional",
                2100,
                0.42,
                3.1,
            ),
            (
                toner_id,
                "hydrating facial toner",
                "commercial",
                3200,
                0.35,
                1.9,
            ),
        ],
    )

    # İçgörü kayıtları ürün başına tek satır olarak saklanır.
    conn.executemany(
        """
        INSERT INTO insights (product_id, sales_score, trend_score, price_elasticity, swot_json)
        VALUES (?, ?, ?, ?, ?)
        """,
        [
            (
                serum_id,
                0.82,
                0.74,
                0.56,
                json.dumps(
                    {
                        "strengths": ["Strong social buzz"],
                        "weaknesses": ["Limited distribution"],
                        "opportunities": ["Influencer partnerships"],
                        "threats": ["Increasing competition"],
                    }
                ),
            ),
            (
                toner_id,
                0.68,
                0.81,
                0.44,
                json.dumps(
                    {
                        "strengths": ["Vegan formula"],
                        "weaknesses": ["Short shelf life"],
                        "opportunities": ["Spa partnerships"],
                        "threats": ["Seasonal demand"],
                    }
                ),
            ),
        ],
    )

    # Tedarikçi ve RFQ ilişkileri oluşturulur.
    conn.execute(
        """
        INSERT INTO suppliers (name, country, moq, lead_time, contact)
        VALUES (?, ?, ?, ?, ?)
        """,
        ("Shenzhen Glow Manufacturing", "China", 500, 28, "sales@glowfactory.cn"),
    )
    supplier_id = conn.execute("SELECT id FROM suppliers LIMIT 1").fetchone()["id"]

    conn.executemany(
        "INSERT INTO product_suppliers (product_id, supplier_id) VALUES (?, ?)",
        [(serum_id, supplier_id), (toner_id, supplier_id)],
    )

    conn.executemany(
        """
        INSERT INTO rfqs (product_id, supplier_id, status, quotes)
        VALUES (?, ?, ?, ?)
        """,
        [
            (
                serum_id,
                supplier_id,
                "open",
                json.dumps([{"unit_price": 18.5, "currency": "USD"}]),
            ),
            (
                toner_id,
                supplier_id,
                "closed",
                json.dumps([{"unit_price": 12.0, "currency": "USD", "moq": 300}]),
            ),
        ],
    )

    # Kreatif varlıklar çoklu boyut ve kanal kaydı ile ilişkilendirilir.
    conn.executemany(
        """
        INSERT INTO creatives (product_id, copy, assets)
        VALUES (?, ?, ?)
        """,
        [
            (
                serum_id,
                "Experience overnight radiance with HydraGlow Night Serum.",
                json.dumps(["https://cdn.example.com/hydraglow/main.png"]),
            ),
            (
                toner_id,
                "Meet Aurora Mist Toner for dewy mornings in seconds.",
                json.dumps(["https://cdn.example.com/auroram-mist/main.png"]),
            ),
        ],
    )

    creative_rows = conn.execute("SELECT id, product_id FROM creatives ORDER BY id").fetchall()
    for creative in creative_rows:
        base_sizes = ["1080x1080", "1080x1920", "1200x628"]
        base_channels = ["Instagram", "TikTok", "Facebook"]
        if creative["product_id"] == toner_id:
            base_sizes = ["1080x1920", "1000x1500"]
            base_channels = ["Instagram", "Pinterest"]
        for size in base_sizes:
            conn.execute(
                "INSERT INTO creative_sizes (creative_id, size) VALUES (?, ?)",
                (creative["id"], size),
            )
        for channel in base_channels:
            conn.execute(
                "INSERT INTO creative_channels (creative_id, channel) VALUES (?, ?)",
                (creative["id"], channel),
            )

    conn.executemany(
        """
        INSERT INTO reports (product_id, pdf_url, created_by)
        VALUES (?, ?, ?)
        """,
        [
            (
                serum_id,
                "https://cdn.example.com/reports/hydraglow.pdf",
                "insight-bot",
            ),
            (
                toner_id,
                "https://cdn.example.com/reports/auroram-mist.pdf",
                "insight-bot",
            ),
        ],
    )

    conn.commit()
