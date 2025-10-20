"""Ad Studio API uç noktaları kreatif planlama ve uyum içgörülerini sunar."""

# Bu router, kampanya briflerini, uyum rehberlerini ve varyasyon üretimini
# FastAPI üzerinden istemcilere sağlar.

from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException

from ..database import get_db
from ..services.adstudio import (
    assemble_brief_payload,
    assemble_compliance_payload,
    generate_variations,
)

router = APIRouter(prefix="/adstudio", tags=["adstudio"])


@router.get("/briefs/{product_id}")
def get_creative_brief(product_id: int, db=Depends(get_db)) -> Dict[str, Any]:
    """Return the enriched creative brief for a product."""

    try:
        return assemble_brief_payload(db, product_id)
    except ValueError as exc:  # pragma: no cover - defensive
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/compliance/{product_id}")
def get_compliance(product_id: int, db=Depends(get_db)) -> Dict[str, Any]:
    """Return the compliance guidance for a product."""

    try:
        return assemble_compliance_payload(db, product_id)
    except ValueError as exc:  # pragma: no cover - defensive
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/variations")
def post_variations(payload: Dict[str, Any], db=Depends(get_db)) -> Dict[str, Any]:
    """Generate ad copy variations from the provided brief context."""

    product_id = payload.get("product_id")
    channel = payload.get("channel")
    if product_id is None or channel is None:
        raise HTTPException(status_code=422, detail="product_id and channel are required")

    variation_count = int(payload.get("variation_count", 3))
    tone = payload.get("tone")
    format_hint = payload.get("format_hint")

    try:
        return generate_variations(
            db,
            product_id=int(product_id),
            channel=str(channel),
            tone=str(tone) if tone else None,
            format_hint=str(format_hint) if format_hint else None,
            variation_count=max(1, min(5, variation_count)),
        )
    except ValueError as exc:  # pragma: no cover - defensive
        raise HTTPException(status_code=404, detail=str(exc)) from exc
