import logging

from redis import RedisError

from app.cache import redis_client
from app.config import settings
from app.logging_context import request_id_context
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
                return None

            return ProductResponse.model_validate_json(cached)

        except RedisError:
            logger.exception(
                "Redis read failed for request_id=%s product_id=%s",
                request_id_context.get(),
                product_id,
            )

    @classmethod
    def set(cls, product: ProductResponse) -> None:
        try:
            redis_client.setex(
                cls._key(product.id),
                settings.cache_ttl_seconds,
                product.model_dump_json(),
            )
        except RedisError:
            logger.exception(
                "Redis write failed for request_id=%s product_id=%s",
                request_id_context.get(),
                product.id,
            )

    @classmethod
    def delete(cls, product_id: int) -> None:
        try:
            redis_client.delete(cls._key(product_id))
        except RedisError:
            logger.exception(
                "Redis delete failed for request_id=%s product_id=%s",
                request_id_context.get(),
                product_id,
            )
