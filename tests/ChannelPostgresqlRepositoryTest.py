import unittest
from unittest.mock import patch, MagicMock
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from uuid import uuid4

from flaskr.infrastructure.databases.channel_postgresql_repository import ChannelPostgresqlRepository
from flaskr.domain.models import Channel
from flaskr.infrastructure.databases.model_sqlalchemy import ChannelModelSqlAlchemy, ChannelPlanModelSqlAlchemy

class TestChannelPostgresqlRepository(unittest.TestCase):

    @patch('flaskr.infrastructure.databases.channel_postgresql_repository.engine')
    @patch('flaskr.infrastructure.databases.channel_postgresql_repository.Session')
    def setUp(self, mock_session, mock_engine):
        mock_engine.return_value = mock_engine

        self.mock_session_instance = mock_session.return_value.__enter__.return_value

        self.repo = ChannelPostgresqlRepository()

    def test_get_channel_by_plan(self):
        plan_id = uuid4()
        channel_plan = ChannelPlanModelSqlAlchemy(
            id=uuid4(),
            channel_id=uuid4(),
            plan_id=plan_id
        )
        channel_model = ChannelModelSqlAlchemy(
            id=channel_plan.channel_id,
            name="Test Channel"
        )
        self.mock_session_instance.query.return_value.filter.return_value.all.side_effect = [[channel_plan], [channel_model]]

        result = self.repo.get_channel_by_plan(plan_id)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].id, channel_model.id)
        self.assertEqual(result[0].name, "Test Channel")
        self.mock_session_instance.query.assert_any_call(ChannelPlanModelSqlAlchemy)
        self.mock_session_instance.query.assert_any_call(ChannelModelSqlAlchemy)

