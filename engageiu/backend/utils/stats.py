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


def percentile_ranks(scores: list[float]) -> list[dict]:
    """
    Compute the score at each of the four key percentile thresholds (P25, P50,
    P75, P90) using ceiling-index selection on the sorted score list:

        index = ceil((pct / 100) * n) - 1
        value = sorted_scores[index]

    Returns a list of 4 dicts ready to render directly in the frontend table.
    Edge-cases:
      - Empty list  → empty list
      - n < 4       → still computed (index is clamped to valid range)
      - All equal   → all ranges show the same value (correct behaviour)
    """
    if not scores:
        return []

    import math
    s = sorted(scores)
    n = len(s)
    score_min = int(s[0])
    score_max = int(s[-1])

    def at_pct(pct: int) -> int:
        idx = math.ceil((pct / 100) * n) - 1
        idx = max(0, min(idx, n - 1))
        return int(s[idx])

    p25 = at_pct(25)
    p50 = at_pct(50)
    p75 = at_pct(75)
    p90 = at_pct(90)

    return [
        {
            "label": "P25",
            "description": "Bottom quarter",
            "score_range": f"{score_min} \u2013 {p25} pts",
            "pct_range": "0 \u2013 25th pct",
        },
        {
            "label": "P50",
            "description": "Median half",
            "score_range": f"{p25} \u2013 {p50} pts",
            "pct_range": "25 \u2013 50th pct",
        },
        {
            "label": "P75",
            "description": "Top quarter",
            "score_range": f"{p50} \u2013 {p75} pts",
            "pct_range": "50 \u2013 75th pct",
        },
        {
            "label": "P90",
            "description": "Top 10%",
            "score_range": f"{p90}+ pts",
            "pct_range": "90th pct+",
        },
    ]


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
        label = f"{int(bucket_lo)}\u2013{int(bucket_hi)}"
        result.append({
            "bucket": label,
            "range": label,   # keep for backward compat with analytics.html
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
