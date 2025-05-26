
import subprocess, platform, shlex

def test_icmp(host: str, timeout: float = 2.0):
    param = '-n' if platform.system().lower()=='windows' else '-c'
    cmd = f"ping {param} 1 -W {int(timeout)} {shlex.quote(host)}"
    proc = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode == 0:
        return {'status': 'REACHABLE'}
    else:
        return {'status': 'UNREACHABLE', 'reason': 'ping failed'}
