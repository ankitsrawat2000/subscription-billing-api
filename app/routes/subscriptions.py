from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/subscriptions", tags=["Subscriptions"])

@router.post(
    "",
    response_model=schemas.SubscriptionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_subscription(
    data: schemas.SubscriptionCreate,
    db: Session = Depends(get_db),
):
    user = (
        db.query(models.User)
        .filter(models.User.id == data.user_id)
        .first()
    )
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    products = (
        db.query(models.Product)
        .filter(
            models.Product.id.in_(data.product_ids),
            models.Product.is_active == True,
        )
        .all()
    )

    if len(products) != len(data.product_ids):
        raise HTTPException(
            status_code=400,
            detail="One or more products are invalid or inactive",
        )

    total_amount = sum(product.price for product in products)

    subscription = models.Subscription(
        user_id=user.id,
        total_amount=total_amount,
        status="pending",
    )

    db.add(subscription)
    db.commit()
    db.refresh(subscription)

    for product in products:
        item = models.SubscriptionItem(
            subscription_id=subscription.id,
            product_id=product.id,
        )
        db.add(item)

    db.commit()

    return subscription
