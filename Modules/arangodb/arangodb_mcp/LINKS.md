# ArangoDB MCP Module — Links

## GitHub Repository
- **mcp-server-arangodb Repo:** https://github.com/arangodb/mcp-server-arangodb
- **Cloned to:** `github/mcp-server-arangodb/`
- **ArangoDB GitHub Org:** https://github.com/arangodb

## Official Documentation
- **MCP Homepage:** https://modelcontextprotocol.io/
- **MCP Tools Concept:** https://modelcontextprotocol.io/docs/concepts/tools
- **ArangoDB MCP README:** https://github.com/arangodb/mcp-server-arangodb/blob/main/README.md

## Docker Image
- **Docker Hub:** https://hub.docker.com/r/arangodb/mcp-arangodb
- **Docker Pull:** `docker pull arangodb/mcp-arangodb:latest`

## Related Modules
- **`../`** — ArangoDB parent module (see `../LINKS.md`)
- **`../../docker/`** — Docker compose setup with MCP profile (`--profile mcp`)

## MCP Profile Usage
Start ArangoDB + MCP sidecar together:
```
docker compose -f ../docker/docker-compose.base.yml --profile mcp up -d
```
Or via the startup script with `--with-mcp`:
```
python scripts/startup_scripts/setup_arangodb_docker.py --with-mcp
```
