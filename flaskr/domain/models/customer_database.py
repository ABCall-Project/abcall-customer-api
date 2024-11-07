from uuid import UUID

class CustomerDatabase:
    def __init__(self, id: UUID, customer_id: UUID, topic: str, content: str):
        self.id = id
        self.customer_id = customer_id
        self.topic = topic
        self.content = content

    def to_dict(self):
        return {
            'id': str(self.id),
            'customer_id': str(self.customer_id),
            'topic': self.topic,
            'content': self.content
        }