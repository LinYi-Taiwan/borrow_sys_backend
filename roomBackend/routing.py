from channels.routing import ProtocolTypeRouter, URLRouter
from roomBackend.urls import websocket_url

application = ProtocolTypeRouter({
    "websocket": URLRouter(
        websocket_url
    )
})
