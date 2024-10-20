from typing import List
from ..domain.models import Customer
import requests
from ..domain.interfaces.customer_repository import CustomerRepository
from ..domain.interfaces.plan_repository import PlanRepository
import uuid
from datetime import datetime
from ..utils import Logger
from  config import Config

class CustomerService:
    def __init__(self, customer_repository: CustomerRepository,plan_repository: PlanRepository):
        self.log = Logger()
        self.customer_repository=customer_repository
        self.plan_repository=plan_repository


    def get_base_plan_suscription_rate(self, customer_id):
        """
        This method query base plan rate by customer id
        Args: 
            customer_id (UUID): customer id
        Returns:
            customer_plan_rate: (decimal)
        """
        customer_plan_rate = self.customer_repository.get_customer_plan(customer_id)
        return customer_plan_rate
    
    def list_customers(self):
        """
        This method query all customers
        Args: 
            none
        Returns:
            customers: (list)
        """
        list_customers=self.customer_repository.list()
        return list_customers
    

    def get_base_plan_issue_fee(self, customer_id):
        """
        This method query base plan issue fee customer id
        Args: 
            customer_id (UUID): customer id
        Returns:
            customer_plan_rate: (decimal)
        """
        issue_fee = self.customer_repository.get_customer_issue_fee(customer_id)
        return issue_fee

    