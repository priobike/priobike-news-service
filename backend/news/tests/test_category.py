from django.test import TestCase
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.utils.http import urlencode
import hashlib
from datetime import timedelta
import json

from news.models import Category, NewsArticle 
from news.tests.test_article import create_category_and_article

from news.models import Category, NewsArticle 
class CategoryTests(TestCase):
    def test_create_news_article_and_get_category_name(self):
        """ Test whether after creation of a category and news object the previously created category gets returned. """
        
        # Article:
        pub_date = timezone.now() - timedelta(days=1)
        article_text = "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis at vero eros et accumsan et iusto odio dignissim qui blandit praesent luptatum zzril delenit augue duis dolore te feugait nulla facilisi. Lorem ipsum dolor sit amet."
        article_title = "Lorem ipsum dolor sit amet, co"
        category_title = "Test131265"
        create_category_and_article(article_title=article_title, article_text=article_text, category_title=category_title, pub_date=pub_date)
        
        # Get article
        response_news_articles = self.client.get(reverse('news:news-articles'))
        response_dict = response_news_articles.json()
        
        # Get corresponding news object
        category_id = response_dict[0]['category_id']
        response_category = self.client.get(reverse('news:category', args=[category_id]))
        
        self.assertEqual(response_category.json()['title'], category_title)