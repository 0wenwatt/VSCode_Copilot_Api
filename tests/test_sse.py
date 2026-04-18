import httpx
import json

resp = httpx.post(
    'http://127.0.0.1:8765/mcp',
    headers={'Content-Type': 'application/json', 'Accept': 'application/json, text/event-stream'},
    json={'jsonrpc': '2.0', 'id': 2, 'method': 'tools/call', 'params': {'name': 'get_server_info', 'arguments': {}}},
    timeout=10
)

print(f'Status: {resp.status_code}')
print(f'Content-Type: {resp.headers.get("content-type")}')
print(f'Response text (first 1000 chars):')
print(resp.text[:1000])
print()
print('Lines:')
for i, line in enumerate(resp.text.split('\n')[:20]):
    print(f'{i}: {repr(line)}')
