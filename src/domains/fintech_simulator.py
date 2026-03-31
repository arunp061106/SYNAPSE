import random
from datetime import datetime, timedelta


class FintechSimulator:

    def __init__(self, user_id):
        self.user_id = user_id
        self.last_time = datetime.utcnow()

    def generate_event(self):

        self.last_time += timedelta(minutes=random.randint(1, 60))

        txn_amount = abs(random.gauss(200, 120))
        balance = abs(random.gauss(5000, 1500))

        fraud_flag = 1 if txn_amount > 800 and random.random() < 0.25 else 0

        event = {
            "domain": "fintech",
            "entity_id": self.user_id,
            "timestamp": self.last_time.isoformat(),
            "transaction_amount": txn_amount,
            "account_balance": balance,
            "fraud_flag": fraud_flag
        }

        return event