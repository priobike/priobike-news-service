import json

from django.core.exceptions import ValidationError
from django.forms.models import model_to_dict
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.generic import View

from news.models import Category, NewsArticle


class NewsResource(View):
    def get(self, _):        
        published_articles = NewsArticle.objects.filter(pub_date__lte=timezone.now())
        
        return JsonResponse(list(published_articles.values()), safe=False)

      
class CategoryResource(View):
    def get(self, _, category_id):
        try:
            category = get_object_or_404(Category, pk=category_id)
        except ValueError:
            return HttpResponseBadRequest(json.dumps({"error": "category_id needs to be an int"}))
        return JsonResponse(model_to_dict(category), safe=False)
