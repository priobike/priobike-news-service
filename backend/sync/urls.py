from django.urls import path

from . import views

app_name = 'sync'

urlpatterns = [
    path("sync", views.SyncResource.as_view(), name="sync"),
]
