from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from news.models import NewsArticle
import firebase_admin
from firebase_admin import credentials
from firebase_admin import messaging
import os

@receiver(post_save, sender=NewsArticle)
def send_notification_for_news_article(sender, instance, created, **kwargs):
    """ Send notification when new news article got created.
    Mobile clients can visualize it as push notifications.
    """
    
    # Don't send message on updates, only when new articles are created.
    if created and not settings.TESTING:
        # Authenticate with firebase admin serice key.
        cred = credentials.Certificate(os.path.join(settings.BASE_DIR, "../backend/news/config/priobikefcm-firebase-adminsdk-evhd7-813bd37626.json"))
        app = firebase_admin.initialize_app(cred)
        
        # Truncate if the text is to long.
        body = (instance.text[:100] + '...') if len(instance.text) > 100 else instance.text
        
        # One of the following: 'dev' / 'staging' / 'production'
        environment = os.environ.get('PUSH_NOTIFICATION_ENVIRONMENT', 'dev')

        # Defining the messsage payload.
        message = messaging.Message(
            data={
                'environment': environment,
            },
            notification=messaging.Notification(
                title = instance.title,
                body = body
            ),
            topic='/topics/Neuigkeiten',
        )

        # Send a message to the devices subscribed to the provided topic.
        response = messaging.send(message)
        # Response is a message ID string.
        print('Successfully sent message:', response)
        
        firebase_admin.delete_app(app)