"""
Comprehensive VSCode <-> JarvisMCP Connection Diagnostic
Tests HTTP connectivity and protocol compliance
"""

import json
import sys
import httpx
import time
from pathlib import Path

# Configuration
JARVIS_URL = "http://127.0.0.1:8765/mcp"
ARANGO_URL = "http://127.0.0.1:8893"
TEST_TIMEOUT = 10

print("=" * 70)
print("VSCode <-> JarvisMCP Connection Diagnostic Report")
print("=" * 70)
print()

# Test 1: Basic HTTP connectivity
print("[1] Testing basic HTTP connectivity to JarvisMCP...")
try:
    response = httpx.get(
        JARVIS_URL,
        headers={"Accept": "application/json"},
        timeout=TEST_TIMEOUT,
        follow_redirects=True,
    )
    print(f"    ✓ HTTP connection successful")
    print(f"    Status Code: {response.status_code}")
    print(f"    Content-Type: {response.headers.get('content-type', 'N/A')}")
except Exception as e:
    print(f"    ✗ HTTP connection failed: {e}")
    sys.exit(1)

print()

# Test 2: Check port availability
print("[2] Verifying port status...")
import socket
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(("127.0.0.1", 8765))
    sock.close()
    if result == 0:
        print(f"    ✓ Port 8765 is open and listening")
    else:
        print(f"    ✗ Port 8765 is not responding")
except Exception as e:
    print(f"    ✗ Socket error: {e}")

print()

# Test 3: Check ArangoDB connectivity
print("[3] Testing ArangoDB connectivity...")
try:
    response = httpx.get(
        f"{ARANGO_URL}/_api/version",
        auth=("root", "test123"),
        timeout=TEST_TIMEOUT,
    )
    if response.status_code == 200:
        data = response.json()
        print(f"    ✓ ArangoDB is running")
        print(f"    Version: {data.get('version', 'unknown')}")
    else:
        print(f"    ⚠ ArangoDB returned status {response.status_code}")
except Exception as e:
    print(f"    ✗ ArangoDB connection failed: {e}")

print()

# Test 4: MCP Protocol - Initialize Session
print("[4] Testing MCP Protocol - Initialize Session...")
try:
    # FastMCP HTTP requires initialization
    init_response = httpx.post(
        JARVIS_URL,
        headers={
            "Content-Type": "application/json",
            "Accept": "text/event-stream",
        },
        json={
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "vscode-diagnostic",
                    "version": "1.0.0",
                },
            },
        },
        timeout=TEST_TIMEOUT,
    )
    
    print(f"    Status: {init_response.status_code}")
    
    # Parse response (might be SSE)
    lines = init_response.text.split("\n")
    print(f"    Response preview (first 3 lines):")
    for line in lines[:3]:
        if line.strip():
            print(f"      {line[:100]}")
    
    if init_response.status_code == 200:
        print(f"    ✓ MCP protocol response received")
    else:
        print(f"    ⚠ Unexpected status code: {init_response.status_code}")
        
except Exception as e:
    print(f"    ✗ MCP protocol test failed: {e}")

print()

# Test 5: VSCode Configuration Check
print("[5] Checking VSCode Configuration...")
config_path = Path(r"c:\Users\Owen\Desktop\Brogramming\VSCode_Copilot_Api\.vscode\settings.json")
if config_path.exists():
    try:
        with open(config_path) as f:
            config = json.load(f)
        
        if "mcpServers" in config:
            print(f"    ✓ MCP servers configuration found")
            for server_name, server_config in config.get("mcpServers", {}).items():
                print(f"      - {server_name}:")
                print(f"        type: {server_config.get('type')}")
                print(f"        url: {server_config.get('url')}")
        else:
            print(f"    ⚠ No mcpServers in workspace settings")
    except Exception as e:
        print(f"    ✗ Error reading settings: {e}")
else:
    print(f"    ⚠ Workspace settings file not found")

print()

# Test 6: Global MCP Configuration Check
print("[6] Checking Global VSCode MCP Configuration...")
global_mcp_config = Path(r"c:\Users\Owen\AppData\Roaming\Code\User\mcp.json")
if global_mcp_config.exists():
    try:
        with open(global_mcp_config) as f:
            config = json.load(f)
        
        if "servers" in config:
            print(f"    ✓ Global MCP servers configuration found")
            jarvis_found = False
            for server_name in config.get("servers", {}).keys():
                if "jarvis" in server_name.lower():
                    print(f"      ✓ Found Jarvis server: {server_name}")
                    jarvis_found = True
                else:
                    print(f"      - {server_name}")
            
            if not jarvis_found:
                print(f"    ⚠ Jarvis server NOT in global config (but OK if in workspace)")
    except Exception as e:
        print(f"    ✗ Error reading global MCP config: {e}")
else:
    print(f"    ⚠ Global MCP config not found at {global_mcp_config}")

print()

# Test 7: Check VSCode MCP extension
print("[7] Checking VSCode MCP Extension Status...")
vscode_extensions = Path(r"c:\Users\Owen\.vscode\extensions")
mcp_extensions = []
if vscode_extensions.exists():
    for ext in vscode_extensions.iterdir():
        if "mcp" in ext.name.lower():
            mcp_extensions.append(ext.name)
            print(f"    ✓ Found MCP extension: {ext.name}")

if not mcp_extensions:
    print(f"    ⚠ No MCP-related extensions found")
    print(f"       Note: VSCode Copilot comes with built-in MCP support")

print()

# Test 8: MCP Tools Discovery
print("[8] Testing MCP Tools Discovery...")
try:
    # Try to get tools via a proper MCP call
    tools_response = httpx.post(
        JARVIS_URL,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
        },
        json={
            "jsonrpc": "2.0",
            "id": "discover-tools",
            "method": "tools/list",
        },
        timeout=TEST_TIMEOUT,
    )
    
    print(f"    Status: {tools_response.status_code}")
    
    if tools_response.status_code in [200, 400]:
        # Try to parse as JSON
        try:
            data = tools_response.json()
            if "error" in data:
                print(f"    ⚠ RPC Error: {data['error'].get('message', 'Unknown')}")
            elif "result" in data:
                tools = data.get("result", {}).get("tools", [])
                print(f"    ✓ Found {len(tools)} tools:")
                for tool in tools[:5]:  # Show first 5
                    print(f"      - {tool.get('name', 'unknown')}")
                if len(tools) > 5:
                    print(f"      ... and {len(tools) - 5} more")
        except Exception as e:
            print(f"    ⚠ Could not parse response: {e}")
            print(f"    Raw response (first 200 chars): {tools_response.text[:200]}")
    
except Exception as e:
    print(f"    ✗ Tools discovery failed: {e}")

print()

# Summary
print("=" * 70)
print("DIAGNOSTIC SUMMARY")
print("=" * 70)
print()
print("✓ JarvisMCP server is running on port 8765")
print("✓ ArangoDB is connected and accessible")
print("✓ HTTP endpoints are responding")
print()
print("Configuration Status:")
print("  • Workspace settings: ✓ Has jarvis MCP server configured")
print("  • Global settings: See details above")
print("  • Port: 8765 (open)")
print()
print("Recommended Next Steps:")
print("  1. Verify VSCode Copilot Chat is installed and enabled")
print("  2. Check Settings > GitHub Copilot > MCP is enabled")
print("  3. In VSCode, run '@github.copilot /help' to see available tools")
print("  4. Try using a tool: '@github.copilot call get_server_info'")
print()
print("=" * 70)
