"""Endpoints delivering sentiment, trend, and opportunity analytics."""

# Bu sayfa, ürün içgörülerini tekil sorgularla sunan API uç noktalarını içerir.

from fastapi import APIRouter, Depends, HTTPException

from ..database import get_db
from ..utils.serializers import fetch_product

router = APIRouter(prefix="/insights", tags=["insights"])


@router.get("/{product_id}")
def get_insight(product_id: int, db=Depends(get_db)) -> dict:
    """Return insight record for a given product id."""
    product = fetch_product(db, product_id)
    if not product or not product.get("insights"):
        raise HTTPException(status_code=404, detail="Insight not available")
    return product["insights"]
