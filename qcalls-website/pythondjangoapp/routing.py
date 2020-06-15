from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from app.consumers import TickTockConsumer

application = ProtocolTypeRouter({
    "websocket": URLRouter([
        path("ws/", TickTockConsumer),
    ])
})
