import unittest
from unittest.mock import MagicMock
from uuid import uuid4


from flaskr.domain.interfaces.plan_repository import PlanRepository
from flaskr.domain.models.plan import Plan

class TestPlanRepository(unittest.TestCase):
    def setUp(self):
        self.plan_repository = PlanRepository()
        self.plan_repository.list = MagicMock()
        self.plan_repository.get_plan_by_id = MagicMock()

    def test_list(self):
        expected_plans = [
            Plan(id=uuid4(), name="Plan A", basic_monthly_rate=100.0, issue_fee=10.0),
            Plan(id=uuid4(), name="Plan B", basic_monthly_rate=200.0, issue_fee=20.0)
        ]
        self.plan_repository.list.return_value = expected_plans

        result = self.plan_repository.list()

        self.assertEqual(result, expected_plans)
        self.plan_repository.list.assert_called_once()

    def test_get_plan_by_id(self):
        plan_id = uuid4()
        expected_plan = Plan(id=plan_id, name="Plan A", basic_monthly_rate=100.0, issue_fee=10.0)
        self.plan_repository.get_plan_by_id.return_value = expected_plan

        result = self.plan_repository.get_plan_by_id(plan_id)

        self.assertEqual(result, expected_plan)
        self.plan_repository.get_plan_by_id.assert_called_once_with(plan_id)

