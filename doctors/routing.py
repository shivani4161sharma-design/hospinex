from django.urls import path
from .consumer import DoctorNotificationConsumer

websocket_urlpatterns = [
    path("ws/doctor/", DoctorNotificationConsumer.as_asgi()),
]

