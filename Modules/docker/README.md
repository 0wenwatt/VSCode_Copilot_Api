# Docker Module

This module contains Docker Compose configuration for running ArangoDB and related services.

## Quick Start

```bash
# Copy the environment file
cp .env.example .env

# Edit .env to configure:
# - ARANGO_ROOT_PASSWORD (default: test123)
# - ARANGO_PORT (default: 8529)
# - ARANGODB_MEMORY and ARANGODB_CORES

# Start the services
docker-compose -f docker-compose.base.yml up -d

# Or with ArangoDB-specific overrides
docker-compose -f docker-compose.arango.yml up -d
```

## Services

### ArangoDB
- **Image**: `arangodb:latest`
- **Container**: `arangodb-server`
- **Port**: `8529` (configurable via ARANGO_PORT)
- **Root Password**: `test123` (configurable via ARANGO_ROOT_PASSWORD)
- **Data Volumes**:
  - `arangodb-data`: Database data
  - `arangodb-apps`: Application data
- **Health Check**: HTTP version check on `/_api/version`

### MCP ArangoDB
- **Image**: `arangodb/mcp-arangodb:latest`
- **Container**: `mcp-arangodb`
- **Connects to**: ArangoDB service via internal network

## Configuration Files

- **docker-compose.base.yml**: Basic ArangoDB + MCP setup
- **docker-compose.arango.yml**: ArangoDB-specific configuration overlay
- **.env.example**: Environment variables template

## Network

Both services communicate via the `arangodb-net` Docker network.

## Volumes

- `arangodb-data`: Persists ArangoDB database files
- `arangodb-apps`: Persists ArangoDB app data

## Integration with Python Ops

See the parent `arangodb` module's `python-ops/` directory for CLI operations:

- `arango_http_up()`: Check if ArangoDB HTTP API is responding
- `arango_write_read_via_container()`: Test Docker exec operations
- `arango_insert_graph_http()`: Insert graph nodes and edges
- `arango_fetch_graph_http()`: Retrieve graph data

## Troubleshooting

### Container won't start
- Check Docker daemon is running
- Verify port 8529 is not in use: `lsof -i :8529`
- Check logs: `docker logs arangodb-server`

### Connection refused
- Wait for health check to pass (40+ seconds startup time)
- Verify credentials in `.env`
- Test connectivity: `curl -u root:test123 http://localhost:8529/_api/version`

## License

See parent directory LICENSE files.
