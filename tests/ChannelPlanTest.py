import unittest
from uuid import uuid4

from flaskr.domain.models.channel_plan import ChannelPlan

class TestChannelPlan(unittest.TestCase):
    def setUp(self):
        self.sample_id = uuid4()
        self.sample_channel_id = uuid4()
        self.sample_plan_id = uuid4()
        
        self.channel_plan = ChannelPlan(
            id=self.sample_id,
            channel_id=self.sample_channel_id,
            plan_id=self.sample_plan_id
        )

    def test_init(self):
        self.assertEqual(self.channel_plan.id, self.sample_id)
        self.assertEqual(self.channel_plan.channel_id, self.sample_channel_id)
        self.assertEqual(self.channel_plan.plan_id, self.sample_plan_id)

    def test_attributes_are_correct_types(self):
        self.assertIsInstance(self.channel_plan.id, uuid4().__class__)
        self.assertIsInstance(self.channel_plan.channel_id, uuid4().__class__)
        self.assertIsInstance(self.channel_plan.plan_id, uuid4().__class__)

