"""API routes powering product discovery and intelligence experiences."""

# Bu sayfa, ürün zekâsı modülündeki arama ve detay isteklerini sayfalı şekilde
# sunmak için gerekli uç noktaları tanımlar.

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from ..database import get_db
from ..utils.serializers import fetch_all_products, fetch_product

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/")
def list_products(
    *,
    q: Optional[str] = Query(None, description="Arama terimi"),
    limit: int = Query(20, ge=1, le=100, description="Sayfa başına kayıt"),
    offset: int = Query(0, ge=0, description="Sayfa başlangıç sırası"),
    db=Depends(get_db),
) -> List[dict]:
    """Return paginated products optionally filtered by keyword search."""
    return fetch_all_products(db, search=q, limit=limit, offset=offset)


@router.get("/{product_id}")
def get_product(product_id: int, db=Depends(get_db)) -> dict:
    """Fetch a single product and raise 404 if not found."""
    product = fetch_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
