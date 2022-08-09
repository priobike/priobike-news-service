from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.utils.http import urlencode
from django.forms.models import model_to_dict
from datetime import timedelta
import json

from news.models import Category, NewsArticle 

def create_category_and_article(article_title, article_text, category_title, pub_date):
    category = Category.objects.create(title=category_title)
    return NewsArticle.objects.create(text=article_text, category=category, pub_date=pub_date, title=article_title)

def serialize_article_to_dict(article: NewsArticle):
    article_dict = model_to_dict(article, fields=[field.name for field in article._meta.fields])
    article_dict = {"category_id" if k == 'category' else k: f'{v.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]}Z' if k == 'pub_date' else v for k,v in article_dict.items()}
    return article_dict

class ArticleTests(TestCase):
    article_texts = [
        "Lorem  ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis at vero eros et accumsan et iusto odio dignissim qui blandit praesent luptatum zzril delenit augue duis dolore te feugait nulla facilisi. Lorem ipsum dolor sit amet.",
        "Lorecvbnmbvbnvbnvbnnvbnvm ipsum dolor sit amet accurem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis at vero eros et accumsan et iusto odio dignissim qui blandit praesent luptatum zzril delenit augue duis dolore te feugait nulla facilisi. Lorem ipsum dolor sit amet.",
        "Loreawesf awem ipsum dolor sit amet accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis at vero eros et accumsan et iusto odio dignissim qui blandit praesent luptatum zzril delenit augue duis dolore te feugait nulla facilisi. Lorem ipsum dolor sit amet.",
        "Loretzluzuiölzuim ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis at vero eros et accumsan et iusto odio dignissim qui blandit praesent luptatum zzril delenit augue duis dolore te feugait nulla facilisi. Lorem ipsum dolor sit amet."
    ]
    
    article_titles = [
        " wef awef ",
        "Lorem t amet, cofa wefa wefa wef awef ",
        "Lorem t amet, co",
        "Lorem ipsum dolor sit amet, co"
    ]
    
    category_names = [
        "Test swergser",
        "Test 346",
        "Test245",
        "Test"
    ]
    
    def test_only_return_news_articles_that_are_not_in_future(self):
        """ Test whether no articles that are scheduled for future dates get returned. """
        
        # Article 1
        pub_date = timezone.now() + timedelta(days=1)
        create_category_and_article(article_title=self.article_titles[0], article_text=self.article_texts[0], category_title=self.category_names[0], pub_date=pub_date)
        
        # Check that "Article 1" doesn't get returned because its date is in the future
        response = self.client.get(reverse('news:news-articles'))
        self.assertQuerysetEqual(response.json(), [])
        
        # Article 2
        pub_date = timezone.now() - timedelta(days=1)
        article = create_category_and_article(article_title=self.article_titles[1], article_text=self.article_texts[1], category_title=self.category_names[1], pub_date=pub_date)
        
        # Check that "Article 2" gets returned because its date is in the past
        response = self.client.get(reverse('news:news-articles'))
        article_dict = serialize_article_to_dict(article)
        self.assertEqual(response.json(), [article_dict])
        
        # Article 3
        pub_date = timezone.now()
        article = create_category_and_article(article_title=self.article_titles[2], article_text=self.article_texts[2], category_title=self.category_names[2], pub_date=pub_date)
        
        # Check that both "Article 2" and "Article 3" get returned 
        response = self.client.get(reverse('news:news-articles'))
        self.assertEqual(len(response.json()), 2)
        
    def test_only_return_news_articles_up_to_specific_date(self):
        """ Test whether only articles with a release date newer like given date get returned. """
        
        # Article 1:
        pub_date = timezone.now()- timedelta(days=1)
        article1 = create_category_and_article(article_title=self.article_titles[0], article_text=self.article_texts[0], category_title=self.category_names[0], pub_date=pub_date)
        
        # Article 2:
        pub_date = timezone.now() - timedelta(days=3)
        article2 = create_category_and_article(article_title=self.article_titles[1], article_text=self.article_texts[1], category_title=self.category_names[1], pub_date=pub_date)
        
        # Article 3:
        pub_date = timezone.now() - timedelta(days=4)
        create_category_and_article(article_title=self.article_titles[2], article_text=self.article_texts[2], category_title=self.category_names[2], pub_date=pub_date)
        test_date = pub_date
        # Article 4:
        pub_date = timezone.now() - timedelta(days=5)
        create_category_and_article(article_title=self.article_titles[3], article_text=self.article_texts[3], category_title=self.category_names[3], pub_date=pub_date)
        
        # Create hash for the articles that got released before or on the test_date
        articles = [article1, article2]
        articles_serialized = [serialize_article_to_dict(article) for article in articles]
        articles_json = json.dumps(articles_serialized)
        
        # Get articles:
        base_url = reverse('news:news-articles')
        response = self.client.get('{base_url}?{querystring}'.format(base_url=base_url, querystring=urlencode({'from': f'{test_date.strftime("%Y-%m-%dT%H:%M:%S.%f")}Z'})))
        
        self.assertEqual(response.json(), articles_serialized)
        
        # Get articles:
        test_date = timezone.now() - timedelta(days=4)
        base_url = reverse('news:news-articles')
        response = self.client.get('{base_url}?{querystring}'.format(base_url=base_url, querystring=urlencode({'from': f'{test_date.strftime("%Y-%m-%dT%H:%M:%S.%f")}Z'})))
        
        self.assertEqual(response.json(), articles_serialized)
        
    def test_sql_injection_attack(self):
        """ Test whether sql injections don't have any impact. """
        days_in_past = [1,3,4,5]
        
        for i in range(4):
            pub_date = timezone.now() - timedelta(days=days_in_past[i])
            create_category_and_article(article_title=self.article_titles[i], article_text=self.article_texts[i], category_title=self.category_names[i], pub_date=pub_date)
        
        # Check that four articles get returned
        response = self.client.get(reverse('news:news-articles'))
        self.assertEqual(len(response.json()), 4)
        
        # Try injection and check status code
        test_date = "DELETE * FROM NewsArticle; "
        base_url = reverse('news:news-articles')
        response = self.client.get('{base_url}?{querystring}'.format(base_url=base_url, querystring=urlencode({'from': test_date})))
        self.assertEqual(response.status_code, 400)
        
        # Check that four articles get returned
        response = self.client.get(reverse('news:news-articles'))
        self.assertEqual(len(response.json()), 4)