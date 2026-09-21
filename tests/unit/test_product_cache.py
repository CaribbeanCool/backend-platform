from unittest.mock import patch

from redis import RedisError

from app.repositories.product_cache import ProductCacheRepository
from app.schemas.product import ProductResponse


def test_cache_get_returns_none_when_redis_fails():
    with patch(
        "app.repositories.product_cache.redis_client.get",
        side_effect=RedisError("Redis unavailable"),
    ):
        result = ProductCacheRepository.get(1)

    assert result is None


def test_cache_set_does_not_raise_when_redis_fails():
    product = ProductResponse(
        id=1,
        name="Keyboard",
        description="Mechanical keyboard",
    )

    with patch(
        "app.repositories.product_cache.redis_client.setex",
        side_effect=RedisError("Redis unavailable"),
    ):
        ProductCacheRepository.set(product)
