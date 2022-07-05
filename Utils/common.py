import ipaddress
import subprocess


def ping_xavier(ip, count):
    for i in range(count):
        process = subprocess.Popen("ping {} -t 1".format(ip), shell=True, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        print(i + 1, stdout)
        if stdout is not None and b'64 bytes from' in stdout:
            return True
    return False


def check_ip_valid(ip):
    try:
        ipaddress.ip_address(ip.strip())
        return True
    except Exception as e:
        return False
