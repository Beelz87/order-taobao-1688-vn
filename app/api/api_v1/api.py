from app.api.api_v1.routers import accounts, auth, roles, user_roles, users, exchanges, stores, shipping_orders, \
    product_categories, deposit_bills
from fastapi import APIRouter

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(roles.router)
api_router.include_router(user_roles.router)
# api_router.include_router(accounts.router)
api_router.include_router(exchanges.router)
api_router.include_router(stores.router)
api_router.include_router(shipping_orders.router)
api_router.include_router(product_categories.router)
api_router.include_router(deposit_bills.router)