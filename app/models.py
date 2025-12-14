from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    subscriptions = relationship("Subscription", back_populates="user")

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Integer, nullable=False)  # monthly price
    is_active = Column(Boolean, default=True)

class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    total_amount = Column(Integer, nullable=False)
    status = Column(String, default="pending")  # pending, paid, cancelled
    stripe_session_id = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="subscriptions")
    items = relationship("SubscriptionItem", back_populates="subscription")

class SubscriptionItem(Base):
    __tablename__ = "subscription_items"

    id = Column(Integer, primary_key=True, index=True)
    subscription_id = Column(
        Integer, ForeignKey("subscriptions.id"), nullable=False
    )
    product_id = Column(
        Integer, ForeignKey("products.id"), nullable=False
    )

    subscription = relationship("Subscription", back_populates="items")
    product = relationship("Product")
