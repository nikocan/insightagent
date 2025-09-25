"""Endpoints orchestrating RFQ lifecycle for sourcing workflows."""

# Bu sayfa, tedarik RFQ süreçlerini listeleme, oluşturma ve durum güncelleme
# yetenekleriyle sunar.

import json
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from ..database import get_db
from ..utils.serializers import fetch_product, fetch_rfqs, fetch_supplier

router = APIRouter(prefix="/rfqs", tags=["rfqs"])


@router.get("/")
def list_rfqs(
    *,
    product_id: Optional[int] = Query(None, ge=1, description="Ürün kimliği"),
    supplier_id: Optional[int] = Query(None, ge=1, description="Tedarikçi kimliği"),
    status: Optional[str] = Query(None, description="Durum filtresi"),
    limit: int = Query(50, ge=1, le=200, description="Maksimum kayıt"),
    db=Depends(get_db),
) -> List[dict]:
    """Return RFQs filtered by sourcing context."""

    return fetch_rfqs(
        db,
        product_id=product_id,
        supplier_id=supplier_id,
        status=status,
        limit=limit,
    )


@router.post("/")
def create_rfq(
    payload: dict,
    db=Depends(get_db),
) -> dict:
    """Create a new RFQ record and return it."""

    payload = payload or {}
    product_id = payload.get("product_id")
    supplier_id = payload.get("supplier_id")
    if not product_id or not supplier_id:
        raise HTTPException(status_code=400, detail="product_id and supplier_id are required")

    if not fetch_product(db, product_id):
        raise HTTPException(status_code=404, detail="Product not found")
    if not fetch_supplier(db, supplier_id):
        raise HTTPException(status_code=404, detail="Supplier not found")

    status = payload.get("status", "open")
    quotes = payload.get("quotes")
    if isinstance(quotes, (dict, list)):
        quotes = json.dumps(quotes)
    db.execute(
        """
        INSERT INTO rfqs (product_id, supplier_id, status, quotes)
        VALUES (?, ?, ?, ?)
        """,
        (product_id, supplier_id, status, quotes),
    )
    db.commit()
    rfq_id = db.execute("SELECT last_insert_rowid() AS id").fetchone()["id"]
    row = db.execute("SELECT * FROM rfqs WHERE id = ?", (rfq_id,)).fetchone()
    return dict(row) if row else {}


@router.patch("/{rfq_id}")
def update_rfq(rfq_id: int, payload: dict, db=Depends(get_db)) -> dict:
    """Update RFQ status or quotes."""

    payload = payload or {}
    row = db.execute("SELECT * FROM rfqs WHERE id = ?", (rfq_id,)).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="RFQ not found")
    existing = dict(row)

    status = payload.get("status", existing["status"])
    quotes = payload.get("quotes", existing.get("quotes"))
    if isinstance(quotes, (dict, list)):
        quotes = json.dumps(quotes)

    db.execute(
        "UPDATE rfqs SET status = ?, quotes = ? WHERE id = ?",
        (status, quotes, rfq_id),
    )
    db.commit()
    row = db.execute("SELECT * FROM rfqs WHERE id = ?", (rfq_id,)).fetchone()
    return dict(row) if row else {}
