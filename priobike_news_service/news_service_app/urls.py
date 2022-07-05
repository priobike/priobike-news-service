from django.urls import path  

from . import views

app_name = 'news_service_app'

urlpatterns = [
    path("api/news", views.NewsResource.as_view(), name="news-articles"),
    path("api/category/<category_id>", views.CategoryResource.as_view(), name="categories")
]