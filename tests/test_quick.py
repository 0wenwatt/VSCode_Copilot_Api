import httpx

try:
    resp = httpx.post(
        'http://127.0.0.1:8765/mcp',
        headers={'Content-Type': 'application/json', 'Accept': 'application/json, text/event-stream'},
        json={'jsonrpc': '2.0', 'id': 1, 'method': 'initialize', 'params': {'protocolVersion': '2024-11-05', 'capabilities': {}, 'clientInfo': {'name': 'test', 'version': '1.0'}}},
        timeout=10
    )
    print(f'Status: {resp.status_code}')
    print(f'Content-Type: {resp.headers.get("content-type")}')
    print(f'Response text (first 500 chars): {resp.text[:500]}')
    try:
        data = resp.json()
        print(f'Server: {data.get("result", {}).get("serverInfo", {}).get("name")}')
        print('✓ SUCCESS')
    except:
        print('(Response is not JSON)')
except Exception as e:
    print(f'Error: {e}')
