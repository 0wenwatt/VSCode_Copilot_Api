"""
Test ArangoDB MCP Server directly via stdio
"""

import json
import os
import subprocess
import sys
from pathlib import Path

# Start the ArangoDB MCP subprocess
arango_mcp_path = Path(__file__).parent / "arangodb_mcp" / "github" / "mcp-server-arangodb"
arango_env = {
    "ARANGO_URL": "http://localhost:8529",
    "ARANGO_DB": "_system",
    "ARANGO_USERNAME": "root",
    "ARANGO_PASSWORD": "jarvis",
}

print("=" * 60)
print("Testing ArangoDB MCP - Stdio Protocol")
print("=" * 60)

try:
    print(f"\n[1] Starting ArangoDB MCP subprocess...")
    process = subprocess.Popen(
        ["node", str(arango_mcp_path / "build" / "index.js")],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env={**os.environ, **arango_env},
    )
    print(f"    ✓ Subprocess started (PID: {process.pid})")

    # Test 1: Initialize
    print(f"\n[2] Initialize...")
    request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "test", "version": "1.0"}
        }
    }
    process.stdin.write(json.dumps(request) + "\n")
    process.stdin.flush()
    
    response_line = process.stdout.readline()
    if not response_line:
        print(f"    ❌ No response from server (got empty line)")
        # Try reading stderr
        stderr_line = process.stderr.readline()
        if stderr_line:
            print(f"    STDERR: {stderr_line}")
        raise RuntimeError("ArangoDB MCP not responding")
        
    response = json.loads(response_line)
    print(f"    Status: OK")
    print(f"    Server: {response.get('result', {}).get('serverInfo', {}).get('name')}")

    # Test 2: List tools
    print(f"\n[3] List tools...")
    request = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/list",
    }
    process.stdin.write(json.dumps(request) + "\n")
    process.stdin.flush()
    
    response_line = process.stdout.readline()
    response = json.loads(response_line)
    tools = response.get("result", {}).get("tools", [])
    print(f"    Available tools: {len(tools)}")
    for tool in tools:
        print(f"      - {tool['name']}: {tool.get('description', 'N/A')}")

    # Test 3: List collections
    print(f"\n[4] Call arango_list_collections...")
    request = {
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {
            "name": "arango_list_collections",
            "arguments": {}
        }
    }
    process.stdin.write(json.dumps(request) + "\n")
    process.stdin.flush()
    
    response_line = process.stdout.readline()
    response = json.loads(response_line)
    
    if "result" in response:
        collections = response["result"]
        print(f"    ✅ Collections retrieved: {len(collections)}")
        for col in collections[:5]:  # Show first 5
            col_type = "Edge" if "type" in col and col["type"] == 3 else "Document"
            print(f"      - {col['name']} ({col_type})")
        if len(collections) > 5:
            print(f"      ... and {len(collections) - 5} more")
    elif "error" in response:
        print(f"    ❌ Error: {response['error']['message']}")
    else:
        print(f"    Response: {json.dumps(response, indent=2)}")

    # Cleanup
    process.terminate()
    process.wait(timeout=5)
    
    print("\n" + "=" * 60)
    print("✅ ArangoDB MCP is working correctly!")
    print("=" * 60)

except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
