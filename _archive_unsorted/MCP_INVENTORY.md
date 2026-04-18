# MCP Inventory & Startup Guide

**Generated:** April 19, 2026  
**Workspace:** VSCode_Copilot_Api  
**Status:** Cataloging All MCPs

## 🎯 MCP Summary

| # | Name | Type | Location | Language | Port | Status |
|---|------|------|----------|----------|------|--------|
| 1 | **JarvisMCP** | HTTP Gateway | `Modules/AI/agents/MCP/JarvisMCP` | Python | 8765 | Running ✅ |
| 2 | **ArangoDB MCP** | Stdio Subprocess | `Modules/arangodb/arangodb_mcp/github/mcp-server-arangodb` | Node.js | 8893* | Mounted to JarvisMCP ✅ |
| 3 | **Time MCP** | Stdio/SSE | `Modules/AI/agents/MCP/github/servers/src/time` | Python | - | Available |
| 4 | **Git MCP** | Stdio/SSE | `Modules/AI/agents/MCP/github/servers/src/git` | Python | - | Available |
| 5 | **Fetch MCP** | Stdio/SSE | `Modules/AI/agents/MCP/github/servers/src/fetch` | Python | - | Available |
| 6 | **Everything MCP** | Stdio/SSE/HTTP | `Modules/AI/agents/MCP/github/servers/src/everything` | TypeScript | 3001 | Available |

*ArangoDB database port (not MCP port - runs as subprocess)

---

## 📋 Detailed MCP Information

### 1. JarvisMCP (PRIMARY GATEWAY)

**Purpose:** FastMCP-based HTTP gateway that orchestrates all other MCPs

**Location:** `Modules/AI/agents/MCP/JarvisMCP`

**Details:**
- **Language:** Python (FastMCP 3.2.4)
- **Transport:** HTTP + SSE
- **URL:** `http://127.0.0.1:8765/mcp`
- **Config:** `.env` file support
- **Status:** Fully operational ✅

**Local Tools:**
- `get_secret_phrase()` - Returns "Jarvis is watching"
- `echo(message)` - Echo utility
- `get_server_info()` - Server metadata

**Mounted Remote MCPs:**
- ArangoDB MCP (via stdio subprocess)

**Start Command:**
```bash
cd Modules/AI/agents/MCP/JarvisMCP
python server.py
```

**Test Command:**
```bash
python test_mcp.py
```

**Files:**
- `server.py` - Main FastMCP server (supports remote MCP mounting)
- `config.py` - Configuration management
- `test_mcp.py` - HTTP client tests
- `requirements.txt` - Python dependencies

---

### 2. ArangoDB MCP (REMOTE - MOUNTED TO JARVISMCP)

**Purpose:** Database operations MCP for ArangoDB integration

**Location:** `Modules/arangodb/arangodb_mcp/github/mcp-server-arangodb`

**Details:**
- **Language:** Node.js (JavaScript/TypeScript)
- **Build Status:** Built (`build/index.js` exists)
- **Transport:** Stdio (runs as subprocess)
- **Database:** ArangoDB 3.12.9 on `http://127.0.0.1:8893`
- **Auth:** root / test123
- **Status:** Mounted to JarvisMCP ✅

**Tools Available:**
- `arangodb_query` - Execute AQL queries
- `arangodb_insert` - Insert documents
- `arangodb_update` - Update documents  
- `arangodb_remove` - Delete documents
- `arangodb_backup` - Backup collections
- `arangodb_list_collections` - List collections
- `arangodb_create_collection` - Create collections

**Environment Variables:**
```bash
ARANGO_URL=http://localhost:8893
ARANGO_DB=_system
ARANGO_USERNAME=root
ARANGO_PASSWORD=test123
```

**Start Separately (if needed):**
```bash
cd Modules/arangodb/arangodb_mcp/github/mcp-server-arangodb
npm install
node build/index.js
```

**Files:**
- `build/index.js` - Compiled MCP server
- `.env` - Environment configuration
- `package.json` - Dependencies

