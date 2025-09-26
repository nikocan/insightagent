"""Endpoints delivering portfolio dashboards and product playbooks."""

# Bu sayfa, portföy genelindeki performans özetleri ile ürün özelinde aksiyon
# planları sunan analitik API uç noktalarını açıklar.

from fastapi import APIRouter, Depends, HTTPException

from ..database import get_db
from ..services.analytics import build_portfolio_dashboard, build_product_playbook

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/dashboard")
def get_portfolio_dashboard(db=Depends(get_db)) -> dict:
    """Return cross-product portfolio metrics."""

    return build_portfolio_dashboard(db)


@router.get("/products/{product_id}/playbook")
def get_product_playbook(product_id: int, db=Depends(get_db)) -> dict:
    """Return a strategic playbook for the given product."""

    try:
        return build_product_playbook(db, product_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
