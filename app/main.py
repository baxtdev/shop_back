from fastapi import FastAPI
from app.routers import user,product,order,blog
from app.admin import user as user_admin,order as order_admin, product as product_admin, blog as blog_admin
from app.api import auth
from app.db.session import engine

from fastapi_pagination import Page, add_pagination, paginate
from fastapi.responses import RedirectResponse
from sqladmin import Admin, ModelView


app = FastAPI()
admin = Admin(app, engine)

add_pagination(app)

app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(product.router, prefix="/products", tags=["products"])
app.include_router(order.router, prefix="/orders", tags=["orders"])
app.include_router(auth.router,prefix="/accounts",tags=["accounts"])
app.include_router(blog.router,prefix="/blog",tags=['blog'])

admin.add_view(user_admin.UserAdmin)
admin.add_view(product_admin.ProductAdmin)
admin.add_view(order_admin.OrderAdmin)
admin.add_view(order_admin.OrderProductAdmin)
admin.add_view(blog_admin.CategoryAdmin)
admin.add_view(blog_admin.NewsAdmin)



@app.get('/',status_code=301,include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")

