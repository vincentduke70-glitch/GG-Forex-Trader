from collections import defaultdict

def instrument_learning_summary(trades):
    """Transparent per-symbol statistics; deliberately does not self-deploy strategy changes."""
    buckets = defaultdict(list)
    for t in trades:
        if t.result_r is not None:
            buckets[t.symbol.upper()].append(float(t.result_r))
    result = {}
    for symbol, rs in buckets.items():
        wins = sum(1 for r in rs if r > 0)
        losses = sum(1 for r in rs if r < 0)
        result[symbol] = {
            "sample_size": len(rs),
            "win_rate_percent": round(wins / len(rs) * 100, 1),
            "net_r": round(sum(rs), 2),
            "average_r": round(sum(rs) / len(rs), 3),
            "status": "collecting evidence" if len(rs) < 30 else "eligible for out-of-sample review",
            "warning": "Historical results do not guarantee future performance."
        }
    return result
