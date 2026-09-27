from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db, Item
from models.schemas import ItemCreate
from datetime import date

router = APIRouter()

def item_status(i):
    total = i.qty_central + i.qty_mufulira + i.qty_nkana
    return "OUT" if total == 0 else ("LOW" if total <= i.reorder_level else "OK")

def to_out(i):
    d = {c.name: getattr(i, c.name) for c in i.__table__.columns}
    d["status"] = item_status(i)
    return d

@router.get("/")
def list_items(db: Session = Depends(get_db)):
    return [to_out(i) for i in db.query(Item).all()]

@router.post("/")
def create_item(payload: ItemCreate, db: Session = Depends(get_db)):
    if db.query(Item).filter(Item.code == payload.code).first():
        raise HTTPException(400, "Item code already exists")
    item = Item(
        code=payload.code, description=payload.description,
        category=payload.category, unit=payload.unit,
        reorder_level=payload.reorder_level,
        qty_central=payload.initial_qty_central,
        wac_usd=payload.initial_wac_usd
    )
    db.add(item); db.commit(); db.refresh(item)
    return to_out(item)

@router.get("/qr/{code}")
def qr_data(code: str, db: Session = Depends(get_db)):
    """Returns the JSON payload that gets embedded in QR codes."""
    i = db.query(Item).filter(Item.code == code).first()
    if not i:
        raise HTTPException(404, "Item not found")
    return {
        "code": i.code, "desc": i.description, "cat": i.category,
        "unit": i.unit, "wac": i.wac_usd,
        "central": i.qty_central, "mufulira": i.qty_mufulira, "nkana": i.qty_nkana,
        "generated": str(date.today())
    }

@router.get("/{code}")
def get_item(code: str, db: Session = Depends(get_db)):
    i = db.query(Item).filter(Item.code == code).first()
    if not i:
        raise HTTPException(404, "Item not found")
    return to_out(i)
