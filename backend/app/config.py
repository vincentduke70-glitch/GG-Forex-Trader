import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./gg_forex.db")
TRADING_MODE = os.getenv("TRADING_MODE", "paper").lower()
ALLOWED_MODES = {"paper", "live"}
if TRADING_MODE not in ALLOWED_MODES:
    raise RuntimeError("TRADING_MODE must be 'paper' or 'live'")
# Live execution is deliberately not implemented in this starter.