---

### 3. Time MCP

**Purpose:** Time and timezone conversion utilities

**Location:** `Modules/AI/agents/MCP/github/servers/src/time`

**Details:**
- **Language:** Python (MCP SDK)
- **Transport:** Stdio / SSE
- **Status:** Ready to integrate

**Tools:**
- `get_current_time` - Get time in specific timezone
- `convert_time` - Convert between timezones

**Example Tools Available:**
- Europe/London, America/New_York, Asia/Tokyo timezones
- DST handling
- Fractional hour support (e.g., Nepal UTC+5:45)

**Start Command:**
```bash
cd Modules/AI/agents/MCP/github/servers/src/time
python -m mcp_server_time
```

**Files:**
- `src/mcp_server_time/server.py` - Main server
- `tests/time_server_test.py` - Test suite
- `requirements.txt` - Dependencies

---

### 4. Git MCP

**Purpose:** Git repository operations and querying

**Location:** `Modules/AI/agents/MCP/github/servers/src/git`

**Details:**
- **Language:** Python (MCP SDK)
- **Transport:** Stdio / SSE  
- **Status:** Ready to integrate

**Tools:**
- `git_status` - Repository status
- `git_diff_unstaged` - Unstaged changes
- `git_diff_staged` - Staged changes
- `git_diff` - Compare branches/commits
- `git_commit` - Create commits
- `git_add` - Stage files
- `git_reset` - Unstage files
- `git_log` - Commit history
- `git_create_branch` - Create branches
- `git_checkout` - Switch branches
- `git_show` - Show commits
- `git_branch` - List branches

**Start Command:**
```bash
cd Modules/AI/agents/MCP/github/servers/src/git
python -m mcp_server_git <repo_path>
```

**Files:**
- `src/mcp_server_git/server.py` - Main server
- `tests/test_server.py` - Comprehensive tests
- `requirements.txt` - Dependencies

---

### 5. Fetch MCP

**Purpose:** Web content fetching and HTML-to-Markdown conversion

**Location:** `Modules/AI/agents/MCP/github/servers/src/fetch`

**Details:**
- **Language:** Python (MCP SDK)
- **Transport:** Stdio / SSE
- **Status:** Ready to integrate

**Tools:**
- `fetch` - Fetch URLs and convert HTML to Markdown
- Supports robots.txt compliance
- HTML simplification
- Raw HTML option
- Truncation support

**Constraints:**
- respects robots.txt
- Max fetch time: 30s
- Content size limits

**Start Command:**
```bash
cd Modules/AI/agents/MCP/github/servers/src/fetch
python -m mcp_server_fetch
```

**Files:**
- `src/mcp_server_fetch/server.py` - Main server
- `tests/test_server.py` - Test suite
- `requirements.txt` - Dependencies

---

### 6. Everything MCP (REFERENCE SERVER)

**Purpose:** Comprehensive reference server showcasing all MCP features

**Location:** `Modules/AI/agents/MCP/github/servers/src/everything`

**Details:**
- **Language:** TypeScript (Node.js)
- **Transport:** Stdio / SSE / Streamable HTTP
- **Build Status:** Ready to build
- **Status:** Available

**Tools Available (20+):**
- `echo` - Echo utility
- `get-sum` - Math operations
- `get-env` - Environment variables
- `get-annotated-message` - Annotated content
- `get-resource-links` - Resource references
- `get-resource-reference` - Resource details
- `get-structured-content` - Structured responses
- `get-tiny-image` - Image content
- `trigger-long-running-operation` - Progress tracking
- `toggle-simulated-logging` - Logging control
- `toggle-subscriber-updates` - Update subscriptions
- `trigger-sampling-request` - LLM sampling
- `trigger-elicitation-request` - User input
- `get-roots-list` - File roots
- `gzip-file-as-resource` - File compression
- And more...

**Resources:**
- Dynamic Text Resources
- Dynamic Blob Resources
- Static Documents
- Session-scoped Resources

