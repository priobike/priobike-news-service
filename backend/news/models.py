import hashlib
import json

from django.db import models
from django.utils import timezone


class Category(models.Model):
    """ A category of news articles. """

    title = models.CharField(max_length=30)

    def __str__(self):
        return self.title

    def __repr__(self):
        """ Used for md5 hash generation. """
        return self.title

class NewsArticle(models.Model):
    """ A news article. """

    text = models.TextField()
    title = models.CharField(max_length=70)
    pub_date = models.DateTimeField(default=timezone.now)

    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL)

    md5 = models.CharField(max_length=32)

    def save(self, *args, **kwargs):
        if not self.md5:
            data = {
                "text": self.text, 
                "title": self.title,
                "pub_date": str(self.pub_date),
                "category": None if not self.category else repr(self.category),
            }
            data_json = json.dumps(data)
            self.md5 = hashlib.md5(data_json.encode('utf-8')).hexdigest()
        return super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.title}: {self.text}"

    class Meta:
        ordering = ['-pub_date']