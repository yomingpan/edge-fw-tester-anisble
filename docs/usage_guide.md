
# Usage Guide

## 1. Configuration
Modify `config/targets.yaml` to list the destinations you want to test.

| field | description | example |
|-------|-------------|---------|
| name  | identifier of the target | `public-dns` |
| host  | hostname / IP | `8.8.8.8` |
| port  | integer port (omit for ICMP) | `53` |
| proto | tcp / udp / icmp | `udp` |
| payload | Optional hint to send protocol‑specific payload (`dns`, `ntp`) | `dns` |

## 2. Local run
Install Python 3.8+ and dependencies:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
Execute:
```bash
python scripts/run_tests.py --config config/targets.yaml
```

## 3. AWX deployment
1. Import the repo as a Project.
2. Create Inventory containing all edge hosts (via SSH).
3. Add credentials for SSH login.
4. Create Job Template using `ansible/playbooks/edge_fw_test.yml`.
5. Launch job and inspect results; JSON output is delimited by `--JSON-START--` markers.

## Notes
* For Scapy packet crafting, running under root or CAP_NET_RAW capability is required.
* Timeout can be adjusted by setting environment variable `EFT_TIMEOUT`.
