"""Serialization helpers that aggregate relational data into JSON-ready dicts."""

# Bu modül, veri katmanındaki ilişkili kayıtları API yanıtlarında kullanılacak
# zenginleştirilmiş sözlüklere dönüştürmek için yardımcı fonksiyonlar sağlar.

import json
from typing import Any, Dict, Iterable, List, Optional

from sqlite3 import Connection


def parse_json(value: str | None) -> Any:
    """Safely parse JSON fields stored as text."""

    if value is None:
        return None
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return value


def summarize_offers(offers: Iterable[Dict[str, Any]]) -> Dict[str, Any] | None:
    """Summarize pricing distribution for quick overviews."""

    offers_list = list(offers)
    if not offers_list:
        return None

    prices = [offer["price"] for offer in offers_list if offer.get("price") is not None]
    if not prices:
        return None

    lowest_offer = min(offers_list, key=lambda offer: offer.get("price", float("inf")))
    highest_offer = max(offers_list, key=lambda offer: offer.get("price", float("-inf")))
    average_price = sum(prices) / len(prices)

    return {
        "count": len(offers_list),
        "average_price": round(average_price, 2),
        "lowest_price": lowest_offer.get("price"),
        "lowest_price_channel": lowest_offer.get("channel"),
        "highest_price": highest_offer.get("price"),
        "highest_price_channel": highest_offer.get("channel"),
    }


