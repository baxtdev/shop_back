from sqladmin import ModelView

from app.models.order import Order,OrderProduct


class OrderAdmin(ModelView, model=Order):
    column_list = [Order.id, Order.name]



class OrderProductAdmin(ModelView, model=OrderProduct):
    column_list = [OrderProduct.id, OrderProduct.order_id]