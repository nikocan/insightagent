"""Ad Studio servisleri kampanya brifleri, uyum kontrolleri ve varyasyon üretimi sağlar."""

# Bu modül, kreatif üretim akışı için veritabanındaki brifleri okuyup
# isteğe bağlı metin varyasyonları oluşturan yardımcı fonksiyonları içerir.

from __future__ import annotations

import random
from typing import Any, Dict, List

from sqlite3 import Connection

from ..utils.serializers import fetch_product, parse_json


def _load_brief(conn: Connection, product_id: int) -> Dict[str, Any] | None:
    """Fetch a creative brief row for the given product."""

    row = conn.execute(
        "SELECT * FROM creative_briefs WHERE product_id = ?",
        (product_id,),
    ).fetchone()
    if not row:
        return None
    brief = dict(row)
    brief["recommended_channels"] = parse_json(brief.get("recommended_channels")) or []
    return brief


def _load_compliance(conn: Connection, product_id: int) -> Dict[str, Any] | None:
    """Fetch stored compliance guidance for a product."""

    row = conn.execute(
        "SELECT * FROM compliance_guidelines WHERE product_id = ?",
        (product_id,),
    ).fetchone()
    if not row:
        return None
    guidance = dict(row)
    guidance["flagged_claims"] = parse_json(guidance.get("flagged_claims")) or []
    return guidance


def assemble_brief_payload(conn: Connection, product_id: int) -> Dict[str, Any]:
    """Return an enriched creative brief combining product and compliance context."""

    product = fetch_product(conn, product_id)
    if not product:
        raise ValueError("Product not found")

    brief = _load_brief(conn, product_id) or {}
    compliance = _load_compliance(conn, product_id) or {"flagged_claims": []}

    return {
        "product": {
            "id": product["id"],
            "title": product["title"],
            "brand": product["brand"],
            "category": product.get("category"),
        },
        "brief": brief,
        "compliance": {
            "level": compliance.get("level", "none"),
            "flagged_claims": compliance.get("flagged_claims", []),
            "guidance": compliance.get("guidance"),
        },
        "creative_assets": product.get("creatives", []),
    }


def assemble_compliance_payload(conn: Connection, product_id: int) -> Dict[str, Any]:
    """Return compliance rules and quick recommendations for a product."""

    product = fetch_product(conn, product_id)
    if not product:
        raise ValueError("Product not found")

    compliance = _load_compliance(conn, product_id) or {}

    return {
        "product": {
            "id": product["id"],
            "title": product["title"],
            "brand": product["brand"],
        },
        "level": compliance.get("level", "none"),
        "flagged_claims": compliance.get("flagged_claims", []),
        "guidance": compliance.get("guidance"),
    }


def generate_variations(
    conn: Connection,
    *,
    product_id: int,
    channel: str,
    tone: str | None = None,
    format_hint: str | None = None,
    variation_count: int = 3,
) -> Dict[str, Any]:
    """Create channel-aware ad copy variations derived from product metadata."""

    product = fetch_product(conn, product_id)
    if not product:
        raise ValueError("Product not found")

    brief = _load_brief(conn, product_id)
    compliance = _load_compliance(conn, product_id) or {"flagged_claims": []}

    brand = product["brand"]
    title = product["title"]
    highlight = brief.get("primary_message") if brief else None
    cta = brief.get("call_to_action") if brief else "Discover more"
    keywords = [kw["term"] for kw in product.get("keywords", [])][:3]

    seed_messages: List[str] = []
    if highlight:
        seed_messages.append(highlight)
    if product.get("insights") and product["insights"].get("sales_score"):
        seed_messages.append(
            f"Sales momentum score: {product['insights']['sales_score']:.0%} confidence"
        )
    if keywords:
        seed_messages.append("Top keyword: " + keywords[0])

    def build_variant(idx: int) -> Dict[str, Any]:
        leading = tone or (brief.get("tone") if brief else "Confident")
        channel_tag = channel.title()
        base = f"{leading} message for {channel_tag}: {title}"
        if highlight:
            base += f" — {highlight}"
        if format_hint:
            base += f" | Format: {format_hint}"
        body_options = [
            f"Glow with {brand}'s {title} in your nightly ritual.",
            f"{title} delivers instant results backed by data-driven insight.",
            f"Join thousands choosing {brand} for elevated skincare.",
        ]
        random.seed(idx + len(title))
        body = random.choice(body_options)
        actions = cta
        return {
            "headline": base,
            "body": body,
            "call_to_action": actions,
        }

    variations = [build_variant(i) for i in range(variation_count)]
    if seed_messages:
        for idx, variant in enumerate(variations):
            variant["body"] += " " + seed_messages[idx % len(seed_messages)]

    flagged = compliance.get("flagged_claims", [])
    return {
        "product": {"id": product["id"], "title": title, "brand": brand},
        "channel": channel,
        "tone": tone or (brief.get("tone") if brief else None),
        "format_hint": format_hint,
        "variations": variations,
        "avoid_phrases": flagged,
    }
