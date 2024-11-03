import unittest
from unittest.mock import patch, MagicMock
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from uuid import uuid4

from flaskr.infrastructure.databases.channel_postgresql_repository import ChannelPostgresqlRepository
from flaskr.domain.models import Channel
from flaskr.infrastructure.databases.model_sqlalchemy import ChannelModelSqlAlchemy, ChannelPlanModelSqlAlchemy

class TestChannelPostgresqlRepository(unittest.TestCase):

    @patch('flaskr.infrastructure.databases.channel_postgresql_repository.create_engine')
    @patch('flaskr.infrastructure.databases.channel_postgresql_repository.sessionmaker')
    def setUp(self, mock_sessionmaker, mock_create_engine):
        self.mock_engine = MagicMock()
        mock_create_engine.return_value = self.mock_engine

        self.mock_session = MagicMock()
        self.mock_session_instance = MagicMock()
        self.mock_session.return_value = self.mock_session_instance
        mock_sessionmaker.return_value = self.mock_session

        self.repo = ChannelPostgresqlRepository('mock_connection_string')
        self.repo.Session = self.mock_session

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

