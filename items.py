import os, json
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db, Item, Return
from models.schemas import AIQuery
from datetime import date, timedelta
import httpx

router = APIRouter()

@router.post("/chat")
async def ai_chat(payload: AIQuery, db: Session = Depends(get_db)):
    items = db.query(Item).all()
    open_returns = db.query(Return).filter(Return.returned == False).all()
    today = date.today()

    ctx = {
        "items": [{
            "code": i.code, "desc": i.description, "cat": i.category,
            "unit": i.unit, "wac_usd": i.wac_usd,
            "central": i.qty_central, "mufulira": i.qty_mufulira, "nkana": i.qty_nkana,
            "total": i.qty_central + i.qty_mufulira + i.qty_nkana,
            "status": ("OUT" if i.qty_central+i.qty_mufulira+i.qty_nkana == 0
                       else "LOW" if i.qty_central+i.qty_mufulira+i.qty_nkana <= i.reorder_level
                       else "OK")
        } for i in items],
        "overdue_returns": [
            {"item": r.item_code, "rig": r.rig, "due": str(r.expected_return_date)}
            for r in open_returns if r.expected_return_date < today
        ],
        "due_soon_returns": [
            {"item": r.item_code, "rig": r.rig, "due": str(r.expected_return_date)}
            for r in open_returns if today <= r.expected_return_date <= today + timedelta(days=3)
        ],
    }

    system = (
        "You are an inventory assistant for BMRC Tech Zambia Limited. "
        "Underground diamond core drilling stores at Mufulira and Nkana mine sites, Zambia. "
        f"Live inventory data: {json.dumps(ctx)}. "
        "Be concise, professional, data-driven. Use USD. Max 150 words unless a detailed report is requested."
    )

    api_key = os.getenv("ANTHROPIC_API_KEY", "")
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            "https://api.anthropic.com/v1/messages",
            headers={"x-api-key": api_key, "anthropic-version": "2023-06-01"},
            json={
                "model": "claude-sonnet-4-6",
                "max_tokens": 512,
                "system": system,
                "messages": [{"role": "user", "content": payload.message}]
            },
            timeout=30
        )
    return {"reply": resp.json()["content"][0]["text"]}
