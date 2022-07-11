from django.test import TestCase
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.utils.http import urlencode
import hashlib
from datetime import timedelta
import json

from news_service_app.utils.serializer import serialize_article_to_dict
from news_service_app.models import Category, NewsArticle 


from news_service_app.models import Category, NewsArticle 
class CategoryTests(TestCase):
    def test_create_news_article_and_get_category_name(self):
        # Article:
        date = timezone.now().date() - timedelta(days=1)
        article_text = "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis at vero eros et accumsan et iusto odio dignissim qui blandit praesent luptatum zzril delenit augue duis dolore te feugait nulla facilisi. Lorem ipsum dolor sit amet."
        article_title = "Lorem ipsum dolor sit amet, co"
        category = Category.objects.create(title="Test131265")
        NewsArticle.objects.create(article_text=article_text, category=category, pub_date=date, article_title=article_title)
        
        # Get article
        response_news_articles = self.client.get(reverse('news_service_app:news-articles'))
        response_dict = response_news_articles.json()
        
        # Get corresponding news object
        category_id = response_dict[0]['category_id']
        response_category = self.client.get(reverse('news_service_app:category', args=[category_id]))
        
        self.assertEqual(response_category.json()['title'], "Test131265")