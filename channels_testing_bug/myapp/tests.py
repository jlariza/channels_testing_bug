import pytest
from django.test import TestCase
from channels.testing import WebsocketCommunicator
from django.urls import path
from channels.routing import URLRouter
from .consumers import MyModelConsumer
from .models import MyModel
from channels.db import database_sync_to_async


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
class TestMyModelConsumer(TestCase):
    """
    Test class that holds the test cases for the MyModelConsumer class
    """

    @database_sync_to_async
    def create_instance(self):
        return MyModel.objects.create()

    # based on https://channels.readthedocs.io/en/latest/topics/testing.html#websocketcommunicator
    async def test_my_consumer(self):
        instance = await self.create_instance()
        application = URLRouter(
            [
                path("test/<object_id>/", MyModelConsumer.as_asgi()),
            ]
        )
        communicator = WebsocketCommunicator(application, f"test/{instance.id}/")
        connected, subprotocol = await communicator.connect()
        self.assertTrue(connected)
