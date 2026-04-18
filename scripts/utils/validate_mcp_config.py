#!/usr/bin/env python3
"""Validate VSCode MCP JSON configuration"""

import json
import sys
from pathlib import Path

config_path = Path(r"c:\Users\Owen\AppData\Roaming\Code\User\mcp.json")

try:
    with open(config_path) as f:
        config = json.load(f)
    print("✓ JSON configuration is valid")
    print(f"✓ Found {len(config.get('servers', {}))} MCP servers configured:")
    for server_name in config.get('servers', {}).keys():
        print(f"  - {server_name}")
except json.JSONDecodeError as e:
    print(f"✗ JSON Syntax Error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"✗ Error: {e}")
    sys.exit(1)
