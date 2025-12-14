# Subscription Billing API

Backend API for subscription-based billing using FastAPI, PostgreSQL, Stripe, and SMTP email.

## Features
- User registration
- Product management
- Multi-product subscriptions
- Stripe Checkout payments
- Secure Stripe webhooks
- Automatic confirmation emails
- Dockerized PostgreSQL

## Tech Stack
- FastAPI
- SQLAlchemy
- PostgreSQL (Docker)
- Stripe (Test mode)
- SMTP (Gmail)

## Setup
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
