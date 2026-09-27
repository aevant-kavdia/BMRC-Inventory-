from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db, Item, Transfer
from core.wac import STORE_FIELD
from models.schemas import TransferCreate

router = APIRouter()

@router.get("/")
def list_transfers(db: Session = Depends(get_db)):
    return db.query(Transfer).order_by(Transfer.id.desc()).all()

@router.post("/")
def create_transfer(payload: TransferCreate, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.code == payload.item_code).first()
    if not item:
        raise HTTPException(404, "Item not found")

    src = STORE_FIELD.get(payload.from_store.lower())
    dst = STORE_FIELD.get(payload.to_store.lower())

    if src:
        cur = getattr(item, src)
        if cur < payload.qty:
            raise HTTPException(400, f"Insufficient stock in {payload.from_store} ({cur} available)")
        setattr(item, src, cur - payload.qty)

    if dst:
        setattr(item, dst, getattr(item, dst) + payload.qty)

    t = Transfer(**payload.model_dump())
    db.add(t); db.commit(); db.refresh(t)
    return t
