import stripe
import os
from fastapi import APIRouter, Request, HTTPException
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from app.database import SessionLocal
from app import models
from app.services.email_service import send_subscription_email

load_dotenv()

router = APIRouter(prefix="/webhooks", tags=["Webhooks"])

STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")

@router.post("/stripe")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            STRIPE_WEBHOOK_SECRET,
        )
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")
    except Exception:
        raise HTTPException(status_code=400, detail="Webhook error")

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        stripe_session_id = session["id"]

        db = SessionLocal()

        try:
            subscription = (
                db.query(models.Subscription)
                .filter(
                    models.Subscription.stripe_session_id
                    == stripe_session_id
                )
                .first()
            )

            if subscription:
                subscription.status = "paid"

                user = (
                    db.query(models.User)
                    .filter(models.User.id == subscription.user_id)
                    .first()
                )

                items = (
                    db.query(models.SubscriptionItem)
                    .filter(
                        models.SubscriptionItem.subscription_id
                        == subscription.id
                    )
                    .all()
                )

                products = []
                for item in items:
                    product = (
                        db.query(models.Product)
                        .filter(models.Product.id == item.product_id)
                        .first()
                    )
                    products.append(
                        {
                            "name": product.name,
                            "price": product.price,
                        }
                    )

                db.commit()

                send_subscription_email(
                    to_email=user.email,
                    user_name=user.full_name,
                    products=products,
                    total_amount=subscription.total_amount,
                    start_date=str(subscription.created_at.date()),
                )

        finally:
            db.close()


    return {"status": "success"}
