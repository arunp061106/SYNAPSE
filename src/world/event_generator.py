from src.world.domain_manager import DomainManager


class UserSimulator:

    def __init__(self, _id, domain):
        self.manager = DomainManager(domain)

    def generate_event(self):
        return self.manager.generate_event()