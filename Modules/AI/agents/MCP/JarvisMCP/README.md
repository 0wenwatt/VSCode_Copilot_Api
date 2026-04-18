# JarvisMCP — FastMCP Server

A Model Context Protocol (MCP) server built with FastMCP, providing a simple but complete example of:
- ✅ HTTP transport (primary)
- ✅ Stdio transport (fallback)
- ✅ Tool definition and execution
- ✅ Configuration management
- ✅ Logging and debugging
- ✅ Manual HTTP testing
- ✅ VS Code Copilot integration

**Current Demo Tool:** `get_secret_phrase()` returns "Jarvis is watching"

---

## Quick Start

### 1. Install Dependencies

```bash
cd Modules/AI/agents/MCP/JarvisMCP
pip install -r requirements.txt
```

Or with uv:
```bash
uv pip install -r requirements.txt
```

### 2. Start the Server (HTTP Mode)

```bash
python server.py
```

Expected output:
```
[INFO] JarvisMCP: JarvisMCP 0.1.0 Starting
[INFO] JarvisMCP: Using http transport
[INFO] JarvisMCP: Configuration: JarvisConfig(transport=http, host=127.0.0.1, port=8765, debug=false)
```

Server is now running on: **http://127.0.0.1:8765**

### 3. Test the Server (in another terminal)

```bash
python client_test.py
```

Expected output:
```
======================================================================
🤖 JarvisMCP HTTP Client Test Suite
======================================================================
Server URL: http://127.0.0.1:8765/mcp
Configuration: JarvisConfig(transport=http, host=127.0.0.1, port=8765, debug=false)

======================================================================
TEST: Get Secret Phrase
======================================================================

📤 Calling: get_secret_phrase
   URL: http://127.0.0.1:8765
   Arguments: {}
✅ Response received

📝 Response:
{
  ...
}

✅ SUCCESS: Got expected phrase: 'Jarvis is watching'

📊 TEST SUMMARY
======================================================================
✅ PASS: Secret Phrase
✅ PASS: Echo
✅ PASS: Server Info

Total: 3/3 passed
======================================================================
```

---

## Configuration

Configure via environment variables in `.env` file or system environment:

```bash
# Transport type: http | stdio | sse
JARVIS_TRANSPORT=http

# HTTP settings
JARVIS_HTTP_HOST=127.0.0.1
JARVIS_HTTP_PORT=8765

# Enable stdio fallback
JARVIS_STDIO_FALLBACK=true

# Secret phrase returned by get_secret_phrase()
JARVIS_SECRET_PHRASE=Jarvis is watching

# Debug logging
JARVIS_DEBUG=false
```

Create a `.env` file in the JarvisMCP directory:

```bash
cat > .env << EOF
JARVIS_TRANSPORT=http
JARVIS_HTTP_PORT=8765
JARVIS_SECRET_PHRASE=Jarvis is watching
JARVIS_DEBUG=false
EOF
```

---

## Available Tools

### `get_secret_phrase()`
Returns the configured secret phrase.

**Response:**
```
"Jarvis is watching"
```

### `echo(message: str)`
Echo a message with a prefix.

**Arguments:**
- `message` (str): The message to echo

**Response:**
```
"Jarvis echoes: Hello Jarvis!"
```

### `get_server_info()`
Get metadata about the JarvisMCP server.

**Response:**
```json
{
  "name": "JarvisMCP",
  "version": "0.1.0",
  "transport": "http",
  "http_url": "http://127.0.0.1:8765",
  "debug_mode": false
}
```

---

## Transport Modes

### HTTP (Primary) 🌐

Default transport. Server listens for HTTP POST requests with MCP-compliant payloads.

**Usage:**
```bash
JARVIS_TRANSPORT=http python server.py
```

**URL:** `http://127.0.0.1:8765`

**Benefits:**
- ✅ Firewall-friendly
- ✅ Easy to test with curl/client tools
- ✅ Stateless - easy to scale
- ✅ Browser-testable

### Stdio (Fallback) 📡

Alternative transport for direct process-to-process communication.

**Usage:**
```bash
JARVIS_TRANSPORT=stdio python server.py
```

**Benefits:**
- ✅ No port binding needed
- ✅ Direct subprocess communication
- ✅ Useful for VS Code Chat direct integration

---

## VS Code Copilot Integration

### 1. Configure MCP Server in VS Code

Add to `.vscode/settings.json` in the workspace root:

```json
{
  "mcpServers": {
    "jarvis": {
      "type": "http",
      "url": "http://127.0.0.1:8765/mcp"
    }
  }
}
```

