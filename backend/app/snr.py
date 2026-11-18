from statistics import median

def detect_zones(candles: list[dict], lookback: int = 120, tolerance_fraction: float = 0.0015):
    """Basic pivot-cluster S/R zones. Requires ordered OHLC candles; not a trade signal."""
    data = candles[-lookback:]
    if len(data) < 7:
        return {"support": [], "resistance": [], "note": "Need at least 7 candles"}
    highs, lows = [], []
    for i in range(2, len(data)-2):
        if data[i]["high"] >= max(x["high"] for x in data[i-2:i] + data[i+1:i+3]):
            highs.append(float(data[i]["high"]))
        if data[i]["low"] <= min(x["low"] for x in data[i-2:i] + data[i+1:i+3]):
            lows.append(float(data[i]["low"]))
    last = float(data[-1]["close"])
    def cluster(levels):
        groups = []
        for level in sorted(levels):
            if not groups or abs(level - median(groups[-1])) / max(abs(level), 1e-9) > tolerance_fraction:
                groups.append([level])
            else:
                groups[-1].append(level)
        return [{"low": round(min(g), 6), "high": round(max(g), 6),
                 "mid": round(median(g), 6), "touches": len(g)} for g in groups]
    support = [z for z in cluster(lows) if z["mid"] <= last]
    resistance = [z for z in cluster(highs) if z["mid"] >= last]
    return {"support": support[-5:], "resistance": resistance[:5],
            "last_close": last, "note": "Candidate zones only; confirm manually across H4/H1/entry timeframe."}
