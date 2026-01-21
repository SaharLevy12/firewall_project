import time

class Policy:
    def __init__(self, name, logger, enforcer, scanner, interval=1):
        self.name = name
        self.logger = logger
        self.enforcer = enforcer
        self.scanner = scanner
        self.interval = interval

    def evaluate(self, item):
        raise NotImplementedError("Policy must implement evaluate()")

    def run(self):
        self.logger.info(f"Policy started: {self.name}")

        while True:
            data = self.scanner.get_current_connections()

            for item in data:
                # print("item - ",item) 
                if self.evaluate(item):
                    self.enforcer.allow(item, self.name)
                else:
                    self.enforcer.block(item, self.name)

            time.sleep(self.interval)

