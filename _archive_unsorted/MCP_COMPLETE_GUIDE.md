# 🚀 Complete MCP Startup & Management Guide

**Last Updated:** April 19, 2026  
**Workspace:** VSCode_Copilot_Api  
**Status:** All Systems Ready ✅

---

## 📋 Quick Start (3 Steps)

### Step 1: Start All MCPs
```bash
# Terminal 1: Start the unified startup system
python startup_all_mcps.py

# This will start:
# ✓ ArangoDB Docker (prerequisite)
# ✓ JarvisMCP (HTTP gateway on port 8765)
# ✓ Time MCP (terminal 2)
# ✓ Git MCP (terminal 3)
# ✓ Fetch MCP (terminal 4)
# ✓ Everything MCP (terminal 5)
```

### Step 2: Check Health
```bash
# In a new terminal: Monitor health
python mcp_health_check.py --watch
```

### Step 3: Use in VS Code
- Open Copilot Chat
- MCPs are automatically available
- All tools accessible through configuration

---

## 🎯 Available MCPs

### 1. **JarvisMCP** (PRIMARY GATEWAY) ✅
**Status:** Fully Operational  
**Purpose:** HTTP Gateway orchestrating all remote MCPs  
**URL:** `http://127.0.0.1:8765/mcp`  
**Transport:** HTTP + SSE

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

**VS Code Config:**
```json
{
  "JarvisMCP": {
    "url": "127.0.0.1:8765",
    "type": "http"
  }
}
```

---

### 2. **ArangoDB MCP** (MOUNTED) ✅
**Status:** Available through JarvisMCP  
**Purpose:** Database operations for ArangoDB  
**Database URL:** `http://127.0.0.1:8893`  
**Auth:** root / test123  
**Transport:** Stdio (as subprocess)

**Tools:**
- `arangodb_query` - Execute AQL queries
- `arangodb_insert` - Insert documents
- `arangodb_update` - Update documents
- `arangodb_remove` - Delete documents
- `arangodb_backup` - Backup collections
- `arangodb_list_collections` - List collections
- `arangodb_create_collection` - Create collections

**Start (via JarvisMCP):**
```bash
cd Modules/AI/agents/MCP/JarvisMCP
python server.py  # Includes ArangoDB MCP automatically
```

**Direct Start (alternative):**
```bash
cd Modules/arangodb/arangodb_mcp/github/mcp-server-arangodb
npm install
node build/index.js
```

**VS Code Config (Direct):**
```json
{
  "arango-mcp": {
    "type": "stdio",
    "command": "node",
    "args": ["build/index.js"],
    "cwd": "C:/Users/Owen/Desktop/Brogramming/VSCode_Copilot_Api/Modules/arangodb/arangodb_mcp/github/mcp-server-arangodb",
    "env": {
      "ARANGO_URL": "http://localhost:8893",
      "ARANGO_DB": "_system",
      "ARANGO_USERNAME": "root",
      "ARANGO_PASSWORD": "test123"
    }
  }
}
```

---

### 3. **Time MCP** 🕐
**Status:** Ready to Integrate  
**Purpose:** Time and timezone conversion utilities  
**Transport:** Stdio / SSE

**Tools:**
- `get_current_time` - Get time in specific timezone
- `convert_time` - Convert between timezones

**Start:**
```bash
cd Modules/AI/agents/MCP/github/servers/src/time
python -m mcp_server_time
```

**VS Code Config:**
```json
{
  "time-mcp": {
    "type": "stdio",
    "command": "python",
    "args": ["-m", "mcp_server_time"],
    "cwd": "C:/Users/Owen/Desktop/Brogramming/VSCode_Copilot_Api/Modules/AI/agents/MCP/github/servers/src/time"
  }
}
```

---

### 4. **Git MCP** 🔧
**Status:** Ready to Integrate  
**Purpose:** Git repository operations and querying  
**Transport:** Stdio / SSE

**Tools:**
- `git_status` - Repository status
- `git_diff_unstaged` - Unstaged changes
- `git_diff_staged` - Staged changes
- `git_commit` - Create commits
- `git_add` - Stage files
- `git_log` - Commit history
- `git_create_branch` - Create branches
- `git_checkout` - Switch branches
- And more...

**Start:**
```bash
cd Modules/AI/agents/MCP/github/servers/src/git
python -m mcp_server_git .
```

**VS Code Config:**
```json
{
  "git-mcp": {
    "type": "stdio",
    "command": "python",
    "args": ["-m", "mcp_server_git", "."],
    "cwd": "C:/Users/Owen/Desktop/Brogramming/VSCode_Copilot_Api"
  }
}
```

