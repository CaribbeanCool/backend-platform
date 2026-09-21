from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.product import ProductRepository
from app.repositories.product_cache import ProductCacheRepository
from app.schemas.product import (
    ProductCreate,
    ProductResponse,
    ProductUpdate,
)


class ProductService:
    @staticmethod
    def list_products(db: Session):
        return ProductRepository.get_all(db)

    @staticmethod
    def get_product(
        db: Session,
        product_id: int,
    ):
        cached_product = ProductCacheRepository.get(product_id)

        if cached_product is not None:
            print(f"CACHE HIT: product:{product_id}")
            return cached_product

        print(f"CACHE MISS: product:{product_id}")

        product = ProductRepository.get_by_id(
            db,
            product_id,
        )

        if product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found",
            )

        response = ProductResponse.model_validate(product)

        ProductCacheRepository.set(response)

        return response

    @staticmethod
    def create_product(
        db: Session,
        payload: ProductCreate,
    ):
        return ProductRepository.create(
            db,
            payload,
        )

    @staticmethod
    def update_product(
        db: Session,
        product_id: int,
        payload: ProductUpdate,
    ):
        product = ProductRepository.get_by_id(
            db,
            product_id,
        )

        if product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found",
            )

        updated_product = ProductRepository.update(
            db,
            product,
            payload,
        )

        ProductCacheRepository.delete(product_id)

        return updated_product

    @staticmethod
    def delete_product(
        db: Session,
        product_id: int,
    ):
        product = ProductRepository.get_by_id(
            db,
            product_id,
        )

        if product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found",
            )

        ProductRepository.delete(
            db,
            product,
        )

        ProductCacheRepository.delete(product_id)
