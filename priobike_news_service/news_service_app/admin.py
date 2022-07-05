from django.contrib import admin

from .models import Category, NewsArticle

admin.site.register(Category)
admin.site.register(NewsArticle)