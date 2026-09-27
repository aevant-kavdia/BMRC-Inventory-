from core.database import init_db, SessionLocal, Item
init_db()
db = SessionLocal()
items = [
    Item(code="HQ-ROD-3M",     description="HQ Drill Rod 3m",              category="Drill Rods",   unit="Pcs",    reorder_level=10,  qty_central=45, qty_mufulira=12, qty_nkana=8,  wac_usd=85.50),
    Item(code="NQ-ROD-3M",     description="NQ Drill Rod 3m",              category="Drill Rods",   unit="Pcs",    reorder_level=15,  qty_central=30, qty_mufulira=18, qty_nkana=5,  wac_usd=62.00),
    Item(code="HQ-CBARREL",    description="HQ Core Barrel Assembly",      category="Core Barrels", unit="Sets",   reorder_level=3,   qty_central=6,  qty_mufulira=2,  qty_nkana=1,  wac_usd=340.00),
    Item(code="HQ-BIT-IMPREG", description="HQ Impregnated Diamond Bit",   category="Drill Bits",   unit="Pcs",    reorder_level=5,   qty_central=3,  qty_mufulira=1,  qty_nkana=0,  wac_usd=210.00),
    Item(code="NQ-OVERSHOT",   description="NQ Overshot Assembly",         category="Overshots",    unit="Pcs",    reorder_level=2,   qty_central=4,  qty_mufulira=1,  qty_nkana=2,  wac_usd=180.00),
    Item(code="HQ-OVERSHOT",   description="HQ Overshot Assembly",         category="Overshots",    unit="Pcs",    reorder_level=2,   qty_central=2,  qty_mufulira=0,  qty_nkana=1,  wac_usd=195.00),
    Item(code="DRILL-GREASE",  description="Drilling Grease 5kg",          category="Consumables",  unit="Kg",     reorder_level=20,  qty_central=35, qty_mufulira=10, qty_nkana=12, wac_usd=8.20),
    Item(code="FLUSH-OIL",     description="Flush Oil (Biodegradable) 20L",category="Consumables",  unit="Litres", reorder_level=100, qty_central=80, qty_mufulira=20, qty_nkana=15, wac_usd=3.50),
    Item(code="PQ-CASING",     description="PQ Casing 1.5m",               category="Casing",       unit="Pcs",    reorder_level=5,   qty_central=0,  qty_mufulira=0,  qty_nkana=2,  wac_usd=120.00),
    Item(code="SAFETY-GLOVES", description="Safety Gloves Pair",           category="Consumables",  unit="Pcs",    reorder_level=30,  qty_central=48, qty_mufulira=15, qty_nkana=20, wac_usd=4.50),
]
for item in items:
    if not db.query(Item).filter(Item.code == item.code).first():
        db.add(item)
db.commit()
print(f"Seeded {len(items)} items.")
