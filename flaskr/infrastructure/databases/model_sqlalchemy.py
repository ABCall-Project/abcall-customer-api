from sqlalchemy import Column, String, Numeric, DateTime,ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import uuid
#from .plan_model_sqlalchemy import PlanModelSqlAlchemy

Base = declarative_base()

class PlanModelSqlAlchemy(Base):
    __tablename__ = 'plan'
    
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    basic_monthly_rate=Column(Numeric(10, 2), nullable=False)
    issue_fee=Column(Numeric(10, 2), nullable=False)

class CustomerModelSqlAlchemy(Base):
    __tablename__ = 'customer'
    
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    plan_id=Column(PG_UUID(as_uuid=True),ForeignKey('plan.id'), default=uuid.uuid4)
    date_suscription=Column(DateTime(timezone=True), default=func.now())
    plan = relationship("PlanModelSqlAlchemy")

class ChannelModelSqlAlchemy(Base):
    __tablename__ = 'channel'
    
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)

class ChannelPlanModelSqlAlchemy(Base):
    __tablename__ = 'channel_plan'
    
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    plan_id=Column(PG_UUID(as_uuid=True),ForeignKey('plan.id'), default=uuid.uuid4)
    channel_id=Column(PG_UUID(as_uuid=True),ForeignKey('channel.id'), default=uuid.uuid4)
    plan = relationship("PlanModelSqlAlchemy")
    channel = relationship("ChannelModelSqlAlchemy")