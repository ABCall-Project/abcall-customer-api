from datetime import datetime, timezone
from typing import List, Optional
from uuid import UUID, uuid4
from ...domain.models import Customer
from ...domain.interfaces import CustomerRepository
from ...infrastructure.databases.model_sqlalchemy import Base, CustomerModelSqlAlchemy,PlanModelSqlAlchemy
from .postgres.db import Session, engine

class CustomerPostgresqlRepository(CustomerRepository):
    def __init__(self):
        self.engine = engine
        self.session = Session
        self._create_tables()

    def _create_tables(self):
        Base.metadata.create_all(self.engine)


    def get_customer_plan(self,customer_id):
        with self.session() as session:
            try:
                result= session.query(PlanModelSqlAlchemy.basic_monthly_rate).join(CustomerModelSqlAlchemy, CustomerModelSqlAlchemy.plan_id == PlanModelSqlAlchemy.id).filter(CustomerModelSqlAlchemy.id == customer_id).first()
                return float(result[0])
            finally:
                session.close()

    def get_customer_issue_fee(self,customer_id):
        with self.session() as session:
            try:
                result= session.query(PlanModelSqlAlchemy.issue_fee).join(CustomerModelSqlAlchemy, CustomerModelSqlAlchemy.plan_id == PlanModelSqlAlchemy.id).filter(CustomerModelSqlAlchemy.id == customer_id).first()
                return float(result[0])
            finally:
                session.close()


    def list(self) -> List[Customer]:
        with self.session() as session:
            try:
                customer_models = session.query(CustomerModelSqlAlchemy).all()
                return [self._from_model(customer_model) for customer_model in customer_models]
            finally:
                session.close()


    def _from_model(self, model: CustomerModelSqlAlchemy) -> Customer:
        return Customer(
            id=model.id,
            document=model.document,
            name=model.name,
            plan_id=model.plan_id,
            date_suscription=model.date_suscription
        )
    

    def get_customer_by_id(self,customer_id):
        with self.session() as session:
            try:
                result = session.query(CustomerModelSqlAlchemy).filter_by(id=customer_id).first()
                if result:
                    return self._from_model(result)
                else:
                    return None
            finally:
                session.close()            
    
    def create_customer(self, name, plan_id, document = None):
        with self.session() as session:
            try:
                customer = CustomerModelSqlAlchemy(
                    name=name,
                    plan_id=plan_id,
                    document=document
                )
                session.add(customer)
                session.commit()
                session.refresh(customer)
                return self._from_model(customer)
            except Exception as ex:
                raise ex
            finally:
                session.close()        

    def add_customers(self, customers: List[dict], plan_id: UUID) -> List[Customer]: 
        with self.session() as session:
            successful_customers = []
            try:
                for customer_data in customers:
                    document = customer_data.get('document')
                    name = customer_data.get('name')

                    if document and name:
                        customer_model = CustomerModelSqlAlchemy(
                            id=uuid4(),
                            document=document,
                            name=name,
                            plan_id=plan_id,
                            date_suscription=datetime.now(timezone.utc)
                        )
                        session.add(customer_model)
                        successful_customers.append(self._from_model(customer_model))

                session.commit()
                return successful_customers
            except Exception as e:
                session.rollback()
                raise e
            finally:
                session.close()
    
    def get_customer_by_document(self, document: str) -> Optional[Customer]:
        with self.session() as session:
            try:
                result = session.query(CustomerModelSqlAlchemy).filter_by(document=document).first()
                if result:
                    return self._from_model(result)
                else:
                    return None
            finally:
                session.close()
