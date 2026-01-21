from policies.policy import Policy

class PortServicePolicy(Policy):
    def __init__(self, disallowlist, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.disallowlist = disallowlist

    def evaluate(self, item):
        process = item["process_name"]
        local_port = item["local_port"]
        remote_port = item["remote_port"]
    
        blocked_ports = self.disallowlist.get(process, [])
    
        if local_port in blocked_ports or remote_port in blocked_ports:
            return False  # חסום → יהרוג רק את ה-PID הזה
    
        return True

