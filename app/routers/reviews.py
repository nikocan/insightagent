"""Endpoints exposing review sentiment and topic intelligence."""

# Bu sayfa, kullanıcı yorumlarını skor ve konu filtreleriyle sunar.

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from ..database import get_db
from ..utils.serializers import fetch_product, fetch_reviews

router = APIRouter(prefix="/reviews", tags=["reviews"])


@router.get("/")
def list_reviews(
    *,
    product_id: Optional[int] = Query(None, ge=1, description="Ürün kimliği"),
    min_rating: Optional[float] = Query(None, ge=0, le=5, description="Minimum puan"),
    limit: int = Query(50, ge=1, le=200, description="Maksimum kayıt"),
    db=Depends(get_db),
) -> List[dict]:
    """Return reviews filtered by rating threshold."""

    return fetch_reviews(db, product_id=product_id, min_rating=min_rating, limit=limit)


@router.get("/highlights/{product_id}")
def review_highlights(product_id: int, db=Depends(get_db)) -> dict:
    """Return quick sentiment highlights for UI badges."""

    product = fetch_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    reviews = product.get("reviews", [])
    if not reviews:
        raise HTTPException(status_code=404, detail="No reviews captured")

    positive = [r for r in reviews if (r.get("sentiment") or "").lower() == "positive"]
    negative = [r for r in reviews if (r.get("sentiment") or "").lower() == "negative"]

    return {
        "total": len(reviews),
        "positive_ratio": round(len(positive) / len(reviews), 2),
        "negative_ratio": round(len(negative) / len(reviews), 2),
        "recent_topics": next(iter((reviews[0].get("topics") or [])), None),
    }
