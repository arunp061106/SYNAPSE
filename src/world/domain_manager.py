import random

from src.domains.ecommerce_simulator import EcommerceSimulator
from src.domains.iot_simulator import IoTSimulator
from src.domains.fintech_simulator import FintechSimulator


class DomainManager:

    def __init__(self, domain):

        if domain == "ecommerce":
            self.simulator_class = EcommerceSimulator
        elif domain == "iot":
            self.simulator_class = IoTSimulator
        elif domain == "fintech":
            self.simulator_class = FintechSimulator
        else:
            raise ValueError("Invalid domain")

    def generate_event(self):

        instance_id = random.randint(1, 100)
        simulator = self.simulator_class(instance_id)

        return simulator.generate_event()