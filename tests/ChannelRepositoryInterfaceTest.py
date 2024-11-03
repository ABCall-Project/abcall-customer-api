import unittest
from unittest.mock import MagicMock
from uuid import uuid4
from flaskr.domain.interfaces.channel_repository import ChannelRepository
from flaskr.domain.models.channel import Channel


class TestChannelRepository(unittest.TestCase):
    def setUp(self):
        self.channel_repository = ChannelRepository()
        self.channel_repository.list = MagicMock()
        self.channel_repository.get_channel_by_plan = MagicMock()

    def test_list(self):
        expected_channels = [
            Channel(id=uuid4(), name="Channel1"),
            Channel(id=uuid4(), name="Channel2")
        ]
        self.channel_repository.list.return_value = expected_channels

        result = self.channel_repository.list()

        self.assertEqual(result, expected_channels)
        self.channel_repository.list.assert_called_once()

    def test_get_channel_by_plan(self):
        plan_id = uuid4()
        expected_channels = [
            Channel(id=uuid4(), name="Channel1"),
            Channel(id=uuid4(), name="Channel2")
        ]
        self.channel_repository.get_channel_by_plan.return_value = expected_channels

        result = self.channel_repository.get_channel_by_plan(plan_id)

        self.assertEqual(result, expected_channels)
        self.channel_repository.get_channel_by_plan.assert_called_once_with(plan_id)
