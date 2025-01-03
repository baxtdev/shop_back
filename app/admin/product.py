from sqladmin import ModelView

from app.models.product import Product

class ProductAdmin(ModelView, model=Product):
    column_list = [Product.id, Product.name]
    