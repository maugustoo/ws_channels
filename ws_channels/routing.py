""" Routing for alarm notification websocket"""
from django.conf.urls import url
from ws_channels.consumers import AlarmNotificationConsumer
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import OriginValidator
from ws_channels.token_auth import TokenAuthMiddleware

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    "websocket": OriginValidator(
        TokenAuthMiddleware(
            URLRouter(
                [
                url(r"^ws/alarm_notification/(?P<room_name>[^/]+)/$",
                    AlarmNotificationConsumer),
                ]
            )
        ),
        ["*"],
    ),
})
