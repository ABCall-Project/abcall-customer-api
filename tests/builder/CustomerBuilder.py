from uuid import uuid4, UUID
from flaskr.domain.models.PlanEnum import PlanEnum
from datetime import datetime
from flaskr.domain.models.customer import Customer

class CustomerBuilder:
    def __init__(self):
        self.id = UUID('e4a0b9f3-3e78-49bc-a4d0-d60fd8b6f574')
        self.name = 'Test Customer'
        self.plan_id = UUID(PlanEnum.ENTREPRENEUR.value)
        self.date_suscription = datetime.strptime('2021-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
    
    def with_id(self, id:UUID):
        self.id = id
        return self

    def with_name(self, name:str):
        self.name = name
        return self
    
    def with_plan_id(self, plan_id:UUID):
        self.plan_id = plan_id
        return self
    
    def with_date_suscription(self, date_suscription:datetime):
        self.date_suscription = date_suscription
        return self
    
    def build(self):
        return Customer(self.id, self.name, self.plan_id, self.date_suscription)