**Prompts:**
- `simple-prompt`
- `args-prompt`
- `completable-prompt`
- `resource-prompt`

**Build & Start:**
```bash
cd Modules/AI/agents/MCP/github/servers/src/everything
npm install
npm run build
npm start  # Or npm run start:stdio, start:sse, start:streamableHttp
```

**Files:**
- `src/everything/server/index.ts` - Server factory
- `src/everything/tools/` - Tool implementations
- `src/everything/resources/` - Resource definitions
- `src/everything/prompts/` - Prompt definitions
- `src/everything/transports/` - Transport implementations
- `docs/` - Architecture documentation

---

## 🔄 Connection Architecture

```
┌─────────────────────────────────────────────────────────┐
│  VS Code Copilot Chat (mcp.json configuration)         │
└────────────────────┬────────────────────────────────────┘
                     │
         ┌───────────┴──────────────┐
         ▼                          ▼
    ┌─────────────┐        ┌──────────────────┐
    │ arango-mcp  │        │  JarvisMCP       │
    │ (Stdio)     │        │  (HTTP Gateway)  │
    └─────────────┘        └──────────────────┘
                                   │
                    ┌──────────────┼──────────────┐
                    ▼              ▼              ▼
            ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
            │ Local Tools │ │ ArangoDB    │ │ Time/Git/   │
            │             │ │ MCP         │ │ Fetch MCPs  │
            │ • secret    │ │ (mounted)   │ │ (future)    │
            │ • echo      │ │             │ │             │
            │ • info      │ │ • arango_*  │ │ • get_time  │
            └─────────────┘ └─────────────┘ └─────────────┘
```

**Current Configuration (mcp.json):**
- `arango-mcp` - Direct stdio connection
- `JarvisMCP` - HTTP gateway (already has ArangoDB mounted)

**Future Extensions:**
- Mount Time MCP through JarvisMCP
- Mount Git MCP through JarvisMCP
- Mount Fetch MCP through JarvisMCP
- Mount Everything MCP through JarvisMCP

---

## 🚀 Startup Sequence (Recommended)

1. **Start ArangoDB Docker** (prerequisite)
   ```bash
   cd Modules/docker
   docker compose -f docker-compose.arango.yml up -d
   ```

2. **Start JarvisMCP** (includes mounted ArangoDB MCP)
   ```bash
   cd Modules/AI/agents/MCP/JarvisMCP
   python server.py
   ```

3. **Start Time MCP** (separate terminal)
   ```bash
   cd Modules/AI/agents/MCP/github/servers/src/time
   python -m mcp_server_time
   ```

4. **Start Git MCP** (separate terminal)
   ```bash
   cd Modules/AI/agents/MCP/github/servers/src/git
   python -m mcp_server_git <path_to_repo>
   ```

5. **Build Everything MCP** (TypeScript)
   ```bash
   cd Modules/AI/agents/MCP/github/servers/src/everything
   npm install
   npm run build
   ```

6. **Start Everything MCP** (separate terminal)
   ```bash
   npm start
   ```

---

## 📊 Current Status Summary

| MCP | Status | Type | Ready? |
|-----|--------|------|--------|
| JarvisMCP | ✅ Running | HTTP Gateway | Yes |
| ArangoDB MCP | ✅ Mounted | Stdio Subprocess | Yes |
| Time MCP | 🔵 Standby | Stdio | Yes |
| Git MCP | 🔵 Standby | Stdio | Yes |
| Fetch MCP | 🔵 Standby | Stdio | Yes |
| Everything MCP | 🔵 Standby | Stdio/SSE | Build needed |

---

## 🔧 Next Steps

1. ✅ Create unified startup script (`startup_all_mcps.py`)
2. ✅ Create MCP dashboard/monitor
3. ✅ Integrate all MCPs into mcp.json configuration
4. ✅ Create health check script
5. ✅ Create shutdown script

---

**Last Updated:** April 19, 2026  
**Maintained By:** MCP Integration Team  
**Version:** 1.0 (Inventory Phase)
