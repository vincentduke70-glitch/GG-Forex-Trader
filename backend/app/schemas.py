from pydantic import BaseModel, Field
from typing import Literal

class Candle(BaseModel):
    timestamp: str
    open: float
    high: float
    low: float
    close: float
    volume: float | None = None

class RiskRequest(BaseModel):
    balance: float = Field(gt=0)
    risk_percent: float = Field(gt=0, le=2)
    stop_distance: float = Field(gt=0, description="Pips or points")
    value_per_distance_per_lot: float = Field(gt=0, description="Broker-specific value in account currency")

class TradeCreate(BaseModel):
    symbol: str
    side: Literal["buy", "sell"]
    outcome: Literal["win", "loss", "break_even"] | None = None
    result_r: float | None = None
    setup_tag: str | None = None
    notes: str | None = None

class PaperOrderCreate(BaseModel):
    symbol: str
    side: Literal["buy", "sell"]
    quantity_lots: float = Field(gt=0)
    entry_price: float = Field(gt=0)
    stop_loss: float | None = None
    take_profit: float | None = None
