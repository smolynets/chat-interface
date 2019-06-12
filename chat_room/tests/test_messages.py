"""
Tests for messages.
"""

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ..models import Message, Room, User


class RegistrationTest(APITestCase):
    """
    This test checks messages.

    This test checks next scenarios:
        1. Successful create message.
    """

    def test_create_message(self):
        """
        Check create.

        Successful created message.
        """

        room = Room.objects.create(name="test_room")
        user = User.objects.create_user(
            username="test2_user",
            email="test@emil.com",
            password="password"
        )

        post_data = {
            "text": "test_text",
            "room": room.id,
            "author": user.id
        }
        Messages_count_before = Message.objects.count()
        response = self.client.post(reverse("message-list"), post_data,
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["text"], "test_text")
        self.assertEqual(response.data["room"], room.id)
        self.assertEqual(response.data["author"], user.id)
        self.assertEqual(Message.objects.count(), Messages_count_before + 1)

    def test_create_message_without_data(self):
        """
        Check create.

        Successful created message.
        """

        post_data = {
            "text": "",
            "room": None,
            "author": None
        }
        Messages_count_before = Message.objects.count()
        response = self.client.post(reverse("message-list"), post_data,
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Message.objects.count(), Messages_count_before)
