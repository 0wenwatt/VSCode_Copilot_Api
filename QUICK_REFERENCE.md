# ⚡ MCP Quick Reference Card

**Print this or bookmark it!**

---

## 🚀 START MCPs

```bash
python startup_all_mcps.py
```

Done! All 6 MCPs starting:
- ✅ ArangoDB Docker
- ✅ JarvisMCP (8765)
- ✅ Time MCP
- ✅ Git MCP
- ✅ Fetch MCP
- ✅ Everything MCP

---

## 🔍 CHECK HEALTH

```bash
python mcp_health_check.py --watch
```

Live dashboard of all MCPs

---

## 🛑 SHUTDOWN

```bash
python mcp_shutdown.py
```

Graceful shutdown of all MCPs

---

## 📊 MCPs AT A GLANCE

| MCP | Type | Port | Start Command |
|-----|------|------|---|
| **JarvisMCP** | HTTP Gateway | 8765 | `cd Modules/AI/agents/MCP/JarvisMCP && python server.py` |
| **ArangoDB** | Database | 8893 | `cd Modules/docker && docker compose -f docker-compose.arango.yml up -d` |
| **Time** | Utilities | - | `cd Modules/AI/agents/MCP/github/servers/src/time && python -m mcp_server_time` |
| **Git** | Tools | - | `cd Modules/AI/agents/MCP/github/servers/src/git && python -m mcp_server_git .` |
| **Fetch** | Web | - | `cd Modules/AI/agents/MCP/github/servers/src/fetch && python -m mcp_server_fetch` |
| **Everything** | Reference | 3001 | `cd Modules/AI/agents/MCP/github/servers/src/everything && npm start` |

---

## 🛠️ AVAILABLE TOOLS

### Via JarvisMCP (8765)
- `get_secret_phrase()` - Secret message
- `echo(message)` - Echo text
- `get_server_info()` - Server status
- `arangodb_query()` - Database queries
- `arangodb_insert()` - Insert documents
- `arangodb_update()` - Update documents
- `arangodb_remove()` - Delete documents

### Via Individual MCPs
- `get_current_time()` - Time in any timezone
- `git_status()` - Repository status
- `git_commit()` - Commit changes
- `git_log()` - View history
- `fetch()` - Web content
- 20+ tools in Everything MCP

---

## 💻 VS CODE SETUP

1. Open Copilot Chat
2. Start MCPs: `python startup_all_mcps.py`
3. Chat automatically recognizes MCPs
4. Use tools in conversations!

**Example:**
```
User: "Use get_current_time to check time in Tokyo"
Copilot: Calls tool → Returns: "9:15 PM JST"
```

---

## ⚙️ STARTUP OPTIONS

```bash
# Start all MCPs
python startup_all_mcps.py

# Start specific MCPs
python startup_all_mcps.py --only jarvis,time,git

# Skip certain MCPs
python startup_all_mcps.py --skip everything

# Skip Docker (if already running)
python startup_all_mcps.py --no-arangodb

# Dry run (validate only)
python startup_all_mcps.py --dry-run

# Live monitoring
python startup_all_mcps.py --monitor
```

---

## 🔧 TROUBLESHOOTING

**Port already in use:**
```bash
netstat -ano | findstr :8765
taskkill /PID <PID> /F
```

**Docker issues:**
```bash
docker compose -f Modules/docker/docker-compose.arango.yml down -v
docker compose -f Modules/docker/docker-compose.arango.yml up -d
```

**Health check:**
```bash
python mcp_health_check.py --detailed
```

**Force shutdown:**
```bash
python mcp_shutdown.py --force
```

---

## 📁 IMPORTANT FILES

| File | Purpose |
|------|---------|
| `startup_all_mcps.py` | Start all MCPs |
| `mcp_health_check.py` | Monitor health |
| `mcp_shutdown.py` | Stop all MCPs |
| `MCP_INVENTORY.md` | Full catalog |
| `MCP_COMPLETE_GUIDE.md` | Detailed guide |
| `MCP_SYSTEM_SUMMARY.md` | Overview |

---

## 🎯 3-STEP START

1. **Terminal 1:** `python startup_all_mcps.py`
2. **Terminal 2:** `python mcp_health_check.py --watch`
3. **VS Code:** Open Copilot Chat → Start using!

---

## 📞 QUICK HELP

**Q: What MCPs are available?**  
A: 6 total - JarvisMCP (gateway), ArangoDB, Time, Git, Fetch, Everything

**Q: How to verify all MCPs work?**  
A: `python mcp_health_check.py`

**Q: How to use in Copilot Chat?**  
A: Start MCPs, open chat, use tools naturally

**Q: How to shut down?**  
A: `python mcp_shutdown.py`

**Q: Can I run individual MCPs?**  
A: Yes! See startup options above

**Q: What if a port is in use?**  
A: Kill process with `taskkill /PID <PID> /F` or change port in config

**Q: How to see what tools are available?**  
A: `python mcp_health_check.py --detailed`

---

## ✅ VERIFICATION

After running `python startup_all_mcps.py`:

- [ ] All 6 MCPs showing as started
- [ ] No error messages
- [ ] Health check shows green
- [ ] Copilot Chat loads MCPs
- [ ] Can call tools in chat

**Run:** `python mcp_health_check.py`

---

## 🚨 EMERGENCY SHUTDOWN

```bash
# Graceful
python mcp_shutdown.py

# Force kill everything
python mcp_shutdown.py --force

# Clean everything (includes data)
python mcp_shutdown.py --purge
```

---

**Status:** ✅ Ready to Use  
**Last Updated:** April 19, 2026  
**Version:** 1.0
