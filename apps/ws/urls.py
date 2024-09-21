from django.urls import re_path

from apps.ws import views

websocket_urlpatterns = [
    re_path(r'^room/', views.ChatConsumer.as_asgi())
]