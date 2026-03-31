import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from asgiref.sync import sync_to_async
from .models import ChatMessage


# =====================================================
# 🔔 DOCTOR NOTIFICATION CONSUMER
# =====================================================
class DoctorNotificationConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        user = self.scope["user"]

        if user.is_anonymous or not user.is_staff:
            await self.close()
            return

        self.group_name = f"doctor_{user.id}"

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def send_notification(self, event):
        await self.send(text_data=json.dumps({
            "type": "notification",
            "message": event["message"],
        }))


# =====================================================
# 💬 DOCTOR ↔ PATIENT CHAT CONSUMER
# =====================================================
class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.user = self.scope["user"]

        if self.user.is_anonymous:
            await self.close()
            return

        self.doctor_id = self.scope["url_route"]["kwargs"]["doctor_id"]
        self.room_group_name = f"chat_doctor_{self.doctor_id}"

        # Optional safety: only doctor OR patient allowed
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)

        message = data.get("message", "").strip()
        patient_name = data.get("patient_name", "")

        if not message:
            return

        sender = "doctor" if self.user.is_staff else "patient"

        await self.save_message(
            sender=sender,
            patient_name=patient_name,
            message=message
        )

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "sender": sender,
                "patient_name": patient_name,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "sender": event["sender"],
            "patient_name": event["patient_name"],
        }))

    @sync_to_async
    def save_message(self, sender, patient_name, message):
        doctor = User.objects.get(id=self.doctor_id)

        ChatMessage.objects.create(
            doctor=doctor,
            patient_name=patient_name,
            message=message,
            sender=sender,
        )