def rows_to_dicts(rows: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Convert SQLite row objects into plain dicts."""

    return [dict(row) for row in rows]


def fetch_product(conn: Connection, product_id: int) -> Dict[str, Any] | None:
    """Return a product with nested offers, reviews, keywords, insights, suppliers, creatives and reports."""

    product = conn.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
    if not product:
        return None

    product_dict = dict(product)
    product_dict["specs_json"] = parse_json(product_dict.get("specs_json"))

    product_dict["offers"] = rows_to_dicts(
        conn.execute(
            "SELECT * FROM offers WHERE product_id = ? ORDER BY last_seen_at DESC NULLS LAST, id DESC",
            (product_id,),
        ).fetchall()
    )

    product_dict["reviews"] = rows_to_dicts(
        conn.execute(
            "SELECT * FROM reviews WHERE product_id = ? ORDER BY date DESC NULLS LAST, id DESC",
            (product_id,),
        ).fetchall()
    )
    for review in product_dict["reviews"]:
        review["topics"] = parse_json(review.get("topics"))

    product_dict["keywords"] = rows_to_dicts(
        conn.execute(
            "SELECT * FROM keywords WHERE product_id = ? ORDER BY volume DESC NULLS LAST",
            (product_id,),
        ).fetchall()
    )

    insight = conn.execute(
        "SELECT * FROM insights WHERE product_id = ?",
        (product_id,),
    ).fetchone()
    if insight:
        insight["swot_json"] = parse_json(insight.get("swot_json"))
    product_dict["insights"] = insight

    supplier_rows = rows_to_dicts(
        conn.execute(
            """
            SELECT s.* FROM suppliers s
            JOIN product_suppliers ps ON ps.supplier_id = s.id
            WHERE ps.product_id = ?
            """,
            (product_id,),
        ).fetchall()
    )
    product_dict["suppliers"] = supplier_rows

    creatives = rows_to_dicts(
        conn.execute(
            "SELECT * FROM creatives WHERE product_id = ?",
            (product_id,),
        ).fetchall()
    )
    for creative in creatives:
        creative_id = creative["id"]
        creative["assets"] = parse_json(creative.get("assets"))
        creative["sizes"] = [
            row["size"]
            for row in conn.execute(
                "SELECT size FROM creative_sizes WHERE creative_id = ?",
                (creative_id,),
            ).fetchall()
        ]
        creative["channels"] = [
            row["channel"]
            for row in conn.execute(
                "SELECT channel FROM creative_channels WHERE creative_id = ?",
                (creative_id,),
            ).fetchall()
        ]
    product_dict["creatives"] = creatives

    product_dict["reports"] = rows_to_dicts(
        conn.execute(
            "SELECT * FROM reports WHERE product_id = ? ORDER BY id DESC",
            (product_id,),
        ).fetchall()
    )

    product_dict["offer_summary"] = summarize_offers(product_dict["offers"])

    return product_dict


def fetch_all_products(
    conn: Connection,
    *,
    search: Optional[str] = None,
    limit: int = 20,
    offset: int = 0,
    product_ids: Optional[Iterable[int]] = None,
) -> List[Dict[str, Any]]:
    """Return paginated products optionally filtered by search criteria."""

    if product_ids is not None:
        ids = list(product_ids)
    else:
        params: list[Any] = []
        query = "SELECT id FROM products"
        if search:
            query += " WHERE LOWER(title) LIKE ? OR LOWER(brand) LIKE ?"
            like_term = f"%{search.lower()}%"
            params.extend([like_term, like_term])
        query += " ORDER BY id LIMIT ? OFFSET ?"
        params.extend([limit, offset])
        ids = [row["id"] for row in conn.execute(query, params).fetchall()]
    return [fetch_product(conn, product_id) for product_id in ids]


def fetch_supplier(conn: Connection, supplier_id: int) -> Dict[str, Any] | None:
    """Return supplier details with optional RFQ list."""

    supplier = conn.execute("SELECT * FROM suppliers WHERE id = ?", (supplier_id,)).fetchone()
    if not supplier:
        return None
    supplier_dict = dict(supplier)
    supplier_dict["rfqs"] = rows_to_dicts(
        conn.execute(
            "SELECT * FROM rfqs WHERE supplier_id = ? ORDER BY id DESC",
            (supplier_id,),
        ).fetchall()
    )
    return supplier_dict


def fetch_offers(
    conn: Connection,
    *,
    product_id: Optional[int] = None,
    channel: Optional[str] = None,
    limit: int = 50,
) -> List[Dict[str, Any]]:
    """Return recent offers optionally filtered by product or channel."""

    params: list[Any] = []
    clauses: list[str] = []
    if product_id is not None:
        clauses.append("product_id = ?")
        params.append(product_id)
    if channel is not None:
        clauses.append("LOWER(channel) = ?")
        params.append(channel.lower())
    where = ""
    if clauses:
        where = " WHERE " + " AND ".join(clauses)
    query = (
        "SELECT * FROM offers"
        + where
        + " ORDER BY last_seen_at DESC NULLS LAST, id DESC LIMIT ?"
    )
    params.append(limit)
    return rows_to_dicts(conn.execute(query, params).fetchall())


def fetch_reviews(
    conn: Connection,
    *,
    product_id: Optional[int] = None,
    min_rating: Optional[float] = None,
    limit: int = 50,
) -> List[Dict[str, Any]]:
    """Return product reviews filtered by rating threshold."""

    params: list[Any] = []
    clauses: list[str] = []
    if product_id is not None:
        clauses.append("product_id = ?")
        params.append(product_id)
    if min_rating is not None:
        clauses.append("rating >= ?")
        params.append(min_rating)
    where = ""
    if clauses:
        where = " WHERE " + " AND ".join(clauses)
    query = "SELECT * FROM reviews" + where + " ORDER BY date DESC NULLS LAST, id DESC LIMIT ?"
    params.append(limit)
    results = rows_to_dicts(conn.execute(query, params).fetchall())
    for review in results:
        review["topics"] = parse_json(review.get("topics"))
    return results


def fetch_rfqs(
    conn: Connection,
    *,
    product_id: Optional[int] = None,
    supplier_id: Optional[int] = None,
    status: Optional[str] = None,
    limit: int = 50,
) -> List[Dict[str, Any]]:
    """Return RFQs filtered by supplier, product or status."""

    params: list[Any] = []
    clauses: list[str] = []
    if product_id is not None:
        clauses.append("product_id = ?")
        params.append(product_id)
    if supplier_id is not None:
        clauses.append("supplier_id = ?")
        params.append(supplier_id)
    if status is not None:
        clauses.append("LOWER(status) = ?")
        params.append(status.lower())
    where = ""
    if clauses:
        where = " WHERE " + " AND ".join(clauses)
    query = "SELECT * FROM rfqs" + where + " ORDER BY id DESC LIMIT ?"
    params.append(limit)
    return rows_to_dicts(conn.execute(query, params).fetchall())
