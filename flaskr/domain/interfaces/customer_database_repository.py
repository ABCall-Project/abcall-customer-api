from typing import List
from uuid import UUID
from ..models.customer_database import CustomerDatabase

class CustomerDatabaseRepository:
    def add_customer_database_entries(self, customer_id: UUID, entries: List[dict]) -> List[CustomerDatabase]:        
        raise NotImplementedError
