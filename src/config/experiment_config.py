import random

from src.domains.ecommerce_simulator import EcommerceSimulator
from src.domains.iot_simulator import IoTSimulator
from src.domains.fintech_simulator import FintechSimulator



class ExperimentConfig:

    def __init__(self, dataset_size=10000, synthetic_ratio=1.0, domain="ecommerce"):
        self.dataset_size = dataset_size
        self.synthetic_ratio = synthetic_ratio
        self.domain = domain