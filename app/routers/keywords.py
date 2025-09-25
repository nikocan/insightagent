"""Keyword mining and SEO intelligence API endpoints."""

# Bu sayfa, SEO ve anahtar kelime önerilerini ürün bazında sunar.

from typing import List

from fastapi import APIRouter, Depends, HTTPException

from ..database import get_db
from ..utils.serializers import fetch_product

router = APIRouter(prefix="/keywords", tags=["keywords"])


@router.get("/{product_id}")
def list_product_keywords(product_id: int, db=Depends(get_db)) -> List[dict]:
    """Return keywords associated with a product."""
    product = fetch_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product.get("keywords", [])
