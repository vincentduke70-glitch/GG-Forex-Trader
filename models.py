from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.sql import func
from .db import Base

class Trade(Base):
    __tablename__ = "trades"
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(32), index=True, nullable=False)
    side = Column(String(8), nullable=False)
    outcome = Column(String(16), nullable=True)
    result_r = Column(Float, nullable=True)
    setup_tag = Column(String(120), nullable=True)
    notes = Column(Text, nullable=True)
    mode = Column(String(12), default="paper", nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class PaperOrder(Base):
    __tablename__ = "paper_orders"
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(32), nullable=False)
    side = Column(String(8), nullable=False)
    quantity_lots = Column(Float, nullable=False)
    entry_price = Column(Float, nullable=False)
    stop_loss = Column(Float, nullable=True)
    take_profit = Column(Float, nullable=True)
    status = Column(String(20), default="SIMULATED", nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
