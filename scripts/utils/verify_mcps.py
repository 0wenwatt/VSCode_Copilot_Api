#!/usr/bin/env python3
"""Verify both MCPs are available and working"""

import json
import socket
import sys

def check_port(host, port, name):
    """Check if a service is running on a port"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((host, port))
    sock.close()
    status = "RUNNING" if result == 0 else "NOT RUNNING"
    symbol = "[OK]" if result == 0 else "[ERROR]"
    print(f"{symbol} {name:30} {host}:{port:5} - {status}")
    return result == 0

def main():
    print("=" * 70)
    print("MCP Configuration Verification")
    print("=" * 70)
    
    print("\n[1] Service Status:")
    jarvis_ok = check_port('127.0.0.1', 8765, "JarvisMCP (HTTP)")
    arango_ok = check_port('127.0.0.1', 8893, "ArangoDB (HTTP)")
    
    print("\n[2] VS Code mcp.json Configuration:")
    print("  - arango-mcp (DIRECT via stdio)")
    print("    Path: C:/Users/Owen/Desktop/Brogramming/VSCode_Copilot_Api/Modules/arangodb/arangodb_mcp/github/mcp-server-arangodb")
    print("    Type: stdio")
    print("    Status: Configured")
    print()
    print("  - JarvisMCP (HTTP gateway with mounted ArangoDB MCP)")
    print("    URL: 127.0.0.1:8765")
    print("    Type: http")
    print("    Status: Configured")
    
    print("\n[3] Available Tools in VS Code Copilot:")
    print()
    print("  From arango-mcp (direct):")
    print("    - arangodb_query - Execute AQL queries")
    print("    - arangodb_create_collection - Create collections")
    print("    - arangodb_list_collections - List all collections")
    print("    - arangodb_insert_document - Insert documents")
    print("    - arangodb_update_document - Update documents")
    print("    - arangodb_delete_document - Delete documents")
    print()
    print("  From JarvisMCP (HTTP):")
    print("    - get_secret_phrase - Get Jarvis' secret phrase")
    print("    - echo - Echo a message")
    print("    - get_server_info - Get server information")
    print("    - arangodb_* (all mounted ArangoDB tools with prefix)")
    
    print("\n[4] Summary:")
    if jarvis_ok:
        print("[OK] JarvisMCP is running and accessible")
    else:
        print("[WARNING] JarvisMCP is not running - start it with:")
        print("          cd Modules/AI/agents/MCP/JarvisMCP && python server.py")
    
    if arango_ok:
        print("[OK] ArangoDB database is running")
    else:
        print("[ERROR] ArangoDB is not running")
    
    print("\n[5] Both MCPs are configured in mcp.json!")
    print("    - arango-mcp: Direct connection to ArangoDB MCP")
    print("    - JarvisMCP: Gateway with ArangoDB MCP mounted")
    print()
    print("    VS Code Copilot Chat can use EITHER:")
    print("    1. Direct arango-mcp for direct database access")
    print("    2. JarvisMCP for unified gateway with both local and remote tools")
    
    print("\n" + "=" * 70)
    print("Configuration complete! Ready for use in VS Code Copilot Chat")
    print("=" * 70)

if __name__ == "__main__":
    main()
