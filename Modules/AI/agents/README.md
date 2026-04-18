# AI Agents Module

Comprehensive collection of agent frameworks, tools, and documentation for building AI agents.

## Structure

### `MCP/` — Model Context Protocol Agents
Implementations and servers for the Model Context Protocol:
- **FastMCP/** — FastMCP framework for building MCP servers
- **github/everything/** — Everything MCP server and implementations
- **JarvisMCP/** — Jarvis MCP implementation
- **LINKS.md** — MCP documentation and resources

### `VSCode_docs/` — VS Code Copilot Agents
Official documentation for building and using VS Code Copilot agents:
- `agents/` — Core agent documentation
  - overview.md
  - agents-tutorial.md
  - agent-tools.md
  - local-agents.md
  - cloud-agents.md
  - subagents.md
  - third-party-agents.md
  - planning.md
  - memory.md
  - copilot-cli.md
- **README.md** — Index and organization guide

### `hooks/` — Agent Lifecycle Hooks
Framework for agent lifecycle management and hooks

### `tools/` — Agent Tools & Utilities
Shared tools and utilities for agent development

### `instructions/` — Agent Instructions & Prompts
Instructions, prompts, and guidance for agent behavior

## Related Modules

- **Playwright MCP** (`Modules/playwright/`) — Browser automation with MCP for AI agents
- **LangChain** (`Modules/Lang_Ecosystem/langchain/`) — LLM framework for agents
- **LangGraph** (`Modules/Lang_Ecosystem/langgraph/`) — Agent state graphs and workflows
- **LangSmith** (`Modules/Lang_Ecosystem/langsmith/`) — Agent monitoring and debugging

## Quick Links

- **Model Context Protocol:** https://modelcontextprotocol.io/
- **VS Code Copilot Docs:** https://code.visualstudio.com/docs/copilot/overview
- **Playwright MCP:** https://github.com/microsoft/playwright-mcp
- **LangChain:** https://www.langchain.com/
- **LangGraph:** https://www.langchain.com/langgraph

## Key Concepts

### Model Context Protocol (MCP)
An open standard for connecting AI applications to external systems. Provides a standardized way to expose tools, resources, and data sources to LLMs.

### VS Code Copilot Agents
Built-in agent framework for VS Code that enables building custom agents for code generation, analysis, and automation.

### Agent Patterns
- **Subagents** — Specialized agents that handle specific tasks
- **Tool Use** — Structured tool calling for deterministic behavior
- **Planning** — Agentic planning and reasoning
- **Memory** — Persistent state and context management

## Getting Started

1. **Explore MCP servers** in `MCP/` to understand agent protocols
2. **Read VSCode documentation** in `VSCode_docs/agents/` for platform-specific guidance
3. **Use Playwright MCP** (`Modules/playwright/`) for browser automation in agents
4. **Leverage LangChain/LangGraph** from `Modules/Lang_Ecosystem/` for agent frameworks

## Architecture Overview

```
Agent Framework (MCP / VS Code Copilot)
    ↓
Tool Interface (agent-tools.md)
    ↓
Execution Environment
    ↓
External Systems
  ├── Browser (Playwright MCP)
  ├── Databases (SQL, ArangoDB, etc.)
  ├── APIs (REST, GraphQL)
  └── File Systems
```

## Adding New Agents

When adding new agent frameworks or implementations:

1. Create a subfolder with the framework name
2. Include a `README.md` explaining the framework
3. Include a `LINKS.md` with documentation links
4. Add relevant configuration files and examples
5. Document any special setup or requirements

## Contributing

When working with agents:
- Keep implementations modular and composable
- Document tool schemas clearly
- Provide example configurations
- Test against multiple MCP clients (VS Code, Cursor, Claude Desktop, etc.)
- Consider token efficiency for LLM context

## Resources

- [MCP Specification](https://modelcontextprotocol.io/)
- [VS Code Copilot API](https://code.visualstudio.com/docs/copilot/chat)
- [LangChain Agents](https://python.langchain.com/docs/modules/agents/)
- [Building Reliable Agents](https://www.anthropic.com/)
