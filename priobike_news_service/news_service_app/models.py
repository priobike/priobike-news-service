from django.db import models

class Category(models.Model):
    title = models.CharField(max_length=30)

    def __str__(self):
        return self.title

class NewsArticle(models.Model):
    article_text = models.TextField()
    article_title = models.CharField(max_length=70)
    pub_date = models.DateField()
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.article_title + ": " + self.article_text

    class Meta:
        ordering = ['-pub_date']