from typing import List, Optional
from uuid import UUID
from ..models.plan import Plan

class PlanRepository:
    def list(self) -> List[Plan]:
        raise NotImplementedError