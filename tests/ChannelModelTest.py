import unittest
from uuid import uuid4
from flaskr.domain.models.channel import Channel

class TestChannel(unittest.TestCase):
    def setUp(self):
        self.sample_id = uuid4()
        self.sample_name = "Sample Channel"
        self.channel = Channel(id=self.sample_id, name=self.sample_name)

    def test_init(self):
        self.assertEqual(self.channel.id, self.sample_id)
        self.assertEqual(self.channel.name, self.sample_name)

    def test_to_dict(self):
        expected_dict = {
            'id': str(self.sample_id),
            'name': self.sample_name
        }
        self.assertEqual(self.channel.to_dict(), expected_dict)

    def test_to_dict_contains_correct_types(self):
        result = self.channel.to_dict()
        self.assertIsInstance(result['id'], str)
        self.assertIsInstance(result['name'], str)

