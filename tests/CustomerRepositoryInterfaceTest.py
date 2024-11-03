import unittest
from unittest.mock import MagicMock
from uuid import uuid4
from flaskr.domain.interfaces.customer_repository import CustomerRepository
from flaskr.domain.models.customer import Customer

class TestCustomerRepository(unittest.TestCase):
    def setUp(self):
        self.customer_repository = CustomerRepository()
        self.customer_repository.list = MagicMock()
        self.customer_repository.get_customer_by_id = MagicMock()
        self.customer_repository.get_customer_plan = MagicMock()
        self.customer_repository.get_customer_issue_fee = MagicMock()

    def test_list(self):
        expected_customers = [
            Customer(id=uuid4(), name="Customer1", plan_id=uuid4(), date_suscription="2023-01-01"),
            Customer(id=uuid4(), name="Customer2", plan_id=uuid4(), date_suscription="2023-02-01")
        ]
        self.customer_repository.list.return_value = expected_customers

        result = self.customer_repository.list()

        self.assertEqual(result, expected_customers)
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
        for customer in result:
            self.assertIsInstance(customer, Customer)
        self.customer_repository.list.assert_called_once()

    def test_get_customer_by_id_found(self):
        customer_id = uuid4()
        expected_customer = Customer(id=customer_id, name="Customer1", plan_id=uuid4(), date_suscription="2023-01-01")
        self.customer_repository.get_customer_by_id.return_value = expected_customer

        result = self.customer_repository.get_customer_by_id(customer_id)

        self.assertEqual(result, expected_customer)
        self.assertIsInstance(result, Customer)
        self.assertEqual(result.id, customer_id)
        self.customer_repository.get_customer_by_id.assert_called_once_with(customer_id)

    def test_get_customer_by_id_not_found(self):
        customer_id = uuid4()
        self.customer_repository.get_customer_by_id.return_value = None

        result = self.customer_repository.get_customer_by_id(customer_id)

        self.assertIsNone(result)
        self.customer_repository.get_customer_by_id.assert_called_once_with(customer_id)

    def test_get_customer_plan(self):
        customer_id = uuid4()
        expected_plan = 99.99
        self.customer_repository.get_customer_plan.return_value = expected_plan

        result = self.customer_repository.get_customer_plan(customer_id)

        self.assertEqual(result, expected_plan)
        self.assertIsInstance(result, float)
        self.customer_repository.get_customer_plan.assert_called_once_with(customer_id)

    def test_get_customer_issue_fee(self):
        customer_id = uuid4()
        expected_issue_fee = 50.0
        self.customer_repository.get_customer_issue_fee.return_value = expected_issue_fee

        result = self.customer_repository.get_customer_issue_fee(customer_id)

        self.assertEqual(result, expected_issue_fee)
        self.assertIsInstance(result, float)
        self.customer_repository.get_customer_issue_fee.assert_called_once_with(customer_id)

    def test_list_empty(self):
        self.customer_repository.list.return_value = []

        result = self.customer_repository.list()

        self.assertEqual(result, [])
        self.assertIsInstance(result, list)
        self.customer_repository.list.assert_called_once()
