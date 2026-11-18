# GG Forex Trader — Professional Edition (starter implementation)

A responsive web trading workspace with a FastAPI backend, instrument-specific SNR analysis,
risk sizing, a persistent SQLite trade journal, and a transparent per-instrument learning
baseline. This is a development starter, **not a deployed or broker-connected trading service**.

## Included
- Responsive dashboard (static frontend served by FastAPI)
- Instrument watchlist: FX majors/crosses, XAUUSD, XAGUSD, indices and crypto symbols
- Candle upload/API contract and H4/H1/entry-timeframe SNR workflow
- Support/resistance zone detection from OHLC candles
- Risk calculator (pip/tick value supplied explicitly)
- Persistent trade journal
- Per-symbol performance summaries and candidate rule-review framework
- Paper-order endpoint (simulated only)
- Tests for risk and SNR utilities
- Docker Compose setup

## Quick start (Python 3.11+)
```bash
cd backend
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Open http://127.0.0.1:8000. API docs: http://127.0.0.1:8000/docs

## Docker
From the project root:
```bash
docker compose up --build
```

## Important limitations
1. Market prices in the initial dashboard are placeholders until a licensed market-data provider is configured.
2. Broker integration is intentionally not enabled. `paper` orders are simulated and never reach a broker.
3. The learning module is a transparent statistics-based baseline, not a trained autonomous AI model. It records results by instrument and surfaces candidates for out-of-sample testing.
4. Automatic strategy changes are allowed only in paper mode. Live strategy changes and live order execution must require explicit human approval.
5. No API keys, broker passwords, or account credentials belong in source code or browser storage.

## Next production steps
- Choose a broker and obtain its official API/MT5 integration details.
- Choose a licensed data feed and map broker-specific symbols/contracts.
- Add user authentication, roles, encrypted secret storage, audit logging and rate limits.
- Add robust candle storage, backtesting with spread/slippage/commission, walk-forward validation and paper forward-testing.
- Deploy behind HTTPS with backups, monitoring and secrets management.
- Perform independent security and trading-system testing before any live use.

## Initial strategy configuration
- Primary research pair: EURUSD
- H4: identify zones
- H1: setup/confirmation
- Entry timeframe: configurable (M15 default in UI)
- Initial risk target: 0.25% per trade
- Separate learning/performance history for every instrument
