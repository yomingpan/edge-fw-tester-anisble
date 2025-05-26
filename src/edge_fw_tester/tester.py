import socket, yaml, json, time, os, sys
from pathlib import Path
from .protocols import tcp_test, udp_test, icmp_test
from .output.formatter import summarise_results

DEFAULT_TIMEOUT = float(os.getenv("EFT_TIMEOUT", "3"))

def load_targets(config_path: str):
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def test_target(target):
    host = target['host']
    port = target.get('port')
    proto = target['proto'].lower()
    payload = target.get('payload', None)
    # Fix: If port is a string and contains commas, convert to int and test each one
    if isinstance(port, str) and ',' in port:
        port_list = [int(p.strip()) for p in port.split(',')]
    elif isinstance(port, str):
        port_list = [int(port.strip())]
    elif isinstance(port, int):
        port_list = [port]
    else:
        port_list = []
    results = []
    for p in port_list:
        if proto == 'tcp':
            res = tcp_test.test_tcp(host, p, DEFAULT_TIMEOUT)
        elif proto == 'udp':
            res = udp_test.test_udp(host, p, payload, DEFAULT_TIMEOUT)
        elif proto == 'icmp':
            res = icmp_test.test_icmp(host, DEFAULT_TIMEOUT)
        else:
            res = {'status': 'ERROR', 'reason': f'Unsupported proto {proto}'}
        results.append({'port': p, **res})
    # If only one port, return single result, otherwise return all results
    if len(results) == 1:
        return results[0]
    return {'multi_port': results}

def run_tests(target_list):
    results = []
    for tgt in target_list:
        res = test_target(tgt)
        results.append({
            'name': tgt.get('name'),
            'host': tgt['host'],
            'port': tgt.get('port'),
            'proto': tgt['proto'],
            **res
        })
    return results

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Edge Firewall Tester")
    parser.add_argument('--config', required=True, help='YAML file with targets')
    parser.add_argument('--json', action='store_true', help='Output raw JSON (no summary)')
    args = parser.parse_args()

    targets = load_targets(args.config)
    results = run_tests(targets)

    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        summarise_results(results)

if __name__ == '__main__':
    main()
