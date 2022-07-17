from django.contrib import admin

from .models import Category, NewsArticle

class NewsArticleAdmin(admin.ModelAdmin):
    exclude = ('md5',)

admin.site.register(Category)
admin.site.register(NewsArticle, NewsArticleAdmin)