from django.urls import path

from . import views

app_name = 'news'

urlpatterns = [
    path("articles", views.NewsResource.as_view(), name="news-articles"),
    path("category/<category_id>", views.CategoryResource.as_view(), name="category")
]
