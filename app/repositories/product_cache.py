import logging

from redis import RedisError

from app.cache import redis_client
from app.config import settings
from app.logging_context import request_id_context
from app.metrics import cache_errors, cache_hits, cache_misses
from app.schemas.product import ProductResponse

logger = logging.getLogger(__name__)


class ProductCacheRepository:
    @staticmethod
    def _key(product_id: int) -> str:
        return f"product:{product_id}"

    @classmethod
    def get(cls, product_id: int) -> ProductResponse | None:
        try:
            cached = redis_client.get(cls._key(product_id))

            if cached is None:
                cache_misses.inc()
                return None

            cache_hits.inc()

            return ProductResponse.model_validate_json(cached)

        except RedisError:
            cache_errors.labels(operation="get").inc()

            logger.exception(
                "Redis read failed request_id=%s product_id=%s",
                request_id_context.get(),
                product_id,
            )

            return None

    @classmethod
    def set(cls, product: ProductResponse) -> None:
        try:
            redis_client.setex(
                cls._key(product.id),
                settings.cache_ttl_seconds,
                product.model_dump_json(),
            )

        except RedisError:
            cache_errors.labels(operation="set").inc()

            logger.exception(
                "Redis write failed request_id=%s product_id=%s",
                request_id_context.get(),
                product.id,
            )

    @classmethod
    def delete(cls, product_id: int) -> None:
        try:
            redis_client.delete(cls._key(product_id))

        except RedisError:
            cache_errors.labels(operation="delete").inc()

            logger.exception(
                "Redis delete failed request_id=%s product_id=%s",
                request_id_context.get(),
                product_id,
            )
