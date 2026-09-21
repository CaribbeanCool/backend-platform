from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models.user import User
from app.schemas.product import (
    ProductCreate,
    ProductResponse,
    ProductUpdate,
)
from app.services.product import ProductService

router = APIRouter(
    prefix="/api/v1/products",
    tags=["products"],
)


@router.get("", response_model=list[ProductResponse])
def list_products(db: Session = Depends(get_db)):
    return ProductService.list_products(db)


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
):
    return ProductService.get_product(db, product_id)


@router.post(
    "",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_product(
    payload: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ProductService.create_product(
        db,
        payload,
    )


@router.patch("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    payload: ProductUpdate,
    db: Session = Depends(get_db),
):
    return ProductService.update_product(
        db,
        product_id,
        payload,
    )


@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
):
    ProductService.delete_product(db, product_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
