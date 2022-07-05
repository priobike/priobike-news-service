from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.forms.models import model_to_dict

from datetime import timedelta

from news_service_app.models import Category, NewsArticle 

def newsarticle_to_dict(article):
    return

class CategoryModelTests(TestCase):
    def test_only_return_news_articles_that_are_not_in_future(self):
        date = timezone.now().date() + timedelta(days=1)
        article_text = "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis at vero eros et accumsan et iusto odio dignissim qui blandit praesent luptatum zzril delenit augue duis dolore te feugait nulla facilisi. Lorem ipsum dolor sit amet."
        article_title = "Lorem ipsum dolor sit amet, co"
        
        category = Category.objects.create(title="Test")
        NewsArticle.objects.create(article_text=article_text, category=category, pub_date=date, article_title=article_title)
        
        response = self.client.get(reverse('news_service_app:news-articles'))
        self.assertQuerysetEqual(response.json(), [])
        
        date = timezone.now().date() - timedelta(days=1)
        article_text = "Lorem ipsum dolor sitdunt nsetetur sadiodio dignissim qui blandit praesent luptatum zzril delenit augue duis dolore te feugait nulla facilisi. Lorem ipsum dolor sit amet."
        article_title = "Lorit amet, co"
        
        category = Category.objects.create(title="Test5")
        article = NewsArticle.objects.create(article_text=article_text, category=category, pub_date=date, article_title=article_title)
        
        response = self.client.get(reverse('news_service_app:news-articles'))
        
        article_dict = model_to_dict(article, fields=[field.name for field in article._meta.fields])
        article_dict = {"category_id" if k == 'category' else k: v.strftime("%Y-%m-%d") if k == 'pub_date' else v for k,v in article_dict.items()}
        self.assertEqual(response.json(), [article_dict])
        
        date = timezone.now().date()
        article_text = "Lorem ipsum dolor sitdunt nsetetur sadiodio dignissim qui blandit praesent luptatum zzril delenit augue duis dolore te feugait nulla facilisi. Lorem ipsum dolor sit amet."
        article_title = "Lorit amet, co"
        
        category = Category.objects.create(title="Test8")
        article = NewsArticle.objects.create(article_text=article_text, category=category, pub_date=date, article_title=article_title)
        
        response = self.client.get(reverse('news_service_app:news-articles'))
        self.assertEqual(len(response.json()), 2)