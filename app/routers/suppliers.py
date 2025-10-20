"""Sourcing and procurement APIs including RFQ orchestration."""

# Bu sayfa, tedarikçi kataloglarını ve RFQ ilişkilerini listeleyen uç noktaları sunar.

from typing import List

from fastapi import APIRouter, Depends, HTTPException

from ..database import get_db
from ..utils.serializers import fetch_product, fetch_supplier, rows_to_dicts

router = APIRouter(prefix="/suppliers", tags=["suppliers"])


@router.get("/")
def list_suppliers(db=Depends(get_db)) -> List[dict]:
    """Return all suppliers in the catalog."""
    return rows_to_dicts(db.execute("SELECT * FROM suppliers").fetchall())


@router.get("/{supplier_id}")
def get_supplier(supplier_id: int, db=Depends(get_db)) -> dict:
    """Fetch a single supplier record."""
    supplier = fetch_supplier(db, supplier_id)
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return supplier


@router.get("/{supplier_id}/rfqs")
def list_supplier_rfqs(supplier_id: int, db=Depends(get_db)) -> List[dict]:
    """List RFQs sent to a specific supplier."""
    supplier = fetch_supplier(db, supplier_id)
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return supplier.get("rfqs", [])


@router.get("/by-product/{product_id}")
def list_suppliers_by_product(product_id: int, db=Depends(get_db)) -> List[dict]:
    """Return suppliers mapped to a given product id."""
    product = fetch_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product.get("suppliers", [])
