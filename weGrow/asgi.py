"""
ASGI configure for weGrow project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from channels import routing
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from . import routing
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'weGrow.settings')

# application = get_asgi_application()
print(111111111111111111111111)
application = ProtocolTypeRouter({
        "http": get_asgi_application(),
        "websocket": URLRouter(routing.websocket_urlpatterns)
})