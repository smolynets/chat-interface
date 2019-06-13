"""
Tests for messages.
"""

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ..models import Message, Room, User
from .factories import MessageFactory, RoomFactory, UserFactory


class MessageTest(APITestCase):
    """
    This test checks messages.

    This test checks next scenarios:
        1. Successful create message.
    """

    def test_post_message(self):
        """
        Check create.

        Successful created message.
        """

        user = User.objects.create_user(
            username="test2_user",
            email="test@emil.com",
            password="password"
        )
        post_data = {"username": "test2_user", "password": "password"}
        response = self.client.post(reverse("login"), post_data,
                                    format="json")

        room = Room.objects.create(name="test_room")

        post_data = {
            "text": "test_text",
            "room": room.id
        }
        Messages_count_before = Message.objects.count()
        response = self.client.post(reverse("message-list"), post_data,
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["text"], "test_text")
        self.assertEqual(response.data["room"], room.id)
        # self.assertEqual(response.data["author"], user.id)
        self.assertEqual(Message.objects.count(), Messages_count_before + 1)

    def test_post_message_without_data(self):
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

    def test_get_message(self):
        """
        Check create.

        Successful created message.
        """

        user = UserFactory()
        post_data = {"username": user.username, "password": user.password}
        response = self.client.post(reverse("login"), post_data,
                                    format="json")

        room = RoomFactory()
        MessageFactory.create_batch(12)

        post_data = {
            "text": "test_text",
            "room": room.id
        }
        response = self.client.get(reverse("message-list"), post_data,
                                   format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 12)
        self.assertEqual(len(response.data["results"]), 10)
        saved_messages = [message.id for message in Message.objects.all()[:10]]
        for message in response.data["results"]:
            self.assertIn(message["id"], saved_messages)