import psutil

class Enforcer:
    def __init__(self, logger):
        self.logger = logger
        self.killed_pids = set()  # כדי לא להרוג שוב ושוב אותו PID

    def allow(self, item, policy_name):
        pass

    def block(self, item, policy_name):
        pid = item.get("process_id")
        process_name = item.get("process_name", "")
        port = item.get("remote_port") or item.get("local_port")

        if not pid:
            return

        if pid in self.killed_pids:
            return  # כבר הרגנו אותו

        try:
            proc = psutil.Process(pid)

            self.logger.warning(
                f"[{policy_name}] KILLING PID {pid} ({process_name}) using port {port}"
            )

            proc.kill()
            self.killed_pids.add(pid)

        except psutil.NoSuchProcess:
            pass
        except psutil.AccessDenied:
            self.logger.error(f"No permission to kill {pid}")
        except Exception as e:
            self.logger.error(f"Kill failed: {e}")
