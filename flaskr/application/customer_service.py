from typing import List
from ..domain.models import Customer
import requests
from ..domain.interfaces.customer_repository import CustomerRepository
from ..domain.interfaces.customer_database_repository import CustomerDatabaseRepository
from ..domain.interfaces.plan_repository import PlanRepository
from ..domain.interfaces.channel_repository import ChannelRepository
import uuid
from datetime import datetime
from ..utils import Logger
from  config import Config

class CustomerService:
    def __init__(self, customer_repository: CustomerRepository,plan_repository: PlanRepository, channel_repository:ChannelRepository, customer_database_repository:CustomerDatabaseRepository):
        self.log = Logger()
        self.customer_repository=customer_repository
        self.plan_repository=plan_repository
        self.channel_repository = channel_repository
        self.customer_database_repository = customer_database_repository        

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
        
    def get_channel_by_plan(self, plan_id):
        """
        This method query base plan issue fee customer id
        Args: 
            plan_id (UUID): plan_id id
        Returns:
            channels: (list)
        """
        channels = self.channel_repository.get_channel_by_plan(plan_id)
        return channels
    

    def get_customer_by_id(self,customer_id):
        """
        This method query customer by id
        Args: 
            customer_id (UUID): customer id
        Returns:
            customer: (Customer)
        """
        return self.customer_repository.get_customer_by_id(customer_id)
    
    def get_plan_by_id(self,plan_id):
        """
        This method query plan by id
        Args: 
            plan_id (UUID): plan id
        Returns:
            plan: (Plan)
        """
        return self.plan_repository.get_plan_by_id(plan_id)

    def load_customer_database_entries(self, customer_id: uuid.UUID, entries: List[dict]) -> List[Customer]:
        """
        This method loads multiple entries for a customer into the customer database.
        
        Args:
            customer_id (UUID): The customer ID associated with each entry.
            entries (List[dict]): List of entries with 'topic' and 'content'.
        
        Returns:
            List[CustomerDatabase]: List of successfully added entries.
        """
        self.log.info(f"Loading entries for customer ID: {customer_id}")
        added_entries = self.customer_database_repository.add_customer_database_entries(customer_id, entries)
        self.log.info(f"Successfully loaded {len(added_entries)} entries for customer ID: {customer_id}")
        return added_entries
    
    def create_customer(self, name, plan_id):
        """
        This method creates a new customer.
        
        Args:
            name (str): The name of the customer.
            plan_id (UUID): The plan ID associated with the customer.
        
        Returns:
            Customer: The newly created customer.
        """
        self.log.info(f"Creating new customer: {name}")
        customer = self.customer_repository.create_customer(name, plan_id)
        self.log.info(f"Successfully created new customer: {name}")
        return customer
    