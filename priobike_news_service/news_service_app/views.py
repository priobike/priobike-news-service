from unicodedata import category
from django.http import  JsonResponse
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from django.utils import timezone
import hashlib
from datetime import datetime, timedelta
import json

from news_service_app.models import Category, NewsArticle 

def cross_origin(response):
    response["Access-Control-Allow-Origin"] = "*"
    return response

@method_decorator(csrf_exempt, name='dispatch')
class NewsResource(View):
    def get(self, request):
        
        params = request.GET
        client_md5_hash = params.get("hash", None)
        last_sync_date = params.get("last_sync_date", None)
        
        if client_md5_hash is not None and last_sync_date is not None:  
            date = datetime.strptime(last_sync_date, "%Y-%m-%d").date()
            
            old_articles = list(NewsArticle.objects.filter(pub_date__lte=date).values())
            old_artilces_json = json.dump(old_articles)
            old_articles_md5_hash = hashlib.md5(old_artilces_json.encode('utf-8')).hexdigest()
            
            if client_md5_hash != old_articles_md5_hash:
                all_articles = list(NewsArticle.objects.filter(pub_date__lte=timezone.now().date()).values())
                return cross_origin(JsonResponse(all_articles, safe=False))
            else:
                date = date - timedelta(days=1)
                new_articles = list(NewsArticle.objects.filter(pub_date__gt=date, pub_date__lte=timezone.now().date()).values())
                return cross_origin(JsonResponse(new_articles, safe=False))
        else:
            articles = list(NewsArticle.objects.filter(pub_date__lte=timezone.now().date()).values())
            return cross_origin(JsonResponse(articles, safe=False))
        
@method_decorator(csrf_exempt, name='dispatch')
class CategoryResource(View):
    def get(self, request, category_id):
        category = get_object_or_404(Category, pk=category_id)
        return cross_origin(JsonResponse(model_to_dict(category), safe=False))