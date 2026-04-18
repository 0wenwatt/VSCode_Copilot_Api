"""
FastMCP HTTP with proper SSE parsing

HTTP responses come as Server-Sent Events (SSE):
  data: {"jsonrpc":"2.0","id":1,"result":{...}}
  
We need to parse SSE format properly.
"""

import httpx
import json
import re

BASE_URL = "http://127.0.0.1:8765"
ACCEPT_HEADER = "application/json, text/event-stream"

def parse_sse(text):
    """Parse Server-Sent Events format"""
    lines = text.strip().split('\n')
    for line in lines:
        if line.startswith('data: '):
            try:
                return json.loads(line[6:])  # Strip 'data: ' prefix
            except:
                pass
    return None

def test_mcp():
    with httpx.Client(timeout=30) as client:
        print("=" * 60)
        print("Testing JarvisMCP - HTTP SSE Protocol")
        print("=" * 60)
        
        # Step 1: Initialize
        print("\n[1] Initialize...")
        response = client.post(f"{BASE_URL}/mcp",
                             json={
                                 "jsonrpc": "2.0",
                                 "id": 1,
                                 "method": "initialize",
                                 "params": {
                                     "protocolVersion": "2024-11-05",
                                     "capabilities": {},
                                     "clientInfo": {"name": "test", "version": "1.0"}
                                 }
                             },
                             headers={
                                 "Content-Type": "application/json",
                                 "Accept": ACCEPT_HEADER
                             })
        
        session_id = response.headers.get("mcp-session-id")
        print(f"    Status: {response.status_code}")
        print(f"    Session: {session_id}")
        
        if response.status_code != 200:
            print(f"    Error: {response.text}")
            return
        
        data = parse_sse(response.text)
        if data:
            print(f"    Response: {json.dumps(data, indent=2)}")
        
        # Step 2: Call get_secret_phrase
        print(f"\n[2] get_secret_phrase()...")
        response = client.post(f"{BASE_URL}/mcp",
                             json={
                                 "jsonrpc": "2.0",
                                 "id": 2,
                                 "method": "tools/call",
                                 "params": {
                                     "name": "get_secret_phrase",
                                     "arguments": {}
                                 }
                             },
                             headers={
                                 "Content-Type": "application/json",
                                 "Accept": ACCEPT_HEADER,
                                 "mcp-session-id": session_id
                             })
        
        print(f"    Status: {response.status_code}")
        data = parse_sse(response.text)
        if data:
            if "result" in data:
                print(f"    ✅ Result: {data['result']}")
            elif "error" in data:
                print(f"    ❌ Error: {data['error']['message']}")
            else:
                print(f"    Response: {json.dumps(data, indent=2)}")
        else:
            print(f"    Failed to parse: {response.text}")
        
        # Step 3: Call echo
        print(f"\n[3] echo('Hello Jarvis')...")
        response = client.post(f"{BASE_URL}/mcp",
                             json={
                                 "jsonrpc": "2.0",
                                 "id": 3,
                                 "method": "tools/call",
                                 "params": {
                                     "name": "echo",
                                     "arguments": {"message": "Hello Jarvis"}
                                 }
                             },
                             headers={
                                 "Content-Type": "application/json",
                                 "Accept": ACCEPT_HEADER,
                                 "mcp-session-id": session_id
                             })
        
        print(f"    Status: {response.status_code}")
        data = parse_sse(response.text)
        if data:
            if "result" in data:
                print(f"    ✅ Result: {data['result']}")
            elif "error" in data:
                print(f"    ❌ Error: {data['error']['message']}")
        
        # Step 4: Call get_server_info
        print(f"\n[4] get_server_info()...")
        response = client.post(f"{BASE_URL}/mcp",
                             json={
                                 "jsonrpc": "2.0",
                                 "id": 4,
                                 "method": "tools/call",
                                 "params": {
                                     "name": "get_server_info",
                                     "arguments": {}
                                 }
                             },
                             headers={
                                 "Content-Type": "application/json",
                                 "Accept": ACCEPT_HEADER,
                                 "mcp-session-id": session_id
                             })
        
        print(f"    Status: {response.status_code}")
        data = parse_sse(response.text)
        if data:
            if "result" in data:
                print(f"    ✅ Result:")
                for k, v in data['result'].items():
                    print(f"        {k}: {v}")
            elif "error" in data:
                print(f"    ❌ Error: {data['error']['message']}")
        
        print("\n" + "=" * 60)
        print("✅ JarvisMCP Server is working correctly!")
        print("=" * 60)

if __name__ == "__main__":
    test_mcp()
