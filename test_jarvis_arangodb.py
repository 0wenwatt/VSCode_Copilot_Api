#!/usr/bin/env python3
"""Test ArangoDB database connectivity and operations"""

import json
import time
import base64
import sys

def test_arangodb():
    print("=" * 70)
    print("Testing ArangoDB Direct Access")
    print("=" * 70)
    
    import socket
    
    # Check if ArangoDB is running
    print("\n[1] Checking if ArangoDB is running on localhost:8893...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', 8893))
    sock.close()
    
    if result != 0:
        print("[ERROR] ArangoDB not running on 127.0.0.1:8893")
        print("Please start ArangoDB first!")
        return False
    
    print("[OK] ArangoDB port 8893 is open")
    
    # Create auth header
    auth_string = base64.b64encode(b'root:test123').decode('utf-8')
    headers = {
        'Authorization': f'Basic {auth_string}',
        'Content-Type': 'application/json'
    }
    
    try:
        import urllib.request
        
        # Test 1: Get version
        print("\n[2] Getting ArangoDB version...")
        req = urllib.request.Request(
            'http://127.0.0.1:8893/_api/version',
            method='GET',
            headers=headers
        )
        response = urllib.request.urlopen(req, timeout=2)
        version_data = json.loads(response.read().decode('utf-8'))
        print(f"[OK] ArangoDB {version_data.get('version', 'unknown')}")
        
        # Test 2: Create collection
        print("\n[3] Creating test collection 'jarvis_test'...")
        req = urllib.request.Request(
            'http://127.0.0.1:8893/_api/collection',
            data=json.dumps({"name": "jarvis_test"}).encode('utf-8'),
            method='POST',
            headers=headers
        )
        try:
            response = urllib.request.urlopen(req, timeout=2)
            result = json.loads(response.read().decode('utf-8'))
            print(f"[OK] Collection created/exists: {result.get('name')}")
        except urllib.error.HTTPError as e:
            if e.code == 409:
                print(f"[OK] Collection already exists")
            else:
                raise
        
        # Test 3: Insert document
        print("\n[4] Inserting test document...")
        test_doc = {
            "test_name": "JarvisMCP Integration Test",
            "timestamp": time.time(),
            "status": "Active",
            "source": "test_jarvis_arangodb.py"
        }
        
        req = urllib.request.Request(
            'http://127.0.0.1:8893/_api/document/jarvis_test',
            data=json.dumps(test_doc).encode('utf-8'),
            method='POST',
            headers=headers
        )
        response = urllib.request.urlopen(req, timeout=2)
        insert_result = json.loads(response.read().decode('utf-8'))
        doc_id = insert_result.get('_id')
        print(f"[OK] Document inserted with ID: {doc_id}")
        
        # Test 4: Retrieve document to verify
        print("\n[5] Retrieving document to verify it was saved...")
        req = urllib.request.Request(
            f'http://127.0.0.1:8893/_api/document/{doc_id}',
            method='GET',
            headers=headers
        )
        response = urllib.request.urlopen(req, timeout=2)
        retrieved = json.loads(response.read().decode('utf-8'))
        
        print(f"[OK] Document retrieved successfully:")
        print(f"     - ID: {retrieved.get('_id')}")
        print(f"     - Name: {retrieved.get('test_name')}")
        print(f"     - Status: {retrieved.get('status')}")
        print(f"     - Source: {retrieved.get('source')}")
        
        # Test 5: List all documents
        print("\n[6] Listing all documents in collection...")
        query_payload = {
            "query": "FOR doc IN jarvis_test RETURN doc"
        }
        req = urllib.request.Request(
            'http://127.0.0.1:8893/_api/cursor',
            data=json.dumps(query_payload).encode('utf-8'),
            method='POST',
            headers=headers
        )
        response = urllib.request.urlopen(req, timeout=2)
        query_result = json.loads(response.read().decode('utf-8'))
        docs = query_result.get('result', [])
        print(f"[OK] Found {len(docs)} document(s) in collection")
        for doc in docs[-3:]:  # Show last 3
            print(f"     - {doc.get('_id')}: {doc.get('test_name')}")
        
        print("\n" + "=" * 70)
        print("SUCCESS: ArangoDB is working and database changes persisted!")
        print("=" * 70)
        return True
        
    except urllib.error.HTTPError as e:
        print(f"\n[ERROR] HTTP {e.code}: {e.reason}")
        try:
            error_body = e.read().decode('utf-8')
            print(f"Details: {error_body[:200]}")
        except:
            pass
        return False
    except Exception as e:
        print(f"\n[ERROR] {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_arangodb()
    sys.exit(0 if success else 1)
