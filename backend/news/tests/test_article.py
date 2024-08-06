from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.utils.http import urlencode
from django.forms.models import model_to_dict
from datetime import timedelta
import os

from news.models import Category, NewsArticle 

def create_category_and_article(article_title, article_text, category_title, pub_date):
    category = Category.objects.create(title=category_title)
    return NewsArticle.objects.create(text=article_text, category=category, pub_date=pub_date, title=article_title)

def serialize_article_to_dict(article: NewsArticle):
    article_dict = model_to_dict(article, fields=[field.name for field in article._meta.fields])
    article_dict = {"category_id" if k == 'category' else k: f'{v.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]}Z' if k == 'pub_date' else v for k,v in article_dict.items()}
    return article_dict

def get_news_articles_relative_url():
    app_url = os.environ.get('APP_URL', None)
    if app_url is not None:
        return reverse('news:news-articles').replace(os.environ.get('APP_URL', None), "/")
    else:
        return reverse('news:news-articles')

def get_news_category_relative_url(category_id):
    app_url = os.environ.get('APP_URL', None)
    if app_url is not None:
        return reverse('news:category', args=[category_id]).replace(os.environ.get('APP_URL', None), "/")
    else:
        return reverse('news:category', args=[category_id])

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
        response = self.client.get(get_news_articles_relative_url())
        self.assertQuerysetEqual(response.json(), [])
        
        # Article 2
        pub_date = timezone.now() - timedelta(days=1)
        article = create_category_and_article(article_title=self.article_titles[1], article_text=self.article_texts[1], category_title=self.category_names[1], pub_date=pub_date)
        
        # Check that "Article 2" gets returned because its date is in the past
        response = self.client.get(get_news_articles_relative_url())
        article_dict = serialize_article_to_dict(article)
        self.assertEqual(response.json(), [article_dict])
        
        # Article 3
        pub_date = timezone.now()
        article = create_category_and_article(article_title=self.article_titles[2], article_text=self.article_texts[2], category_title=self.category_names[2], pub_date=pub_date)
        
        # Check that both "Article 2" and "Article 3" get returned 
        response = self.client.get(get_news_articles_relative_url())
        self.assertEqual(len(response.json()), 2)
        
    def test_sql_injection_attack(self):
        """ Test whether sql injections don't have any impact. """
        days_in_past = [1,3,4,5]
        
        for i in range(4):
            pub_date = timezone.now() - timedelta(days=days_in_past[i])
            create_category_and_article(article_title=self.article_titles[i], article_text=self.article_texts[i], category_title=self.category_names[i], pub_date=pub_date)
        
        # Check that four articles get returned
        response = self.client.get(get_news_articles_relative_url())
        self.assertEqual(len(response.json()), 4)
        
        # Try injection and check status code
        test_category_id = "DELETE * FROM NewsArticle; "
        base_url = get_news_category_relative_url(test_category_id)
        response = self.client.get('{base_url}'.format(base_url=base_url))
        self.assertEqual(response.status_code, 400)
        
        # Check that four articles get returned
        response = self.client.get(get_news_articles_relative_url())
        self.assertEqual(len(response.json()), 4)
