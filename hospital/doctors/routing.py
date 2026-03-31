from django.urls import path
from .consumers import DoctorNotificationConsumer

websocket_urlpatterns = [
    path("ws/doctor/", DoctorNotificationConsumer.as_asgi()),
]
