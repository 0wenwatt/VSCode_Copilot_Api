"""
MCP Gateway Integration Test

Verifies that:
1. ArangoDB is running and accessible
2. JarvisMCP is running and responding
3. ArangoDB MCP subprocess is active
4. ArangoDB MCP can connect to the database with real credentials
5. Tools are discoverable through JarvisMCP HTTP gateway

Usage:
    python test_mcp_integration.py              # Run all tests
    python test_mcp_integration.py --quick      # Quick connectivity test only
    python test_mcp_integration.py --verbose    # Detailed output
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

try:
    import httpx
except ImportError:
    print("ERROR: httpx package not installed")
    print("Install it with: pip install httpx")
    sys.exit(1)

WORKSPACE_ROOT = Path(__file__).resolve().parents[2]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Test MCP gateway integration")
    parser.add_argument("--quick", action="store_true", help="Quick connectivity test only")
    parser.add_argument("--verbose", action="store_true", help="Detailed output")
    parser.add_argument("--retries", type=int, default=10, help="Max connection retries")
    parser.add_argument("--delay", type=float, default=1.0, help="Delay between retries (seconds)")
    return parser.parse_args()


def test_arangodb_http(url: str = "http://127.0.0.1:8893", retries: int = 10, delay: float = 1.0, verbose: bool = False) -> bool:
    """Test direct HTTP connection to ArangoDB."""
    print("\n[1] Testing ArangoDB HTTP connectivity...")
    
    for attempt in range(1, retries + 1):
        try:
            response = httpx.get(
                f"{url}/_api/version",
                auth=("root", "test123"),
                timeout=5
            )
            if response.status_code == 200:
                version_info = response.json()
                print(f"  [OK] ArangoDB responding (version {version_info.get('version', 'unknown')})")
                if verbose:
                    print(f"    Response: {json.dumps(version_info, indent=2)}")
                return True
        except Exception as e:
            if verbose:
                print(f"    Attempt {attempt}/{retries}: {e}")
            if attempt < retries:
                time.sleep(delay)
    
    print(f"  [FAILED] ArangoDB not responding after {retries} attempts")
    return False


def test_jarvismcp_http(url: str = "http://127.0.0.1:8765/mcp", retries: int = 10, delay: float = 1.0, verbose: bool = False) -> tuple[bool, str]:
    """Test JarvisMCP HTTP endpoint and get session ID."""
    print("\n[2] Testing JarvisMCP HTTP connectivity...")
    
    # Initial delay to let the server fully start
    print(f"  Waiting for JarvisMCP to be ready...")
    time.sleep(2)
    
    session_id = None
    for attempt in range(1, retries + 1):
        try:
            # Send initialize request with proper SSE headers
            response = httpx.post(
                url,
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json, text/event-stream",
                },
                json={
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "initialize",
                    "params": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {},
                        "clientInfo": {"name": "test-client", "version": "1.0.0"},
                    },
                },
                timeout=5,
            )
            
            if response.status_code == 200:
                # Extract session ID from headers
                session_id = response.headers.get("mcp-session-id")
                
                # FastMCP returns Server-Sent Events format
                # Parse SSE response: "event: message\ndata: {...}\n\n"
                text = response.text
                if "data: " in text:
                    # Extract JSON from SSE data field
                    data_line = [line for line in text.split("\n") if line.startswith("data: ")]
                    if data_line:
                        json_str = data_line[0].replace("data: ", "")
                        try:
                            data = json.loads(json_str)
                            server_name = data.get("result", {}).get("serverInfo", {}).get("name", "unknown")
                            print(f"  [OK] JarvisMCP responding (server: {server_name})")
                            print(f"    Session ID: {session_id}")
                            if verbose:
                                print(f"    Response: {json.dumps(data.get('result', {}).get('serverInfo'), indent=2)}")
                            return True, session_id
                        except json.JSONDecodeError:
                            pass
        except Exception as e:
            if verbose:
                print(f"    Attempt {attempt}/{retries}: {e}")
            if attempt < retries:
                time.sleep(delay)
    
    print(f"  [FAILED] JarvisMCP not responding after {retries} attempts")
    return False, None


def test_jarvismcp_tools(url: str = "http://127.0.0.1:8765/mcp", session_id: str | None = None, verbose: bool = False) -> dict:
    """Test JarvisMCP tools and get server info."""
    print("\n[3] Testing JarvisMCP tools...")
    
    if not session_id:
        print(f"  [FAILED] No session ID provided")
        return {"success": False, "registered_remote_mcps": []}
    
    try:
        # Get server info to see registered MCPs
        response = httpx.post(
            url,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream",
                "mcp-session-id": session_id,
            },
            json={
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/call",
                "params": {
                    "name": "get_server_info",
                    "arguments": {},
                },
            },
            timeout=5,
        )
        
        if response.status_code == 200:
            # Parse SSE response format
            text = response.text
            if "data: " in text:
                data_line = [line for line in text.split("\n") if line.startswith("data: ")]
                if data_line:
                    json_str = data_line[0].replace("data: ", "")
                    try:
                        result = json.loads(json_str)
                        content = result.get("result", {}).get("structuredContent", {})
                        
                        if isinstance(content, dict):
                            remote_mcps = content.get("registered_remote_mcps", [])
                            print(f"  [OK] get_server_info() working")
                            print(f"    Registered remote MCPs: {remote_mcps}")
                            
                            if verbose:
                                print(f"    Full info: {json.dumps(content, indent=2)}")
                            
                            return {
                                "success": True,
                                "registered_remote_mcps": remote_mcps,
                                "data": content,
                            }
                    except json.JSONDecodeError:
                        pass
        else:
            if verbose:
                print(f"    HTTP {response.status_code}: {response.text[:200]}")
        
        print(f"  [FAILED] get_server_info() failed")
        return {"success": False, "registered_remote_mcps": []}
        
    except Exception as e:
        print(f"  [FAILED] get_server_info() error: {e}")
        return {"success": False, "registered_remote_mcps": []}


def test_arangodb_mcp(url: str = "http://127.0.0.1:8765/mcp", session_id: str | None = None, verbose: bool = False) -> bool:
    """Test ArangoDB MCP tool access through JarvisMCP gateway."""
    print("\n[4] Testing ArangoDB MCP through JarvisMCP gateway...")
    
    if not session_id:
        print(f"  [FAILED] No session ID provided")
        return False
    
    try:
        # Try to call an ArangoDB MCP tool
        response = httpx.post(
            url,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream",
                "mcp-session-id": session_id,
            },
            json={
                "jsonrpc": "2.0",
                "id": 3,
                "method": "tools/call",
                "params": {
                    "name": "arango_list_collections",
                    "arguments": {},
                },
            },
            timeout=10,
        )
        
        if response.status_code == 200:
            # Parse SSE response format
            text = response.text
            if "data: " in text:
                data_line = [line for line in text.split("\n") if line.startswith("data: ")]
                if data_line:
                    json_str = data_line[0].replace("data: ", "")
                    try:
                        result = json.loads(json_str)
                        
                        # Check if there's an error
                        if "error" in result:
                            error_msg = result.get("error", {}).get("message", "unknown error")
                            print(f"  [WARNING] ArangoDB MCP responded with error: {error_msg}")
                            if verbose:
                                print(f"    Full response: {json.dumps(result, indent=2)}")
                            return False
                        
                        # Success
                        content = result.get("result", {}).get("content", [])
                        if content:
                            text_result = content[0].get("text", "") if isinstance(content, list) and len(content) > 0 else ""
                            print(f"  [OK] arango_list_collections() working")
                            if verbose:
                                print(f"    Response: {text_result[:200]}...")
                            return True
                    except json.JSONDecodeError:
                        pass
        
        print(f"  [FAILED] arango_list_collections() failed (HTTP {response.status_code})")
        if verbose:
            print(f"    Response: {response.text[:500]}")
        return False
        
    except Exception as e:
        print(f"  [FAILED] arango_list_collections() error: {e}")
        return False


def main() -> int:
    args = parse_args()
    
    print("="*60)
    print("MCP Gateway Integration Test")
    print("="*60)
    
    # Test 1: ArangoDB HTTP
    if not test_arangodb_http(retries=args.retries, delay=args.delay, verbose=args.verbose):
        print("\n[FAILED] ArangoDB is not running. Start it with: python startup.py")
        return 1
    
    # Test 2: JarvisMCP HTTP
    success, session_id = test_jarvismcp_http(retries=args.retries, delay=args.delay, verbose=args.verbose)
    if not success:
        print("\n[FAILED] JarvisMCP is not running. Start it with: python startup.py")
        return 1
    
    if args.quick:
        print("\n" + "="*60)
        print("[OK] Quick test passed: services are running")
        print("="*60)
        return 0
    
    # Test 3: JarvisMCP tools
    server_info = test_jarvismcp_tools(session_id=session_id, verbose=args.verbose)
    
    if not server_info["success"]:
        print("\n[FAILED] JarvisMCP tools test failed")
        return 1
    
    if "arangodb" not in server_info.get("registered_remote_mcps", []):
        print("\n[FAILED] ArangoDB MCP not registered in JarvisMCP")
        print("   Make sure JarvisMCP was started with ArangoDB MCP enabled")
        return 1
    
    # Test 4: ArangoDB MCP through gateway
    if test_arangodb_mcp(session_id=session_id, verbose=args.verbose):
        print("\n" + "="*60)
        print("[OK] Full integration test passed!")
        print("[OK] ArangoDB MCP is connected with real credentials")
        print("="*60)
        return 0
    else:
        print("\n" + "="*60)
        print("[WARNING] ArangoDB MCP tool call failed")
        print("   (This may be due to database connection issues)")
        print("   But JarvisMCP gateway is working correctly")
        print("="*60)
        return 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        raise SystemExit(130)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        raise SystemExit(1)
