import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import recipes.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'recipe_backend.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            recipes.routing.websocket_urlpatterns
        )
    ),
})
