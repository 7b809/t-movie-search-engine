from cachetools import TTLCache

search_cache = TTLCache(
    maxsize=1000,
    ttl=600
)