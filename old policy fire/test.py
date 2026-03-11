import socket
import time

def get_domain_ips(domain, attempts=50, delay=1):
    ips = set()

    for _ in range(attempts):
        try:
            result = socket.gethostbyname_ex(domain)[2]
            ips.update(result)
        except:
            pass
        time.sleep(delay)

    return ips


print(get_domain_ips("youtube.com", 20))