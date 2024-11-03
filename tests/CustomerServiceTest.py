import unittest
from unittest.mock import MagicMock
from uuid import uuid4
from flaskr.domain.models.customer import Customer
from flaskr.application.customer_service import CustomerService
from flaskr.domain.interfaces.customer_repository import CustomerRepository
from flaskr.domain.interfaces.plan_repository import PlanRepository
from flaskr.domain.interfaces.channel_repository import ChannelRepository

class TestCustomerService(unittest.TestCase):
    def setUp(self):
        self.mock_customer_repository = MagicMock(spec=CustomerRepository)
        self.mock_plan_repository = MagicMock(spec=PlanRepository)
        self.mock_channel_repository = MagicMock(spec=ChannelRepository)
        
        self.service = CustomerService(
            customer_repository=self.mock_customer_repository,
            plan_repository=self.mock_plan_repository,
            channel_repository=self.mock_channel_repository
        )

    def test_get_base_plan_suscription_rate(self):
        customer_id = uuid4()
        expected_rate = 99.99
        self.mock_customer_repository.get_customer_plan.return_value = expected_rate
        
        result = self.service.get_base_plan_suscription_rate(customer_id)
        
        self.assertEqual(result, expected_rate)
        self.mock_customer_repository.get_customer_plan.assert_called_once_with(customer_id)

    def test_list_customers(self):
        expected_customers = [
            Customer(id=uuid4(), name="Customer1", plan_id=uuid4(), date_suscription="2023-01-01"),
            Customer(id=uuid4(), name="Customer2", plan_id=uuid4(), date_suscription="2023-02-01")
        ]
        self.mock_customer_repository.list.return_value = expected_customers
        
        result = self.service.list_customers()
        
        self.assertEqual(result, expected_customers)
        self.mock_customer_repository.list.assert_called_once()

    def test_get_base_plan_issue_fee(self):
        customer_id = uuid4()
        expected_fee = 50.0
        self.mock_customer_repository.get_customer_issue_fee.return_value = expected_fee
        
        result = self.service.get_base_plan_issue_fee(customer_id)
        
        self.assertEqual(result, expected_fee)
        self.mock_customer_repository.get_customer_issue_fee.assert_called_once_with(customer_id)

    def test_get_channel_by_plan(self):
        plan_id = uuid4()
        expected_channels = ["Channel1", "Channel2"]
        self.mock_channel_repository.get_channel_by_plan.return_value = expected_channels
        
        result = self.service.get_channel_by_plan(plan_id)
        
        self.assertEqual(result, expected_channels)
        self.mock_channel_repository.get_channel_by_plan.assert_called_once_with(plan_id)

    def test_get_customer_by_id(self):
        customer_id = uuid4()
        expected_customer = Customer(id=customer_id, name="Customer1", plan_id=uuid4(), date_suscription="2023-01-01")
        self.mock_customer_repository.get_customer_by_id.return_value = expected_customer
        
        result = self.service.get_customer_by_id(customer_id)
        
        self.assertEqual(result, expected_customer)
        self.mock_customer_repository.get_customer_by_id.assert_called_once_with(customer_id)

    def test_get_plan_by_id(self):
        plan_id = uuid4()
        expected_plan = MagicMock()
        self.mock_plan_repository.get_plan_by_id.return_value = expected_plan
        
        result = self.service.get_plan_by_id(plan_id)
        
        self.assertEqual(result, expected_plan)
        self.mock_plan_repository.get_plan_by_id.assert_called_once_with(plan_id)
