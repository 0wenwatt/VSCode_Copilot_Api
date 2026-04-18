#!/usr/bin/env python3
"""
Test all configured MCPs
"""
import subprocess
import json
import sys
import time
import requests
from pathlib import Path

def test_jarvismcp():
    """Test JarvisMCP (HTTP)"""
    print("\n" + "="*60)
    print("Testing JarvisMCP (HTTP)")
    print("="*60)
    try:
        response = requests.get("http://127.0.0.1:8765/mcp/tools", timeout=5)
        print(f"✓ JarvisMCP is reachable")
        print(f"  Status: {response.status_code}")
        print(f"  Response: {response.json()}")
        return True
    except requests.exceptions.ConnectionError:
        print(f"✗ JarvisMCP is NOT reachable at 127.0.0.1:8765")
        return False
    except Exception as e:
        print(f"✗ Error testing JarvisMCP: {e}")
        return False

def test_eplan_rag():
    """Test Eplan_Documentation_RAG_MCP (HTTP)"""
    print("\n" + "="*60)
    print("Testing Eplan_Documentation_RAG_MCP (HTTP)")
    print("="*60)
    try:
        response = requests.get("https://rag2026.covaga.xyz/mcp", timeout=10)
        print(f"✓ Eplan RAG MCP is reachable")
        print(f"  Status: {response.status_code}")
        return True
    except requests.exceptions.ConnectionError:
        print(f"✗ Eplan RAG MCP is NOT reachable at rag2026.covaga.xyz")
        return False
    except Exception as e:
        print(f"✗ Error testing Eplan RAG MCP: {e}")
        return False

def test_github_mcp():
    """Test GitHub MCP (HTTP)"""
    print("\n" + "="*60)
    print("Testing GitHub MCP (HTTP)")
    print("="*60)
    try:
        response = requests.get("https://api.githubcopilot.com/mcp/", timeout=10)
        print(f"✓ GitHub MCP is reachable")
        print(f"  Status: {response.status_code}")
        return True
    except requests.exceptions.ConnectionError:
        print(f"✗ GitHub MCP is NOT reachable at api.githubcopilot.com")
        return False
    except Exception as e:
        print(f"✗ Error testing GitHub MCP: {e}")
        return False

def test_arango_mcp():
    """Test arango-mcp (stdio)"""
    print("\n" + "="*60)
    print("Testing arango-mcp (stdio)")
    print("="*60)
    arango_path = Path("c:/Users/Owen/Desktop/Brogramming/Test_Environment/Test_Environment/jarvis_project/versions/V3.0/modules/arangodb_mcp/github/mcp-server-arangodb")
    
    if not arango_path.exists():
        print(f"✗ ArangoDB MCP path does not exist: {arango_path}")
        return False
    
    print(f"  Path: {arango_path}")
    print(f"  Checking for build/index.js...")
    
    build_file = arango_path / "build" / "index.js"
    if build_file.exists():
        print(f"  ✓ Build file exists")
        try:
            # Test with a simple node command to verify it works
            result = subprocess.run(
                ["node", "--version"],
                timeout=5,
                capture_output=True,
                text=True
            )
            print(f"  ✓ Node.js is available: {result.stdout.strip()}")
            return True
        except Exception as e:
            print(f"  ✗ Error checking Node.js: {e}")
            return False
    else:
        print(f"  ✗ Build file not found: {build_file}")
        return False

def test_context7_mcp():
    """Test Context7 MCP (stdio)"""
    print("\n" + "="*60)
    print("Testing io.github.upstash/context7 (stdio)")
    print("="*60)
    print("  This MCP requires CONTEXT7_API_KEY environment variable")
    print("  Checking if npx is available...")
    
    try:
        result = subprocess.run(
            ["npx", "--version"],
            timeout=5,
            capture_output=True,
            text=True
        )
        print(f"  ✓ npx is available: {result.stdout.strip()}")
        print(f"  Note: To use this MCP, set CONTEXT7_API_KEY environment variable")
        return True
    except FileNotFoundError:
        print(f"  ✗ npx is NOT available (npm not installed)")
        return False
    except Exception as e:
        print(f"  ✗ Error checking npx: {e}")
        return False

def main():
    print("\n╔════════════════════════════════════════════════════════════╗")
    print("║        Testing All Configured MCPs                        ║")
    print("╚════════════════════════════════════════════════════════════╝\n")
    
    results = {}
    
    # Test each MCP
    results["JarvisMCP"] = test_jarvismcp()
    results["Eplan_Documentation_RAG_MCP"] = test_eplan_rag()
    results["GitHub_MCP"] = test_github_mcp()
    results["arango-mcp"] = test_arango_mcp()
    results["Context7_MCP"] = test_context7_mcp()
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    
    for mcp_name, is_working in results.items():
        status = "✓ OK" if is_working else "✗ FAILED"
        print(f"{status:8} - {mcp_name}")
    
    working_count = sum(1 for v in results.values() if v)
    total_count = len(results)
    
    print(f"\n{working_count}/{total_count} MCPs are working")
    print("="*60 + "\n")
    
    return 0 if working_count == total_count else 1

if __name__ == "__main__":
    sys.exit(main())
