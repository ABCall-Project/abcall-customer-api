import unittest
from unittest.mock import patch, MagicMock
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from uuid import uuid4
from unittest.mock import ANY
from flaskr.infrastructure.databases.customer_postgresql_repository import CustomerPostgresqlRepository
from flaskr.domain.models.customer import Customer
from flaskr.infrastructure.databases.model_sqlalchemy import CustomerModelSqlAlchemy, PlanModelSqlAlchemy

class TestCustomerPostgresqlRepository(unittest.TestCase):

    @patch('flaskr.infrastructure.databases.customer_postgresql_repository.create_engine')
    @patch('flaskr.infrastructure.databases.customer_postgresql_repository.sessionmaker')
    def setUp(self, mock_sessionmaker, mock_create_engine):
        self.mock_engine = MagicMock()
        mock_create_engine.return_value = self.mock_engine

        self.mock_session = MagicMock()
        self.mock_session_instance = MagicMock()
        self.mock_session.return_value = self.mock_session_instance
        mock_sessionmaker.return_value = self.mock_session

        self.repo = CustomerPostgresqlRepository('mock_connection_string')
        self.repo.Session = self.mock_session

    def test_get_customer_plan(self):
        customer_id = uuid4()
        expected_rate = 99.99
        mock_plan = (expected_rate,)
        self.mock_session_instance.query.return_value.join.return_value.filter.return_value.first.return_value = mock_plan

        result = self.repo.get_customer_plan(customer_id)

        self.assertEqual(result, expected_rate)
        self.mock_session_instance.query.assert_called_once_with(PlanModelSqlAlchemy.basic_monthly_rate)
        self.mock_session_instance.query().join.assert_called_once_with(CustomerModelSqlAlchemy, ANY)
     

    def test_get_customer_issue_fee(self):
        customer_id = uuid4()
        expected_fee = 50.0
        mock_fee = (expected_fee,)
        self.mock_session_instance.query.return_value.join.return_value.filter.return_value.first.return_value = mock_fee

        result = self.repo.get_customer_issue_fee(customer_id)

        self.assertEqual(result, expected_fee)
        self.mock_session_instance.query.assert_called_once_with(PlanModelSqlAlchemy.issue_fee)
        self.mock_session_instance.query().join.assert_called_once_with(CustomerModelSqlAlchemy, ANY)
    

    def test_list(self):
        mock_customer = CustomerModelSqlAlchemy(
            id=uuid4(),
            name="Customer A",
            plan_id=uuid4(),
            date_suscription="2023-01-01"
        )
        self.mock_session_instance.query.return_value.all.return_value = [mock_customer]

        result = self.repo.list()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, "Customer A")
        self.mock_session_instance.query.assert_called_once_with(CustomerModelSqlAlchemy)

    def test_get_customer_by_id_found(self):
        customer_id = uuid4()
        mock_customer = CustomerModelSqlAlchemy(
            id=customer_id,
            name="Customer B",
            plan_id=uuid4(),
            date_suscription="2023-02-01"
        )
        self.mock_session_instance.query.return_value.filter_by.return_value.first.return_value = mock_customer

        result = self.repo.get_customer_by_id(customer_id)

        self.assertIsNotNone(result)
        self.assertEqual(result.id, customer_id)
        self.mock_session_instance.query.assert_called_once_with(CustomerModelSqlAlchemy)
        self.mock_session_instance.query().filter_by.assert_called_once_with(id=customer_id)

    def test_get_customer_by_id_not_found(self):
        customer_id = uuid4()
        self.mock_session_instance.query.return_value.filter_by.return_value.first.return_value = None

        result = self.repo.get_customer_by_id(customer_id)

        self.assertIsNone(result)
        self.mock_session_instance.query.assert_called_once_with(CustomerModelSqlAlchemy)
        self.mock_session_instance.query().filter_by.assert_called_once_with(id=customer_id)
