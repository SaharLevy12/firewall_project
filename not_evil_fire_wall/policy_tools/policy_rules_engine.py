import threading

class PolicyEngine:
    def __init__(self, logger):
        self.logger = logger
        self.policies = []

    def add_policy(self, policy):
        self.policies.append(policy)

    def start(self):
        for policy in self.policies:
            thread = threading.Thread(target=policy.run, daemon=True)
            thread.start()
            self.logger.info(f"Thread started for policy: {policy.name}")
