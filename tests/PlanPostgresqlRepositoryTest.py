import unittest
from unittest.mock import patch, MagicMock
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from uuid import uuid4
from unittest.mock import ANY
from flaskr.infrastructure.databases.plan_postgresql_repository import PlanPostgresqlRepository
from flaskr.domain.models.plan import Plan
from flaskr.infrastructure.databases.model_sqlalchemy import PlanModelSqlAlchemy

class TestPlanPostgresqlRepository(unittest.TestCase):

    @patch('flaskr.infrastructure.databases.plan_postgresql_repository.create_engine')
    @patch('flaskr.infrastructure.databases.plan_postgresql_repository.sessionmaker')
    def setUp(self, mock_sessionmaker, mock_create_engine):
        self.mock_engine = MagicMock()
        mock_create_engine.return_value = self.mock_engine

        self.mock_session = MagicMock()
        self.mock_session_instance = MagicMock()
        self.mock_session.return_value = self.mock_session_instance
        mock_sessionmaker.return_value = self.mock_session

        self.repo = PlanPostgresqlRepository('mock_connection_string')
        self.repo.Session = self.mock_session

    def test_get_rate_plan(self):
        plan_id = uuid4()
        expected_rate = 150.0
        mock_rate = (expected_rate,)
        self.mock_session_instance.query.return_value.filter.return_value.first.return_value = mock_rate

        result = self.repo.get_rate_plan(plan_id)

        self.assertEqual(result[0], expected_rate)
        self.mock_session_instance.query.assert_called_once_with(PlanModelSqlAlchemy.basic_monthly_rate)
        self.mock_session_instance.query().filter.assert_called_once_with(ANY)

    def test_get_plan_by_id_found(self):
        plan_id = uuid4()
        mock_plan = PlanModelSqlAlchemy(
            id=plan_id,
            name="Plan C",
            basic_monthly_rate=120.0,
            issue_fee=15.0
        )
        self.mock_session_instance.query.return_value.filter_by.return_value.first.return_value = mock_plan

        result = self.repo.get_plan_by_id(plan_id)

        self.assertIsNotNone(result)
        self.assertEqual(result.id, plan_id)
        self.assertEqual(result.name, "Plan C")
        self.assertEqual(result.basic_monthly_rate, 120.0)
        self.assertEqual(result.issue_fee, 15.0)
        self.mock_session_instance.query.assert_called_once_with(PlanModelSqlAlchemy)
        self.mock_session_instance.query().filter_by.assert_called_once_with(id=plan_id)

    def test_get_plan_by_id_not_found(self):
        plan_id = uuid4()
        self.mock_session_instance.query.return_value.filter_by.return_value.first.return_value = None

        result = self.repo.get_plan_by_id(plan_id)

        self.assertIsNone(result)
        self.mock_session_instance.query.assert_called_once_with(PlanModelSqlAlchemy)
        self.mock_session_instance.query().filter_by.assert_called_once_with(id=plan_id)
