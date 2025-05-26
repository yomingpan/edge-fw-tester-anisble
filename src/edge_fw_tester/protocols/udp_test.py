import socket, struct, random, errno
import time
try:
    from scapy.layers.inet import IP, UDP
    from scapy.sendrecv import sr1
    from scapy.layers.dns import DNS, DNSQR
    from scapy.layers.ntp import NTP
    SCAPY_AVAILABLE = True
except ImportError:
    SCAPY_AVAILABLE = False

def _dns_payload(domain: str = "example.com"):
    return DNS(rd=1, qd=DNSQR(qname=domain))

def _ntp_payload():
    # Simple NTP packet (LI=0, VN=3, Mode=3)
    data = b'\x1b' + 47 * b'\0'
    return data

def _raw_dns_query(domain: str = "example.com"):
    # 產生一個最簡單的 DNS 查詢封包 (A record, 1 question)
    import random
    tid = random.randint(0, 65535)
    # Header: [ID][Flags][QDCOUNT][ANCOUNT][NSCOUNT][ARCOUNT]
    header = struct.pack('>HHHHHH', tid, 0x0100, 1, 0, 0, 0)
    # Question: QNAME (labels), QTYPE, QCLASS
    qname = b''.join([bytes([len(x)]) + x.encode() for x in domain.split('.')]) + b'\x00'
    qtype = struct.pack('>H', 1)  # A
    qclass = struct.pack('>H', 1) # IN
    return header + qname + qtype + qclass

def test_udp(host: str, port: int, payload_type: str = None, timeout: float = 3.0):
    if SCAPY_AVAILABLE and payload_type in ('dns', 'ntp'):
        pkt = IP(dst=host)/UDP(dport=port)
        if payload_type == 'dns':
            pkt /= _dns_payload()
        elif payload_type == 'ntp':
            pkt /= _ntp_payload()
        try:
            ans = sr1(pkt, timeout=timeout, verbose=0)
            if ans:
                return {'status': 'OPEN'}
            else:
                return {'status': 'FILTERED', 'reason': 'no response'}
        except PermissionError:
            # Fallback to socket if scapy needs root
            pass
        except Exception as e:
            return {'status': 'ERROR', 'reason': str(e)}

    # Fallback raw socket approach
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(timeout)
    try:
        if payload_type == 'dns':
            s.sendto(_raw_dns_query(), (host, port))
        elif payload_type == 'ntp':
            s.sendto(_ntp_payload(), (host, port))
        else:
            s.sendto(b'edge-fw-test', (host, port))
        s.recvfrom(512)
        return {'status': 'OPEN'}
    except socket.timeout:
        return {'status': 'FILTERED', 'reason': 'timeout/no response'}
    except ConnectionRefusedError:
        return {'status': 'CLOSED', 'reason': 'ICMP Port Unreachable'}
    except Exception as e:
        return {'status': 'ERROR', 'reason': str(e)}
    finally:
        s.close()
