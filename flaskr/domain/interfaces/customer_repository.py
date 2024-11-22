from typing import List, Optional
from uuid import UUID
from ..models.customer import Customer

class CustomerRepository:
    def list(self) -> List[Customer]:
        raise NotImplementedError
    
    def get_customer_by_id(self,customer_id):
         raise NotImplementedError
    
    def get_customer_plan(self,customer_id):
        raise NotImplementedError

    def get_customer_issue_fee(self,customer_id):
        raise NotImplementedError
    
    def create_customer(self, name, plan_id, document):
        raise NotImplementedError
    
    def add_customers(self, customers: List[dict], plan_id: UUID) -> List[Customer]:
        raise NotImplementedError

    def get_customer_by_document(self, document: str) -> Optional[Customer]:
        raise NotImplementedError