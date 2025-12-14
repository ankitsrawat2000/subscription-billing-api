from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import models
from app.services import stripe_service
import stripe

router = APIRouter(prefix="/payments", tags=["Payments"])

@router.post("/checkout")
def create_checkout_session(
    subscription_id: int,
    db: Session = Depends(get_db),
):
    subscription = (
        db.query(models.Subscription)
        .filter(models.Subscription.id == subscription_id)
        .first()
    )

    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")

    if subscription.status != "pending":
        raise HTTPException(
            status_code=400,
            detail="Subscription already paid or cancelled",
        )

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        mode="payment",
        line_items=[
            {
                "price_data": {
                    "currency": "inr",
                    "product_data": {
                        "name": f"Subscription #{subscription.id}"
                    },
                    "unit_amount": subscription.total_amount * 100,
                },
                "quantity": 1,
            }
        ],
        success_url="http://localhost:8000/payment-success",
        cancel_url="http://localhost:8000/payment-cancel",
    )

    subscription.stripe_session_id = session.id
    db.commit()

    return {
        "checkout_url": session.url,
        "stripe_session_id": session.id,
    }
