"""Reporting endpoints to share executive-ready deliverables."""

# Bu sayfa, rapor ve paylaşım katmanının API yüzeyini sunar.

from typing import List

from fastapi import APIRouter, Depends, HTTPException

from ..database import get_db
from ..utils.serializers import fetch_product

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/{product_id}")
def list_reports(product_id: int, db=Depends(get_db)) -> List[dict]:
    """Return generated reports associated with a product."""
    product = fetch_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product.get("reports", [])
