from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import List, Optional
from uuid import UUID
from ...domain.models import Customer
from ...domain.interfaces import CustomerRepository
from ...infrastructure.databases.model_sqlalchemy import Base, CustomerModelSqlAlchemy,PlanModelSqlAlchemy


class CustomerPostgresqlRepository(CustomerRepository):
    def __init__(self, connection_string: str):
        self.engine = create_engine(connection_string)
        self.Session = sessionmaker(bind=self.engine)
        self._create_tables()

    def _create_tables(self):
        Base.metadata.create_all(self.engine)


    def get_customer_plan(self,customer_id):
        session = self.Session()
        try:
            result= session.query(PlanModelSqlAlchemy.basic_monthly_rate).join(CustomerModelSqlAlchemy, CustomerModelSqlAlchemy.plan_id == PlanModelSqlAlchemy.id).filter(CustomerModelSqlAlchemy.id == customer_id).first()
            return float(result[0])
        finally:
            session.close()

    def get_customer_issue_fee(self,customer_id):
        session = self.Session()
        try:
            result= session.query(PlanModelSqlAlchemy.issue_fee).join(CustomerModelSqlAlchemy, CustomerModelSqlAlchemy.plan_id == PlanModelSqlAlchemy.id).filter(CustomerModelSqlAlchemy.id == customer_id).first()
            return float(result[0])
        finally:
            session.close()


    def list(self) -> List[Customer]:
        session = self.Session()
        try:
            customer_models = session.query(CustomerModelSqlAlchemy).all()
            return [self._from_model(customer_model) for customer_model in customer_models]
        finally:
            session.close()


    def _from_model(self, model: CustomerModelSqlAlchemy) -> Customer:
        return Customer(
            id=model.id,
            name=model.name,
            plan_id=model.plan_id,
            date_suscription=model.date_suscription
        )
