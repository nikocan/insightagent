"""Advertising studio endpoints for copy and asset orchestration."""

# Bu sayfa, Ad Studio üretimlerini listeleyen uç noktaları içerir.

from typing import List

from fastapi import APIRouter, Depends, HTTPException

from ..database import get_db
from ..utils.serializers import fetch_product

router = APIRouter(prefix="/creatives", tags=["creatives"])


@router.get("/{product_id}")
def list_creatives(product_id: int, db=Depends(get_db)) -> List[dict]:
    """List creative assets generated for a product."""
    product = fetch_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product.get("creatives", [])
