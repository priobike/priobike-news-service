from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.utils.http import urlencode
import hashlib
from datetime import timedelta
import json

from news_service_app.utils.serializer import serialize_article_to_dict
from news_service_app.models import Category, NewsArticle 

class ArticleTests(TestCase):
    def test_only_return_news_articles_that_are_not_in_future(self):
        # Article 1
        date = timezone.now().date() + timedelta(days=1)
        article_text = "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis at vero eros et accumsan et iusto odio dignissim qui blandit praesent luptatum zzril delenit augue duis dolore te feugait nulla facilisi. Lorem ipsum dolor sit amet."
        article_title = "Lorem ipsum dolor sit amet, co"
        category = Category.objects.create(title="Test")
        NewsArticle.objects.create(article_text=article_text, category=category, pub_date=date, article_title=article_title)
        
        # Check that "Article 1" doesn't get returned because its date is in the future
        response = self.client.get(reverse('news_service_app:news-articles'))
        self.assertQuerysetEqual(response.json(), [])
        
        # Article 2
        date = timezone.now().date() - timedelta(days=1)
        article_text = "Lorem ipsum dolor sitdunt nsetetur sadiodio dignissim qui blandit praesent luptatum zzril delenit augue duis dolore te feugait nulla facilisi. Lorem ipsum dolor sit amet."
        article_title = "Lorit amet, co"
        category = Category.objects.create(title="Test5")
        article = NewsArticle.objects.create(article_text=article_text, category=category, pub_date=date, article_title=article_title)
        
        # Check that "Article 2" gets returned because its date is in the past
        response = self.client.get(reverse('news_service_app:news-articles'))
        article_dict = serialize_article_to_dict(article)
        self.assertEqual(response.json(), [article_dict])
        
        # Article 3
        date = timezone.now().date()
        article_text = "Lorem ipsum dolor sitdunt nsetetur sadiodio dignissim qui blandit praesent luptatum zzril delenit augue duis dolore te feugait nulla facilisi. Lorem ipsum dolor sit amet."
        article_title = "Lorit amet, co"
        category = Category.objects.create(title="Test8")
        article = NewsArticle.objects.create(article_text=article_text, category=category, pub_date=date, article_title=article_title)
        
        # Check that both "Article 2" and "Article 3" get returned 
        response = self.client.get(reverse('news_service_app:news-articles'))
        self.assertEqual(len(response.json()), 2)
        
    def test_only_return_news_articles_up_to_specific_date(self):
        # Show articles with a release date newer or same like this date
        test_date = timezone.now().date() - timedelta(days=4)
        
        # Article 1:
        date = timezone.now().date() - timedelta(days=1)
        article_text = "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis at vero eros et accumsan et iusto odio dignissim qui blandit praesent luptatum zzril delenit augue duis dolore te feugait nulla facilisi. Lorem ipsum dolor sit amet."
        article_title = "Lorem ipsum dolor sit amet, co"
        category = Category.objects.create(title="Test")
        NewsArticle.objects.create(article_text=article_text, category=category, pub_date=date, article_title=article_title)
        
        # Article 2:
        date = timezone.now().date() - timedelta(days=3)
        article_text = "Lorem ipsum dolor sit amet accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis at vero eros et accumsan et iusto odio dignissim qui blandit praesent luptatum zzril delenit augue duis dolore te feugait nulla facilisi. Lorem ipsum dolor sit amet."
        article_title = "Lorem t amet, co"
        category = Category.objects.create(title="Test245")
        NewsArticle.objects.create(article_text=article_text, category=category, pub_date=date, article_title=article_title)
        
        # Article 3:
        date = timezone.now().date() - timedelta(days=4)
        article_text = "Lorem ipsum dolor sit amet accurem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis at vero eros et accumsan et iusto odio dignissim qui blandit praesent luptatum zzril delenit augue duis dolore te feugait nulla facilisi. Lorem ipsum dolor sit amet."
        article_title = "Lorem t amet, cofa wefa wefa wef awef "
        category = Category.objects.create(title="Test 346")
        article1 = NewsArticle.objects.create(article_text=article_text, category=category, pub_date=date, article_title=article_title)
        
        # Article 4:
        date = timezone.now().date() - timedelta(days=5)
        article_text = "Lorem  ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis at vero eros et accumsan et iusto odio dignissim qui blandit praesent luptatum zzril delenit augue duis dolore te feugait nulla facilisi. Lorem ipsum dolor sit amet."
        article_title = " wef awef "
        category = Category.objects.create(title="Test swergser")
        article2 = NewsArticle.objects.create(article_text=article_text, category=category, pub_date=date, article_title=article_title)
        
        # Create hash for the articles that got released before or on the test_date
        articles = [article1, article2]
        articles_serialized = [serialize_article_to_dict(article) for article in articles]
        articles_json = json.dumps(articles_serialized)
        hash = hashlib.md5(articles_json.encode('utf-8')).hexdigest()
        
        # Get articles:
        base_url = reverse('news_service_app:news-articles')
        response = self.client.get('{base_url}?{querystring}'.format(base_url=base_url, querystring=urlencode({'last_sync_date': test_date.strftime("%Y-%m-%d"), 'hash': hash})))
        self.assertEqual(len(response.json()), 2)
        
    def test_return_all_articles_after_sending_wrong_hash(self):
        # Theoretically show articles with a release date newer or same like this date
        test_date = timezone.now().date() - timedelta(days=4)
        
        # Article 1:
        date = timezone.now().date() - timedelta(days=1)
        article_text = "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis at vero eros et accumsan et iusto odio dignissim qui blandit praesent luptatum zzril delenit augue duis dolore te feugait nulla facilisi. Lorem ipsum dolor sit amet."
        article_title = "Lorem ipsum dolor sit amet, co"
        category = Category.objects.create(title="Test")
        NewsArticle.objects.create(article_text=article_text, category=category, pub_date=date, article_title=article_title)
        
        # Article 2:
        date = timezone.now().date() - timedelta(days=3)
        article_text = "Lorem ipsum dolor sit amet accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis at vero eros et accumsan et iusto odio dignissim qui blandit praesent luptatum zzril delenit augue duis dolore te feugait nulla facilisi. Lorem ipsum dolor sit amet."
        article_title = "Lorem t amet, co"
        category = Category.objects.create(title="Test245")
        NewsArticle.objects.create(article_text=article_text, category=category, pub_date=date, article_title=article_title)
        
        # Article 3:
        date = timezone.now().date() - timedelta(days=4)
        article_text = "Lorem ipsum dolor sit amet accurem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis at vero eros et accumsan et iusto odio dignissim qui blandit praesent luptatum zzril delenit augue duis dolore te feugait nulla facilisi. Lorem ipsum dolor sit amet."
        article_title = "Lorem t amet, cofa wefa wefa wef awef "
        category = Category.objects.create(title="Test 346")
        article1 = NewsArticle.objects.create(article_text=article_text, category=category, pub_date=date, article_title=article_title)
        
        # Article 4:
        date = timezone.now().date() - timedelta(days=5)
        article_text = "Lorem  ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis at vero eros et accumsan et iusto odio dignissim qui blandit praesent luptatum zzril delenit augue duis dolore te feugait nulla facilisi. Lorem ipsum dolor sit amet."
        article_title = " wef awef "
        category = Category.objects.create(title="Test swergser")
        article2 = NewsArticle.objects.create(article_text=article_text, category=category, pub_date=date, article_title=article_title)
        
        # Create wrong hash
        hash = "bc3afe19e2b0c792554c86f55c3e4d99"
        
        # Get all articles because of wrong hash:
        base_url = reverse('news_service_app:news-articles')
        response = self.client.get('{base_url}?{querystring}'.format(base_url=base_url, querystring=urlencode({'last_sync_date': test_date.strftime("%Y-%m-%d"), 'hash': hash})))
        self.assertEqual(len(response.json()), 4)
        
