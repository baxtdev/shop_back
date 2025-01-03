from sqladmin import ModelView

from app.models.blog import News,Category


class CategoryAdmin(ModelView, model=Category):
    column_list = [Category.id, Category.name]


class NewsAdmin(ModelView, model=News):
    column_list = [News.id, News.name, Category.name]