from prometheus_client import Counter

cache_hits = Counter(
    "product_cache_hits_total",
    "Number of successful product cache hits",
)

cache_misses = Counter(
    "product_cache_misses_total",
    "Number of product cache misses",
)

cache_errors = Counter(
    "product_cache_errors_total",
    "Number of product cache operation errors",
    ["operation"],
)