---

### 5. **Fetch MCP** 🌐
**Status:** Ready to Integrate  
**Purpose:** Web content fetching and HTML-to-Markdown  
**Transport:** Stdio / SSE

**Tools:**
- `fetch` - Fetch URLs and convert to Markdown
- Robots.txt compliant
- HTML simplification
- Raw HTML option

**Start:**
```bash
cd Modules/AI/agents/MCP/github/servers/src/fetch
python -m mcp_server_fetch
```

**VS Code Config:**
```json
{
  "fetch-mcp": {
    "type": "stdio",
    "command": "python",
    "args": ["-m", "mcp_server_fetch"],
    "cwd": "C:/Users/Owen/Desktop/Brogramming/VSCode_Copilot_Api/Modules/AI/agents/MCP/github/servers/src/fetch"
  }
}
```

---

### 6. **Everything MCP** 📚
**Status:** Ready to Build  
**Purpose:** Reference server with comprehensive MCP features  
**Transport:** Stdio / SSE / HTTP

**Features:**
- 20+ tools demonstrating MCP capabilities
- Multiple resource types (Text, Blob, Files, Session-scoped)
- 4 different prompts with completions
- Long-running operations with progress
- Task support (experimental)

**Build & Start:**
```bash
cd Modules/AI/agents/MCP/github/servers/src/everything
npm install
npm run build
npm start
```

**VS Code Config:**
```json
{
  "everything-mcp": {
    "type": "stdio",
    "command": "npm",
    "args": ["start"],
    "cwd": "C:/Users/Owen/Desktop/Brogramming/VSCode_Copilot_Api/Modules/AI/agents/MCP/github/servers/src/everything"
  }
}
```

---

## 🔧 Startup Scripts

### **startup_all_mcps.py** (Recommended)
Start all MCPs with proper sequencing and health checks.

**Usage:**
```bash
# Start everything
python startup_all_mcps.py

# Start only specific MCPs
python startup_all_mcps.py --only jarvis,time,git

# Skip certain MCPs
python startup_all_mcps.py --skip everything

# Skip ArangoDB Docker (if already running)
python startup_all_mcps.py --no-arangodb

# Dry run (show commands without executing)
python startup_all_mcps.py --dry-run

# Show live monitoring
python startup_all_mcps.py --monitor
```

**Options:**
- `--only`: Start specific MCPs (comma-separated)
- `--skip`: Skip specific MCPs
- `--dry-run`: Show commands without running
- `--no-arangodb`: Skip Docker startup
- `--monitor`: Live status monitoring
- `--check-only`: Only check running status

---

### **mcp_health_check.py** (Monitoring)
Check status and health of all MCPs.

**Usage:**
```bash
# Quick status check
python mcp_health_check.py

# Detailed diagnostics
python mcp_health_check.py --detailed

# Continuous monitoring (updates every 5s)
python mcp_health_check.py --watch

# Run comprehensive tests
python mcp_health_check.py --test
```

**Features:**
- Port connectivity checks
- API responsiveness tests
- Configuration validation
- Tool availability reporting
- Live status dashboard

---

### **mcp_shutdown.py** (Cleanup)
Gracefully shut down all MCPs.

**Usage:**
```bash
# Graceful shutdown
python mcp_shutdown.py

# Force termination
python mcp_shutdown.py --force

# Cleanup Docker volumes (data loss!)
python mcp_shutdown.py --purge

# Only stop Docker
python mcp_shutdown.py --docker-only

# Only stop processes
python mcp_shutdown.py --processes-only
```

---

## 📊 Architecture Diagram

```
┌──────────────────────────────────────────────────────────┐
│  VS Code Copilot Chat                                   │
│  (mcp.json configuration)                               │
└──────────────────┬───────────────────────────────────────┘
                   │
        ┌──────────┴──────────┐
        │                     │
        ▼                     ▼
   ┌─────────────┐    ┌──────────────────┐
   │ arango-mcp  │    │  JarvisMCP       │
   │ (Direct)    │    │  (HTTP Gateway)  │
   │ Stdio       │    │  Port: 8765      │
   └─────────────┘    └──────────────────┘
                           │
                ┌──────────┼──────────┐
                ▼          ▼          ▼
          ┌─────────┐ ┌─────────┐ ┌─────────┐
          │ Local   │ │Arangodb │ │ Time/   │
          │ Tools   │ │ MCP     │ │ Git/    │
          │         │ │         │ │ Fetch   │
          │• secret │ │• query  │ │         │
          │• echo   │ │• insert │ │(mounted)│
          │• info   │ │• update │ │         │
          └─────────┘ └─────────┘ └─────────┘
```

