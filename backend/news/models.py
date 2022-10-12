import hashlib
import json
import os

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from firebase_admin import delete_app, initialize_app
from firebase_admin.credentials import Certificate
from firebase_admin.messaging import Message, Notification, send


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


@receiver(post_save, sender=NewsArticle)
def send_notification_for_news_article(sender, instance, created, **kwargs):
    """ 
    Send notification when new news article got created.
    
    Mobile clients can visualize it as push notifications.
    """

    # In debug mode, we don't want to send notifications.
    if settings.DEBUG:
        print('Debug mode is on, skipping notification sending.')
        return

    # Don't send message on updates, only when new articles are created.
    if not created:
        print('News article was updated, skipping notification sending.')
        return
        
    # Authenticate with firebase admin serice key.
    cred = Certificate(os.path.join(settings.BASE_DIR, "config/fcm-key.json"))
    app = initialize_app(cred)
    
    # Truncate if the text is to long.
    body = (instance.text[:100] + '...') if len(instance.text) > 100 else instance.text

    # Create the FCM message.
    payload = { 'environment': settings.FCM_PUSH_NOTIFICATION_ENVIRONMENT }
    notification = Notification(title = instance.title, body = body)
    topic = settings.FCM_PUSH_NOTIFICATION_TOPIC
    message = Message(data=payload, notification=notification, topic=topic)

    # Send a message to the devices subscribed to the provided topic.
    response = send(message)
    # Response is a message ID string.
    print('Successfully sent FCM message:', response)
    
    delete_app(app)
