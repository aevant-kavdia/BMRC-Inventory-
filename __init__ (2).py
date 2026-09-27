from pydantic import BaseModel
from typing import Optional
from datetime import date

class ItemCreate(BaseModel):
    code: str
    description: str
    category: str
    unit: str
    reorder_level: int = 5
    initial_qty_central: float = 0
    initial_wac_usd: float = 0

class TransferCreate(BaseModel):
    std_number: str
    gate_pass: Optional[str] = None
    transfer_date: date
    from_store: str
    to_store: str
    item_code: str
    qty: float
    entered_by: str

class GRNCreate(BaseModel):
    grn_number: str
    invoice_ref: Optional[str] = None
    receipt_date: date
    supplier: str
    store: str
    item_code: str
    qty_received: float
    unit_cost_usd: float
    currency: str = "USD"
    boe_rate: Optional[float] = None

class ReturnCreate(BaseModel):
    item_code: str
    rig: str
    qty: float
    issue_date: date
    expected_return_date: date
    gate_pass: Optional[str] = None

class AIQuery(BaseModel):
    message: str
