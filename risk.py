def calculate_position_size(balance: float, risk_percent: float,
                             stop_distance: float, value_per_distance_per_lot: float):
    values = (balance, risk_percent, stop_distance, value_per_distance_per_lot)
    if any(v <= 0 for v in values):
        raise ValueError("All inputs must be positive")
    if risk_percent > 2:
        raise ValueError("Risk percent is capped at 2% by this calculator")
    risk_cash = balance * risk_percent / 100
    lots = risk_cash / (stop_distance * value_per_distance_per_lot)
    return {"risk_cash": round(risk_cash, 2), "estimated_lots": round(lots, 4)}