Or with all options:

```json
{
  "mcpServers": {
    "jarvis": {
      "type": "http",
      "url": "http://127.0.0.1:8765/mcp",
      "enabled": true,
      "alwaysAllow": [
        "get_secret_phrase",
        "echo",
        "get_server_info"
      ]
    }
  }
}
```

### 2. Start JarvisMCP Server

```bash
python server.py
```

### 3. Test with Copilot Chat

Open Copilot Chat in VS Code and ask:

> "Use the get_secret_phrase tool to get the secret"

Copilot should call the tool and respond with "Jarvis is watching".

---

## Development

### File Structure

```
JarvisMCP/
├── server.py          # Main FastMCP server
├── config.py          # Configuration management
├── client_test.py     # HTTP client for testing
├── requirements.txt   # Python dependencies
├── README.md          # This file
└── .env              # Local configuration (create manually)
```

### Adding New Tools

Edit `server.py` and add a new function with `@mcp.tool()` decorator:

```python
@mcp.tool(description="Your tool description")
def my_new_tool(param1: str, param2: int) -> str:
    """
    Detailed docstring explaining the tool.
    
    Args:
        param1 (str): Description
        param2 (int): Description
    
    Returns:
        str: The result
    """
    logger.info(f"my_new_tool() called with {param1}, {param2}")
    return f"Result: {param1} {param2}"
```

Tools are automatically:
- ✅ Schema-validated
- ✅ Exposed to clients
- ✅ Logged when called
- ✅ Type-checked

### Debugging

Enable debug logging:

```bash
JARVIS_DEBUG=true python server.py
```

Or in `.env`:
```
JARVIS_DEBUG=true
```

---

## Testing

### Manual HTTP Testing

```bash
# Test with curl
curl -X POST http://127.0.0.1:8765/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "get_secret_phrase",
      "arguments": {}
    },
    "id": 1
  }'
```

### Automated Testing

```bash
python client_test.py
```

---

## FastMCP Documentation

- **FastMCP Docs:** https://gofastmcp.com/
- **Servers Guide:** https://gofastmcp.com/servers/server
- **Clients Guide:** https://gofastmcp.com/clients/client
- **Model Context Protocol:** https://modelcontextprotocol.io/

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│ VS Code / Claude Desktop / Other MCP Client                     │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ HTTP
                         │ POST /mcp
                         │ application/json
                         │
                    ┌────▼─────────────────────────────┐
                    │ JarvisMCP (FastMCP Server)       │
                    │ Port: 8765                       │
                    │ Transport: HTTP / Stdio          │
                    │                                  │
                    │ Tools:                           │
                    │ ├─ get_secret_phrase()          │
                    │ ├─ echo()                       │
                    │ └─ get_server_info()            │
                    └──────────────────────────────────┘
```

---

## Roadmap

### v0.1.0 (Current)
- [x] HTTP transport
- [x] Basic tools (secret phrase, echo, info)
- [x] Configuration management
- [x] HTTP client testing
- [x] Documentation

### v0.2.0 (Planned)
- [ ] Stdio transport fully tested
- [ ] Resource definitions
- [ ] Prompt templates
- [ ] Error handling improvements
- [ ] Logging enhancements

### v0.3.0 (Future)
- [ ] ArangoDB integration
- [ ] Multiple tool namespaces
- [ ] Tool result caching
- [ ] Performance optimizations
- [ ] Metrics/monitoring

---

## Troubleshooting

### Port Already in Use

If you get "Address already in use":

```bash
# Find process using port 8765
lsof -i :8765

# Kill the process
kill -9 <PID>

# Or use a different port
JARVIS_HTTP_PORT=8766 python server.py
```

### Connection Refused

If client test fails with "Connection refused":

1. ✅ Is the server running? `python server.py`
2. ✅ Is it on the right port? Check `JARVIS_HTTP_PORT`
3. ✅ Are you using localhost? Should be `127.0.0.1`

### Dependencies Missing

```bash
pip install -r requirements.txt
```

Required packages:
- `fastmcp>=3.0.0` — FastMCP framework
- `httpx>=0.25.0` — HTTP client library
- `python-dotenv>=1.0.0` — .env file support

---

## License

This module is part of the VSCode_Copilot_Api project.

---

## References

- **FastMCP:** https://github.com/PrefectHQ/fastmcp
- **Model Context Protocol:** https://modelcontextprotocol.io/
- **VS Code Copilot:** https://code.visualstudio.com/docs/copilot/overview
