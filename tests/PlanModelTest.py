import unittest
from uuid import uuid4
from datetime import datetime
from flaskr.domain.models.plan import Plan

class TestPlan(unittest.TestCase):
    def setUp(self):
        self.sample_id = uuid4()
        self.sample_name = "Sample Plan"
        self.sample_basic_monthly_rate = 100.0
        self.sample_issue_fee = 15.0
        self.plan = Plan(
            id=self.sample_id,
            name=self.sample_name,
            basic_monthly_rate=self.sample_basic_monthly_rate,
            issue_fee=self.sample_issue_fee
        )

    def test_init(self):
        self.assertEqual(self.plan.id, self.sample_id)
        self.assertEqual(self.plan.name, self.sample_name)
        self.assertEqual(self.plan.basic_monthly_rate, self.sample_basic_monthly_rate)
        self.assertEqual(self.plan.issue_fee, self.sample_issue_fee)

    def test_to_dict(self):
        expected_dict = {
            'id': str(self.sample_id),
            'name': self.sample_name,
            'basic_monthly_rate': str(self.sample_basic_monthly_rate),
            'issue_fee': str(self.sample_issue_fee)
        }
        self.assertEqual(self.plan.to_dict(), expected_dict)
