from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db, Item, GRN
from core.wac import recalc_wac, STORE_FIELD
from models.schemas import GRNCreate

router = APIRouter()

@router.get("/")
def list_grns(db: Session = Depends(get_db)):
    return db.query(GRN).order_by(GRN.id.desc()).all()

@router.post("/")
def post_grn(payload: GRNCreate, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.code == payload.item_code).first()
    if not item:
        raise HTTPException(404, "Item not found")

    sf = STORE_FIELD.get(payload.store.lower())
    if not sf:
        raise HTTPException(400, "Invalid store name")

    # ZMW → USD conversion using Bank of Zambia rate
    cost_usd = payload.unit_cost_usd
    if payload.currency == "ZMW" and payload.boe_rate:
        cost_usd = payload.unit_cost_usd / payload.boe_rate

    old_qty = getattr(item, sf)
    new_wac = recalc_wac(old_qty, item.wac_usd, payload.qty_received, cost_usd)

    setattr(item, sf, old_qty + payload.qty_received)
    item.wac_usd = new_wac

    g = GRN(**payload.model_dump(), new_wac_usd=new_wac)
    db.add(g); db.commit(); db.refresh(g)
    return g
