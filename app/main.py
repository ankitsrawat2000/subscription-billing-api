from fastapi import FastAPI
from app.database import engine
from app import models
from app.routes.users import router as user_router
from app.routes.products import router as product_router
from app.routes.subscriptions import router as subscription_router
from app.routes.payments import router as payment_router
from app.routes.webhooks import router as webhook_router

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(user_router)
app.include_router(product_router)
app.include_router(subscription_router)
app.include_router(payment_router)
app.include_router(webhook_router)


@app.get("/")
def root():
    return {"message": "User API ready"}