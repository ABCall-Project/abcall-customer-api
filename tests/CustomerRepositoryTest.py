import unittest
from flaskr.domain.interfaces.customer_repository import CustomerRepository
class CustomerRepositoryTestCase(unittest.TestCase):
    def setUp(self):
        self.repo = CustomerRepository()

    def test_list_implementation(self):
        with self.assertRaises(NotImplementedError):
            self.repo.list()
    
    def test_get_customer_by_id_implementation(self):
        with self.assertRaises(NotImplementedError):
            self.repo.get_customer_by_id(customer_id=None)

    def test_get_customer_plan_implementation(self):
        with self.assertRaises(NotImplementedError):
            self.repo.get_customer_plan(customer_id=None)

    def test_get_customer_issue_fee_implementation(self):
        with self.assertRaises(NotImplementedError):
            self.repo.get_customer_issue_fee(customer_id=None)
    
    def test_create_customer_implementation(self):
        with self.assertRaises(NotImplementedError):
            self.repo.create_customer(name='', plan_id=None, document=None)