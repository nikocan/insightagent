"""Endpoints that surface offer and pricing intelligence."""

# Bu sayfa, fiyat ve stok sinyallerini kanal bazlı filtrelerle listeleyen
# uç noktaları içerir.

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from ..database import get_db
from ..utils.serializers import fetch_offers, fetch_product, summarize_offers

router = APIRouter(prefix="/offers", tags=["offers"])


@router.get("/")
def list_offers(
    *,
    product_id: Optional[int] = Query(None, ge=1, description="Ürün kimliği filtresi"),
    channel: Optional[str] = Query(None, description="Pazar yeri veya kanal adı"),
    limit: int = Query(50, ge=1, le=200, description="Döndürülecek maksimum kayıt"),
    db=Depends(get_db),
) -> List[dict]:
    """Return recent offers with optional filtering."""

    return fetch_offers(db, product_id=product_id, channel=channel, limit=limit)


@router.get("/snapshot/{product_id}")
def offer_snapshot(product_id: int, db=Depends(get_db)) -> dict:
    """Provide summary pricing stats for a product."""

    product = fetch_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    summary = summarize_offers(product.get("offers", []))
    if not summary:
        raise HTTPException(status_code=404, detail="No offers recorded")
    return summary
