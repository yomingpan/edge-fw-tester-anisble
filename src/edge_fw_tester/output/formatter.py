from collections import defaultdict
import json, sys

def summarise_results(results):
    # Simple console summary
    print("\nTest Summary")
    print("="*50)
    flat_results = []
    for r in results:
        # 展開 multi_port 結果
        if 'multi_port' in r:
            for sub in r['multi_port']:
                name = r.get('name') or f"{r['host']}:{sub.get('port','')}"
                print(f"{name:<25} {r['proto'].upper():<4} {sub['port']:<5} {sub['status']:<10} {sub.get('reason','')}")
                flat_results.append({**r, **sub})
        else:
            name = r.get('name') or f"{r['host']}:{r.get('port','')}"
            print(f"{name:<25} {r['proto'].upper():<4} {r.get('port',''):<5} {r['status']:<10} {r.get('reason','')}")
            flat_results.append(r)
    print("-"*50)
    stats = defaultdict(int)
    for r in flat_results:
        stats[r['status']] += 1
    print("Status counts:")
    for k,v in stats.items():
        print(f"  {k:<10}: {v}")
    # also output machine-readable JSON at end, separated by marker
    print("\n--JSON-START--")
    print(json.dumps(flat_results, ensure_ascii=False))
    print("--JSON-END--")
