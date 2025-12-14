from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    full_name: str
    email: EmailStr


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


class ProductCreate(BaseModel):
    name: str
    description: str | None = None
    price: int
    is_active: bool = True


class ProductResponse(BaseModel):
    id: int
    name: str
    description: str | None
    price: int
    is_active: bool

    class Config:
        from_attributes = True


class SubscriptionCreate(BaseModel):
    user_id: int
    product_ids: list[int]


class SubscriptionResponse(BaseModel):
    id: int
    user_id: int
    total_amount: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
