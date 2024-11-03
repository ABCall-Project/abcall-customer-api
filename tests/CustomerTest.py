import unittest
from uuid import uuid4
from datetime import datetime
from flaskr.domain.models.customer import Customer

class TestCustomer(unittest.TestCase):
    def setUp(self):
        self.sample_id = uuid4()
        self.sample_name = "Sample Customer"
        self.sample_plan_id = uuid4()
        self.sample_date_suscription = datetime(2023, 1, 1)
        self.customer = Customer(
            id=self.sample_id,
            name=self.sample_name,
            plan_id=self.sample_plan_id,
            date_suscription=self.sample_date_suscription
        )

    def test_init(self):
        self.assertEqual(self.customer.id, self.sample_id)
        self.assertEqual(self.customer.name, self.sample_name)
        self.assertEqual(self.customer.plan_id, self.sample_plan_id)
        self.assertEqual(self.customer.date_suscription, self.sample_date_suscription)

    def test_to_dict(self):
        expected_dict = {
            'id': str(self.sample_id),
            'name': self.sample_name,
            'plan_id': str(self.sample_plan_id),
            'date_suscription': self.sample_date_suscription.isoformat()
        }
        self.assertEqual(self.customer.to_dict(), expected_dict)

    def test_to_dict_date_suscription_none(self):
        self.customer.date_suscription = None
        expected_dict = {
            'id': str(self.sample_id),
            'name': self.sample_name,
            'plan_id': str(self.sample_plan_id),
            'date_suscription': None
        }
        self.assertEqual(self.customer.to_dict(), expected_dict)
