from time import sleep
from policy_tools.logger import Logger
from policy_tools.ConfigurationManager import ConfigurationManager
from policy_tools.Enforcer import Enforcer
from policy_tools.policy_rules_engine import PolicyEngine
from policy_tools.network_scanner import Scanner

from policies.port_service_policy import PortServicePolicy 

logger = Logger()
config_manager = ConfigurationManager()

disallowlist = config_manager.load_allowlist("not_evil_fire_wall\\disallowlist.json")
# print(disallowlist)

scanner = Scanner()
scanner.start()
enforcer = Enforcer(logger)

port_policy = PortServicePolicy(
    name="Port Service Allowlist",
    scanner=scanner,
    enforcer=enforcer,
    logger=logger,
    interval=10,
    disallowlist=disallowlist
)

engine = PolicyEngine(logger)
engine.add_policy(port_policy)
engine.start()

logger.info("Firewall engine is running")

while True:
    sleep(1)
