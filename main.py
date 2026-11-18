from pathlib import Path
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from .db import Base, engine, get_db
from .models import Trade, PaperOrder
from .schemas import RiskRequest, TradeCreate, PaperOrderCreate, Candle
from .risk import calculate_position_size
from .snr import detect_zones
from .learning import instrument_learning_summary
from .config import TRADING_MODE

Base.metadata.create_all(bind=engine)
app = FastAPI(title="GG Forex Trader API", version="0.1.0",
              description="Professional trading platform starter. Paper mode only.")
FRONTEND = Path(__file__).resolve().parents[2] / "frontend"
if not FRONTEND.exists():  # Docker layout: /app/app and /app/frontend
    FRONTEND = Path(__file__).resolve().parents[1] / "frontend"

INSTRUMENTS = [
    {"symbol": s, "category": c} for s, c in [
        ("EURUSD","forex"),("GBPUSD","forex"),("USDJPY","forex"),("AUDUSD","forex"),
        ("NZDUSD","forex"),("USDCAD","forex"),("USDCHF","forex"),("EURGBP","forex"),
        ("EURJPY","forex"),("GBPJPY","forex"),("XAUUSD","metals"),("XAGUSD","metals"),
        ("NAS100","index"),("US30","index"),("SPX500","index"),("BTCUSD","crypto"),("ETHUSD","crypto")
    ]
]

@app.get("/")
def home():
    return FileResponse(FRONTEND / "index.html")

@app.get("/api/health")
def health():
    return {"status": "ok", "mode": TRADING_MODE, "live_execution": False,
            "market_data": "not_connected", "broker": "not_connected"}

@app.get("/api/instruments")
def instruments():
    return INSTRUMENTS

@app.post("/api/risk/calculate")
def risk(req: RiskRequest):
    try:
        return calculate_position_size(req.balance, req.risk_percent, req.stop_distance,
                                       req.value_per_distance_per_lot)
    except ValueError as e:
        raise HTTPException(400, str(e))

@app.post("/api/analysis/snr/{symbol}/{timeframe}")
def snr(symbol: str, timeframe: str, candles: list[Candle]):
    if timeframe not in {"H4", "H1", "M15", "M5"}:
        raise HTTPException(400, "Supported timeframes: H4, H1, M15, M5")
    return {"symbol": symbol.upper(), "timeframe": timeframe,
            "analysis": detect_zones([c.model_dump() for c in candles])}

@app.post("/api/trades")
def create_trade(req: TradeCreate, db: Session = Depends(get_db)):
    trade = Trade(**req.model_dump(), mode="paper")
    db.add(trade); db.commit(); db.refresh(trade)
    return {"id": trade.id, "message": "Journal trade saved", "mode": "paper"}

@app.get("/api/trades")
def list_trades(db: Session = Depends(get_db)):
    rows = db.query(Trade).order_by(Trade.id.desc()).limit(250).all()
    return [{"id": t.id, "symbol": t.symbol, "side": t.side, "outcome": t.outcome,
             "result_r": t.result_r, "setup_tag": t.setup_tag, "notes": t.notes,
             "created_at": t.created_at} for t in rows]

@app.get("/api/learning")
def learning(db: Session = Depends(get_db)):
    rows = db.query(Trade).all()
    return instrument_learning_summary(rows)

@app.post("/api/orders/paper")
def paper_order(req: PaperOrderCreate, db: Session = Depends(get_db)):
    order = PaperOrder(**req.model_dump(), status="SIMULATED")
    db.add(order); db.commit(); db.refresh(order)
    return {"id": order.id, "status": "SIMULATED",
            "message": "Paper order recorded. No broker was contacted."}

@app.get("/api/orders/live/status")
def live_status():
    return {"enabled": False, "reason": "Broker integration, security review and explicit live approval are required."}
