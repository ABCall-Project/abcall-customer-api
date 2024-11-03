from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import List
from ...domain.models import  Channel
from ...domain.interfaces import ChannelRepository
from .model_sqlalchemy import Base, ChannelModelSqlAlchemy,ChannelPlanModelSqlAlchemy

class ChannelPostgresqlRepository(ChannelRepository):
    def __init__(self, connection_string: str):
        self.engine = create_engine(connection_string)
        self.Session = sessionmaker(bind=self.engine)
        self._create_tables()

    def _create_tables(self):
        Base.metadata.create_all(self.engine)

    def get_channel_by_plan(self, plan_id) ->List[Channel]:
        session = self.Session()
        try:
            print(f'el plan id {plan_id}')
            channel_plans = session.query(ChannelPlanModelSqlAlchemy).filter(ChannelPlanModelSqlAlchemy.plan_id == plan_id).all()
            channel_ids = [channel_plan.channel_id for channel_plan in channel_plans]
            channels_models = session.query(ChannelModelSqlAlchemy).filter(ChannelModelSqlAlchemy.id.in_(channel_ids)).all()
            return [self._from_channel_model(channel_models) for channel_models in channels_models]  
        finally:
            session.close()

    def _from_channel_model(self, model: ChannelModelSqlAlchemy) -> Channel:
        return Channel(
            id=model.id,
            name=model.name,
        )