
import socket, errno

def test_tcp(host: str, port: int, timeout: float = 3.0):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        code = s.connect_ex((host, port))
        if code == 0:
            return {'status': 'OPEN'}
        elif code == errno.ECONNREFUSED:
            return {'status': 'CLOSED', 'reason': 'Connection refused by host'}
        else:
            return {'status': 'FILTERED', 'reason': f'socket error {code}'}
    except socket.timeout:
        return {'status': 'FILTERED', 'reason': 'timeout'}
    except Exception as e:
        return {'status': 'ERROR', 'reason': str(e)}
    finally:
        s.close()
