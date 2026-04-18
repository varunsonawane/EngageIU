"""
Pure-Python statistics — no external libraries (statistics, numpy, scipy).
Implements all metrics required by the case PDF plus grad-team extras.
"""
from __future__ import annotations


def _sorted(values: list[float]) -> list[float]:
    return sorted(values)


def mean(values: list[float]) -> float:
    if not values:
        return 0.0
    return sum(values) / len(values)


def median(values: list[float]) -> float:
    if not values:
        return 0.0
    s = _sorted(values)
    n = len(s)
    mid = n // 2
    if n % 2 == 1:
        return float(s[mid])
    return (s[mid - 1] + s[mid]) / 2.0


def quartiles(values: list[float]) -> tuple[float, float, float]:
    """Return (Q1, median, Q3) using the inclusive method."""
    if not values:
        return 0.0, 0.0, 0.0
    s = _sorted(values)
    n = len(s)

    def _percentile(data: list[float], pct: float) -> float:
        """Linear interpolation percentile."""
        if not data:
            return 0.0
        idx = pct / 100.0 * (len(data) - 1)
        lo = int(idx)
        hi = lo + 1
        if hi >= len(data):
            return float(data[lo])
        frac = idx - lo
        return data[lo] + frac * (data[hi] - data[lo])

    q1 = _percentile(s, 25)
    med = _percentile(s, 50)
    q3 = _percentile(s, 75)
    return q1, med, q3


def std_deviation(values: list[float]) -> float:
    """Population standard deviation."""
    if len(values) < 2:
        return 0.0
    m = mean(values)
    variance = sum((x - m) ** 2 for x in values) / len(values)
    return variance ** 0.5


def percentile_ranks(values: list[float]) -> list[dict]:
    """
    For each value, return its percentile rank within the list.
    percentile_rank = (number of values < x) / n * 100
    """
    if not values:
        return []
    n = len(values)
    result = []
    for v in values:
        count_below = sum(1 for x in values if x < v)
        pct = round(count_below / n * 100, 1)
        result.append({"score": v, "percentile_rank": pct})
    return result


def score_distribution(values: list[float], num_buckets: int = 5) -> list[dict]:
    """
    Bucket scores into `num_buckets` equal-width intervals.
    Returns list of { range_label, count, percentage }.
    """
    if not values:
        return []
    lo = min(values)
    hi = max(values)
    if lo == hi:
        return [{"range": f"{int(lo)}", "count": len(values), "percentage": 100.0}]

    bucket_size = (hi - lo) / num_buckets
    buckets: list[int] = [0] * num_buckets

    for v in values:
        idx = int((v - lo) / bucket_size)
        if idx >= num_buckets:
            idx = num_buckets - 1
        buckets[idx] += 1

    n = len(values)
    result = []
    for i, count in enumerate(buckets):
        bucket_lo = lo + i * bucket_size
        bucket_hi = lo + (i + 1) * bucket_size
        result.append({
            "range": f"{int(bucket_lo)}–{int(bucket_hi)}",
            "count": count,
            "percentage": round(count / n * 100, 1),
        })
    return result


def full_stats(scores: list[float]) -> dict:
    """Compute all statistics required by the case (basic + grad extras)."""
    if not scores:
        return {
            "count": 0,
            "mean": 0.0,
            "median": 0.0,
            "q1": 0.0,
            "q3": 0.0,
            "min": 0.0,
            "max": 0.0,
            "std_deviation": 0.0,
            "percentile_ranks": [],
            "score_distribution": [],
        }

    q1, med, q3 = quartiles(scores)
    return {
        "count": len(scores),
        "mean": round(mean(scores), 2),
        "median": round(med, 2),
        "q1": round(q1, 2),
        "q3": round(q3, 2),
        "min": min(scores),
        "max": max(scores),
        "std_deviation": round(std_deviation(scores), 2),
        "percentile_ranks": percentile_ranks(scores),
        "score_distribution": score_distribution(scores),
    }
