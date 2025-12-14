from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/products", tags=["Products"])

@router.post(
    "",
    response_model=schemas.ProductResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_product(
    product: schemas.ProductCreate,
    db: Session = Depends(get_db),
):
    new_product = models.Product(
        name=product.name,
        description=product.description,
        price=product.price,
        is_active=product.is_active,
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product


@router.get(
    "",
    response_model=list[schemas.ProductResponse],
)
def list_products(
    db: Session = Depends(get_db),
):
    products = (
        db.query(models.Product)
        .filter(models.Product.is_active == True)
        .all()
    )
    return products