---

## 🚀 Recommended Startup Procedure

### **Option 1: All MCPs (Complete Setup)**
```bash
# Terminal 1: Run unified startup
python startup_all_mcps.py

# Terminal 2: Monitor health
python mcp_health_check.py --watch

# Then use in VS Code Copilot Chat
```

### **Option 2: Essential MCPs Only (Quick)**
```bash
# Terminal 1: Start JarvisMCP gateway
cd Modules/AI/agents/MCP/JarvisMCP
python server.py

# Terminal 2: Start ArangoDB Docker (if not running)
cd Modules/docker
docker compose -f docker-compose.arango.yml up -d

# Then use in VS Code Copilot Chat
```

### **Option 3: Individual MCPs**
```bash
# Start only the MCPs you need in separate terminals

# Terminal 1: ArangoDB Docker
cd Modules/docker
docker compose -f docker-compose.arango.yml up -d

# Terminal 2: JarvisMCP
cd Modules/AI/agents/MCP/JarvisMCP
python server.py

# Terminal 3: Time MCP
cd Modules/AI/agents/MCP/github/servers/src/time
python -m mcp_server_time

# Terminal 4: Git MCP
cd Modules/AI/agents/MCP/github/servers/src/git
python -m mcp_server_git .

# And so on...
```

---

## ✅ Verification Checklist

After starting MCPs:

- [ ] ArangoDB Docker running (`docker ps`)
- [ ] JarvisMCP responding on port 8765 (`curl http://127.0.0.1:8765/mcp`)
- [ ] ArangoDB API responding (`curl -u root:test123 http://127.0.0.1:8893/_api/version`)
- [ ] Health check shows all green (`python mcp_health_check.py`)
- [ ] VS Code recognizes MCP servers (`Copilot Chat → Settings`)
- [ ] Tools are available in chat

---

## 🐛 Troubleshooting

### **JarvisMCP won't start**
```bash
# Check if port 8765 is already in use
netstat -ano | findstr :8765

# Kill the process if needed
taskkill /PID <PID> /F

# Check dependencies
pip install -r Modules/AI/agents/MCP/JarvisMCP/requirements.txt
```

### **ArangoDB Docker won't start**
```bash
# Check Docker status
docker ps -a

# View logs
docker compose -f Modules/docker/docker-compose.arango.yml logs arangodb

# Rebuild
docker compose -f Modules/docker/docker-compose.arango.yml down
docker compose -f Modules/docker/docker-compose.arango.yml up -d
```

### **Port conflicts**
```bash
# Find what's using the port
netstat -ano | findstr :<port>

# Change port in config
# JarvisMCP: Edit Modules/AI/agents/MCP/JarvisMCP/.env (JARVIS_HTTP_PORT)
# ArangoDB: Edit Modules/docker/docker-compose.arango.yml (ports)
```

### **Python dependencies missing**
```bash
# Install all MCP dependencies
pip install mcp httpx fastmcp

# For Git MCP
pip install gitpython

# For Fetch MCP
pip install readabilipy protego

# For Time MCP
pip install tzlocal
```

### **Node.js issues**
```bash
# Check Node.js version
node --version
npm --version

# Install dependencies for Everything MCP
cd Modules/AI/agents/MCP/github/servers/src/everything
npm install

# Rebuild TypeScript
npm run build
```

---

## 📚 Files Created/Updated

| File | Purpose |
|------|---------|
| `MCP_INVENTORY.md` | Comprehensive MCP catalog |
| `startup_all_mcps.py` | Unified startup system |
| `mcp_health_check.py` | Health monitoring & diagnostics |
| `mcp_shutdown.py` | Graceful shutdown & cleanup |
| `mcp_config_extended.json` | Complete mcp.json configuration |

---

## 🎯 Next Steps

1. ✅ **Verify all MCPs work** → `python mcp_health_check.py`
2. ✅ **Test in VS Code** → Open Copilot Chat
3. ✅ **Use in workflows** → Leverage tools in your development
4. ✅ **Monitor health** → Run `python mcp_health_check.py --watch`
5. ✅ **Graceful shutdown** → `python mcp_shutdown.py` when done

---

## 📞 Support

**Quick Commands Reference:**
```bash
# Start everything
python startup_all_mcps.py

# Check health
python mcp_health_check.py --watch

# Shutdown
python mcp_shutdown.py

# View inventory
cat MCP_INVENTORY.md

# Test individual MCP
cd Modules/AI/agents/MCP/JarvisMCP
python test_mcp.py
```

---

**Created:** April 19, 2026  
**Status:** Production Ready ✅  
**Version:** 2.0 (Complete Integration)
