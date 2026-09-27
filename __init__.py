from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db, Return
from models.schemas import ReturnCreate
from datetime import date, timedelta

router = APIRouter()

def ret_status(r) -> str:
    today = date.today()
    if r.expected_return_date < today:
        return "overdue"
    if r.expected_return_date <= today + timedelta(days=3):
        return "due_soon"
    return "ok"

def to_out(r):
    d = {c.name: getattr(r, c.name) for c in r.__table__.columns}
    d["status"] = ret_status(r)
    return d

@router.get("/")
def list_returns(db: Session = Depends(get_db)):
    rows = db.query(Return).filter(Return.returned == False).all()
    return [to_out(r) for r in rows]

@router.post("/")
def add_return(payload: ReturnCreate, db: Session = Depends(get_db)):
    r = Return(**payload.model_dump())
    db.add(r); db.commit(); db.refresh(r)
    return to_out(r)

@router.patch("/{id}/close")
def close_return(id: int, db: Session = Depends(get_db)):
    r = db.query(Return).filter(Return.id == id).first()
    if not r:
        raise HTTPException(404, "Return record not found")
    r.returned = True
    db.commit()
    return {"message": "Marked as returned"}
