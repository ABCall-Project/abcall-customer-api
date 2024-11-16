from typing import List, Optional
from uuid import UUID
from ...domain.models import Plan
from ...domain.interfaces import PlanRepository
from ...infrastructure.databases.model_sqlalchemy import Base, PlanModelSqlAlchemy
from .postgres.db import Session, engine
from ...utils import Logger

log = Logger()

class PlanPostgresqlRepository(PlanRepository):
    def __init__(self):
        self.engine = engine
        self.session = Session
        self._create_tables()

    def _create_tables(self):
        Base.metadata.create_all(self.engine)

    
    def get_rate_plan(self,plan_id):
        with self.session() as session:
            try:
                log.info(f'the plan id {plan_id}')
                return session.query(PlanModelSqlAlchemy.basic_monthly_rate).filter(PlanModelSqlAlchemy.id == plan_id).first()
            finally:
                session.close()

    def get_plan_by_id(self,plan_id):
        with self.session() as session:
            try:
                result = session.query(PlanModelSqlAlchemy).filter_by(id=plan_id).first()
                if result:
                    return self._from_model(result)
                else:
                    return None
            finally:
                session.close()

    def _from_model(self, model: PlanModelSqlAlchemy) -> Plan:
        return Plan(
            id=model.id,
            name=model.name,
            basic_monthly_rate=model.basic_monthly_rate,
            issue_fee=model.issue_fee
        )
