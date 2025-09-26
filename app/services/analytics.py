"""Service helpers deriving analytics dashboards from stored data."""

# Bu modül, portföy ve ürün bazında stratejik raporlar üretmek için veri
# katmanından gelen ilişkili kayıtları derleyip özetler.

from collections import Counter
from statistics import mean
from typing import Any, Dict, Iterable, List

from sqlite3 import Connection

from ..utils.serializers import (
    fetch_all_products,
    fetch_product,
    fetch_rfqs,
)


def _summarize_reviews(reviews: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
    """Return aggregate review sentiment and topic distribution."""

    review_list = list(reviews)
    if not review_list:
        return {
            "count": 0,
            "average_rating": None,
            "positive_ratio": 0.0,
            "sentiment_breakdown": {},
            "top_topics": [],
        }

    sentiments = Counter(
        (review.get("sentiment") or "unknown").lower() for review in review_list
    )
    ratings = [review.get("rating", 0) for review in review_list]
    topics = Counter(
        topic
        for review in review_list
        for topic in (review.get("topics") or [])
        if isinstance(topic, str)
    )

    positive_ratio = sentiments.get("positive", 0) / len(review_list)

    return {
        "count": len(review_list),
        "average_rating": round(mean(ratings), 2),
        "positive_ratio": round(positive_ratio, 2),
        "sentiment_breakdown": dict(sentiments),
        "top_topics": [topic for topic, _ in topics.most_common(5)],
    }


def _summarize_keywords(keywords: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
    """Return aggregate keyword opportunity metrics."""

    keyword_list = list(keywords)
    if not keyword_list:
        return {
            "total_volume": 0,
            "average_difficulty": None,
            "primary_terms": [],
        }

    total_volume = sum(keyword.get("volume", 0) or 0 for keyword in keyword_list)
    difficulties = [
        keyword.get("difficulty")
        for keyword in keyword_list
        if keyword.get("difficulty") is not None
    ]
    average_difficulty = round(mean(difficulties), 2) if difficulties else None

    top_terms = [
        keyword.get("term")
        for keyword in sorted(
            keyword_list,
            key=lambda item: item.get("volume", 0) or 0,
            reverse=True,
        )[:5]
        if keyword.get("term")
    ]

    return {
        "total_volume": total_volume,
        "average_difficulty": average_difficulty,
        "primary_terms": top_terms,
    }


def _summarize_creatives(creatives: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
    """Return channel and asset coverage for creatives."""

    creative_list = list(creatives)
    if not creative_list:
        return {
            "unique_channels": [],
            "dominant_channels": [],
            "asset_count": 0,
        }

    channel_counter = Counter(
        channel
        for creative in creative_list
        for channel in (creative.get("channels") or [])
        if isinstance(channel, str)
    )
    asset_count = sum(len(creative.get("assets") or []) for creative in creative_list)

    return {
        "unique_channels": sorted(channel_counter.keys()),
        "dominant_channels": [channel for channel, _ in channel_counter.most_common(3)],
        "asset_count": asset_count,
    }


def build_portfolio_dashboard(conn: Connection) -> Dict[str, Any]:
    """Compose a portfolio-wide performance dashboard."""

    products = fetch_all_products(conn, limit=100)
    if not products:
        return {
            "overview": {"product_count": 0, "average_sales_score": None, "keyword_volume_total": 0},
            "growth": {"top_growing_products": []},
            "pricing": {"average_price_gap": None, "lowest_offer": None},
            "sourcing": {"open_rfqs": 0, "supplier_coverage": 0},
            "creative": {"channels": [], "asset_count": 0},
        }

    sales_scores = [
        product["insights"]["sales_score"]
        for product in products
        if product.get("insights") and product["insights"].get("sales_score") is not None
    ]
    average_sales_score = round(mean(sales_scores), 2) if sales_scores else None

    top_growing_products = [
        {
            "product_id": product["id"],
            "brand": product.get("brand"),
            "title": product.get("title"),
            "trend_score": product["insights"].get("trend_score"),
        }
        for product in products
        if product.get("insights") and product["insights"].get("trend_score") is not None
    ]
    top_growing_products.sort(key=lambda item: item["trend_score"], reverse=True)
    top_growing_products = top_growing_products[:3]

    total_keyword_volume = sum(
        keyword.get("volume", 0) or 0
        for product in products
        for keyword in product.get("keywords", [])
    )

    offer_gaps: List[float] = []
    lowest_offer: Dict[str, Any] | None = None
    for product in products:
        summary = product.get("offer_summary") or {}
        lowest_price = summary.get("lowest_price")
        highest_price = summary.get("highest_price")
        if lowest_price is not None and highest_price is not None:
            offer_gaps.append(float(highest_price) - float(lowest_price))
        for offer in product.get("offers", []):
            if lowest_offer is None or (
                offer.get("price") is not None
                and offer.get("price") < lowest_offer.get("price", float("inf"))
            ):
                lowest_offer = {
                    "product_id": product["id"],
                    "channel": offer.get("channel"),
                    "price": offer.get("price"),
                }

    average_price_gap = round(mean(offer_gaps), 2) if offer_gaps else None

    rfqs = fetch_rfqs(conn, limit=500)
    open_rfqs = sum(1 for rfq in rfqs if (rfq.get("status") or "").lower() == "open")
    supplier_ids = {
        supplier.get("id")
        for product in products
        for supplier in product.get("suppliers", [])
        if supplier.get("id") is not None
    }

    creative_mix = _summarize_creatives(
        creative for product in products for creative in product.get("creatives", [])
    )

    return {
        "overview": {
            "product_count": len(products),
            "average_sales_score": average_sales_score,
            "keyword_volume_total": total_keyword_volume,
        },
        "growth": {"top_growing_products": top_growing_products},
        "pricing": {
            "average_price_gap": average_price_gap,
            "lowest_offer": lowest_offer,
        },
        "sourcing": {
            "open_rfqs": open_rfqs,
            "supplier_coverage": len(supplier_ids),
        },
        "creative": {
            "channels": creative_mix["unique_channels"],
            "dominant_channels": creative_mix["dominant_channels"],
            "asset_count": creative_mix["asset_count"],
        },
    }


def build_product_playbook(conn: Connection, product_id: int) -> Dict[str, Any]:
    """Compose an actionable playbook for a specific product."""

    product = fetch_product(conn, product_id)
    if not product:
        raise ValueError("Product not found")

    review_summary = _summarize_reviews(product.get("reviews", []))
    keyword_summary = _summarize_keywords(product.get("keywords", []))
    creative_mix = _summarize_creatives(product.get("creatives", []))
    offer_summary = product.get("offer_summary") or {}

    price_gap = None
    lowest_price = offer_summary.get("lowest_price")
    highest_price = offer_summary.get("highest_price")
    if lowest_price is not None and highest_price is not None:
        price_gap = round(float(highest_price) - float(lowest_price), 2)

    rfqs = fetch_rfqs(conn, product_id=product_id, limit=200)
    open_rfqs = sum(1 for rfq in rfqs if (rfq.get("status") or "").lower() == "open")
    supplier_count = len(product.get("suppliers", []))

    if supplier_count == 0:
        sourcing_status = "no_suppliers"
    elif open_rfqs:
        sourcing_status = "negotiation"
    else:
        sourcing_status = "stable"

    campaign_angles = [f"Highlight {topic}" for topic in review_summary["top_topics"]]
    if not campaign_angles and product.get("insights"):
        strengths = (product["insights"].get("swot_json") or {}).get("strengths", [])
        campaign_angles = [f"Promote {strength}" for strength in strengths]

    next_best_actions: List[str] = []
    if review_summary["positive_ratio"] < 0.7:
        next_best_actions.append("Run review uplift initiatives")
    if keyword_summary["primary_terms"]:
        next_best_actions.append(
            f"Launch SEM campaigns around '{keyword_summary['primary_terms'][0]}'"
        )
    if open_rfqs:
        next_best_actions.append("Follow up on open RFQs")
    elif supplier_count < 2:
        next_best_actions.append("Expand supplier shortlist")
    if price_gap is not None and price_gap > 3:
        next_best_actions.append("Investigate premium pricing justification")

    swot = product.get("insights", {}).get("swot_json") or {}

    return {
        "product": {
            "id": product.get("id"),
            "brand": product.get("brand"),
            "title": product.get("title"),
            "category": product.get("category"),
        },
        "pricing": {
            "offer_summary": offer_summary,
            "price_gap": price_gap,
        },
        "sentiment": review_summary,
        "keywords": keyword_summary,
        "sourcing": {
            "supplier_count": supplier_count,
            "open_rfqs": open_rfqs,
            "status": sourcing_status,
        },
        "creative": {
            "recommended_channels": creative_mix["dominant_channels"],
            "asset_count": creative_mix["asset_count"],
            "angles": campaign_angles,
        },
        "actions": next_best_actions,
        "insight_focus": {
            "sales_score": product.get("insights", {}).get("sales_score"),
            "trend_score": product.get("insights", {}).get("trend_score"),
            "swot": swot,
        },
    }
