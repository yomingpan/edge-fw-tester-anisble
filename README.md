# Edge Firewall Tester

A Python tool to validate whether network connectivity issues from IoT edge devices
are caused by firewall filtering or by remote‑side service problems.

* Supports **TCP**, **UDP** (DNS 53 / NTP 123 by default) and **ICMP** (ping).
* Uses `socket` for lightweight probing and optionally `scapy` for packet‑level tests.
* Designed to run in bulk via **Ansible AWX**; includes playbook for deployment and result collection.
* Outputs structured JSON; a simple analyzer groups failures by edge or by target.

---
## Quick Start (single host)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/run_tests.py --config config/targets.yaml
```

## Run Tests with pytest

To run unit tests (make sure dependencies are installed):

```bash
# Add src to PYTHONPATH so pytest can find the modules
PYTHONPATH=src .venv/bin/python -m pytest -v tests/
```

## AWX Usage (summary)

1. Import this repo into an AWX Project (SCM type: Git).
2. Create an **Inventory** of edge hosts (SSH reachable).
3. Add credentials for SSH login.
4. Add **edge_fw_test** Job Template using `ansible/playbooks/edge_fw_test.yml`.
5. Launch the job and view results in the AWX UI or download aggregated JSON. JSON output is delimited by `--JSON-START--` markers.

## Notes
* For Scapy packet crafting, running under root or CAP_NET_RAW capability is required.
* Timeout can be adjusted by setting environment variable `EFT_TIMEOUT`.

Detailed docs in `docs/usage_guide.md`.
