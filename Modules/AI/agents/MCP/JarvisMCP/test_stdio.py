#!/usr/bin/env python
"""
Test runner: Start JarvisMCP in stdio mode
"""
import os
import sys

os.environ['JARVIS_TRANSPORT'] = 'stdio'
os.environ['JARVIS_DEBUG'] = 'true'

# Add current dir to path
sys.path.insert(0, '.')

if __name__ == '__main__':
    from server import mcp
    print("Starting JarvisMCP in stdio mode...", file=sys.stderr)
    mcp.run(transport='stdio')
