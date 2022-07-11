from django.forms.models import model_to_dict
from news_service_app.models import NewsArticle 

def serialize_article_to_dict(article: NewsArticle):
    article_dict = model_to_dict(article, fields=[field.name for field in article._meta.fields])
    article_dict = {"category_id" if k == 'category' else k: v.strftime("%Y-%m-%d") if k == 'pub_date' else v for k,v in article_dict.items()}
    return article_dict