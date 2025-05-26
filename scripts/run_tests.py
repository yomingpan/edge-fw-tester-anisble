#!/usr/bin/env python3
import sys, os
# Add src to sys.path for module resolution
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from edge_fw_tester.tester import main

if __name__ == '__main__':
    main()
