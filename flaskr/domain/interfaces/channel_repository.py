from typing import List, Optional
from uuid import UUID
from ..models.channel import Channel

class ChannelRepository:
    def list(self) -> List[Channel]:
        raise NotImplementedError
    
    def get_channel_by_plan(self, plan_id) ->List[Channel]:
        raise NotImplementedError