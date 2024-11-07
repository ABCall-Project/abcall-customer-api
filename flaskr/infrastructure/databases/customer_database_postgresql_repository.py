from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import List
from uuid import UUID, uuid4
from ...domain.models.customer_database import CustomerDatabase
from ...infrastructure.databases.model_sqlalchemy import Base, CustomerDatabaseModelSqlAlchemy

class CustomerDatabasePostgresqlRepository:
    def __init__(self, connection_string: str):
        self.engine = create_engine(connection_string)
        self.Session = sessionmaker(bind=self.engine)
        self._create_tables()

    def _create_tables(self):
        Base.metadata.create_all(self.engine)

    def add_customer_database_entries(self, customer_id: UUID, entries: List[dict]) -> List[CustomerDatabase]:      
        session = self.Session()
        successful_entries = []

        try:
            for entry in entries:
                topic = entry.get('topic')
                content = entry.get('content')
                
                if topic and content:
                    customer_entry = CustomerDatabaseModelSqlAlchemy(
                        id=uuid4(),
                        customer_id=customer_id,
                        topic=topic,
                        content=content
                    )
                    session.add(customer_entry)
                    successful_entries.append(self._from_customer_database_model(customer_entry))

            session.commit()
            return successful_entries
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def _from_customer_database_model(self, model: CustomerDatabaseModelSqlAlchemy) -> CustomerDatabase:
        return CustomerDatabase(
            id=model.id,
            customer_id=model.customer_id,
            topic=model.topic,
            content=model.content
        )