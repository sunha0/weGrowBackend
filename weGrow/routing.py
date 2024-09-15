from django.urls import re_path,include

from websocket import views
websocket_urlpatterns = [
    re_path(r"^ws/(?P<group>\w+)/", views.ChatConsumer)
]

