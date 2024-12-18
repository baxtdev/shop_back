from fastapi import FastAPI
from app.routers import user,product,order,blog
from app.api import auth
from fastapi_pagination import Page, add_pagination, paginate


app = FastAPI()
add_pagination(app)


app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(product.router, prefix="/products", tags=["products"])
app.include_router(order.router, prefix="/orders", tags=["orders"])
app.include_router(auth.router,prefix="/accounts",tags=["accounts"])
app.include_router(blog.router,prefix="/blog",tags=['blog'])
