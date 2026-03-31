import random
from datetime import datetime, timedelta


class IoTSimulator:

    def __init__(self, device_id):
        self.device_id = device_id
        self.last_time = datetime.utcnow()

    def generate_event(self):

        self.last_time += timedelta(seconds=random.randint(5, 60))

        event = {
            "domain": "iot",
            "entity_id": self.device_id,
            "timestamp": self.last_time.isoformat(),
            "temperature": random.uniform(20, 80),
            "humidity": random.uniform(30, 90),
            "device_status": random.choice(["ok", "warning", "critical"])
        }

        return event