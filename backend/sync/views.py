import json

from django.conf import settings
from django.db.transaction import atomic
from django.http import HttpResponseBadRequest, JsonResponse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from news.models import Category, NewsArticle


@method_decorator(csrf_exempt, name='dispatch')
class SyncResource(View):
    def post(self, request):        
        # Check that the sync key is correct.
        try:
            body = json.loads(request.body)
        except json.JSONDecodeError:
            print("Invalid JSON.")
            return HttpResponseBadRequest(json.dumps({"error": "Invalid JSON."}))

        sync_key = body.get("key")
        if sync_key != settings.SYNC_KEY:
            print(f"Invalid key: {sync_key}")
            return HttpResponseBadRequest(json.dumps({"error": "Invalid key."}))
        
        if not isinstance(body.get("categories"), list) or not isinstance(body.get("articles"), list):
            print(f"Invalid data format: {body}")
            return HttpResponseBadRequest(json.dumps({"error": "Invalid data format."}))

        with atomic():
            # Clear the database
            Category.objects.all().delete()
            NewsArticle.objects.all().delete()

            # Load the categories contained in the response.
            categories = body.get("categories")
            for category in categories:
                title = category.get("title")
                try:
                    _, created = Category.objects.get_or_create(title=title)
                    if created:
                        print(f"Created category: {title}")
                except Exception as err:
                    print(f"Error during sync: {err}")
                    return JsonResponse({"status": "error"})

            # Load the articles contained in the response.
            articles = body.get("articles")
            for article in articles:
                category_title = article.get("category")
                article_title = article.get("title")
                if category_title:
                    category = Category.objects.get(title=category_title)
                else:
                    category = None
                try:
                    _, created = NewsArticle.objects.get_or_create(
                        text=article.get("text"),
                        title=article_title, 
                        pub_date=timezone.datetime.fromisoformat(article.get("pubDate")), 
                        category=category,
                    )
                except Exception as err:
                    print(f"Error during sync: {err}")
                    return JsonResponse({"status": "error"})
                if created:
                    print(f"Created article: {article_title}")
        
        return JsonResponse({"status": "ok"})