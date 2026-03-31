import random
from datetime import datetime, timedelta


class EcommerceSimulator:

    def __init__(self, user_id):
        self.user_id = user_id
        self.last_time = datetime.utcnow()

    def generate_event(self):

        self.last_time += timedelta(minutes=random.randint(1, 10))

        event = {
            "domain": "ecommerce",
            "entity_id": self.user_id,
            "timestamp": self.last_time.isoformat(),
            "event_type": random.choice(["browse", "add_to_cart", "purchase"]),
            "transaction_amount": abs(random.gauss(80, 30))
        }

        return event