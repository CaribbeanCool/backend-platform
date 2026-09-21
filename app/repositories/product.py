from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


class ProductRepository:
    @staticmethod
    def get_all(db: Session) -> list[Product]:
        return list(db.scalars(select(Product)).all())

    @staticmethod
    def get_by_id(db: Session, product_id: int) -> Product | None:
        return db.get(Product, product_id)

    @staticmethod
    def create(db: Session, payload: ProductCreate) -> Product:
        product = Product(**payload.model_dump())

        db.add(product)
        db.commit()
        db.refresh(product)

        return product

    @staticmethod
    def update(
        db: Session,
        product: Product,
        payload: ProductUpdate,
    ) -> Product:
        data = payload.model_dump(exclude_unset=True)

        for field, value in data.items():
            setattr(product, field, value)

        db.commit()
        db.refresh(product)

        return product

    @staticmethod
    def delete(db: Session, product: Product) -> None:
        db.delete(product)
        db.commit()
