from app.risk import calculate_position_size
from app.snr import detect_zones

def test_risk_025_percent():
    result = calculate_position_size(1000, 0.25, 20, 10)
    assert result["risk_cash"] == 2.5
    assert result["estimated_lots"] == 0.0125

def test_snr_needs_enough_candles():
    assert "note" in detect_zones([{"high": 2, "low": 1, "close": 1.5}] * 5)
