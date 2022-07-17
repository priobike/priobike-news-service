import json

from django.core import serializers
from django.core.exceptions import ValidationError
from django.forms.models import model_to_dict
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.generic import View

from news.models import Category, NewsArticle


class NewsResource(View):
    def get(self, request):        
        last_sync_date = request.GET.get("from", None)

        published_articles = NewsArticle.objects.filter(pub_date__lte=timezone.now())
        if last_sync_date:
            try:
                published_articles = published_articles.filter(pub_date__gt=last_sync_date)
            except ValidationError:
                return HttpResponseBadRequest(json.dumps({"error": "Invalid date format."}))
        
        return JsonResponse(list(published_articles.values()), safe=False)

      
class CategoryResource(View):
    def get(self, request, category_id):
        category = get_object_or_404(Category, pk=category_id)
        return JsonResponse(model_to_dict(category), safe=False)
