from app.cache import redis_client
from app.config import settings
from app.schemas.product import ProductResponse


class ProductCacheRepository:
    @staticmethod
    def _key(product_id: int) -> str:
        return f"product:{product_id}"

    @classmethod
    def get(
        cls,
        product_id: int,
    ) -> ProductResponse | None:
        cached = redis_client.get(cls._key(product_id))

        if cached is None:
            return None

        return ProductResponse.model_validate_json(cached)

    @classmethod
    def set(
        cls,
        product: ProductResponse,
    ) -> None:
        redis_client.setex(
            cls._key(product.id),
            settings.cache_ttl_seconds,
            product.model_dump_json(),
        )

    @classmethod
    def delete(
        cls,
        product_id: int,
    ) -> None:
        redis_client.delete(cls._key(product_id))
