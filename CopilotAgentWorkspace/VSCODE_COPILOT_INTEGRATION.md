# VSCode Copilot Integration Guide

**Connecting your LangChain + ArangoDB backend to VSCode Copilot**

---

## Overview: The Big Picture

```
┌─────────────────────────────────────────────────────────────────┐
│                     VSCode Editor Context                       │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Chat View                                                │  │
│  │ • User message → Copilot processes                       │  │
│  │ • Response rendered in chat                              │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              ↕                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Custom Instructions (.github/copilot-instructions.md)   │  │
│  │ • Always-on context injected before each request         │  │
│  │ • Guides Copilot behavior and knowledge                  │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              ↕                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ MCP Servers (.vscode/mcp.json)                           │  │
│  │ • stdio/HTTP bridge to your backend services             │  │
│  │ • Exposes tools (functions) + resources (context)        │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              ↕                                  │
└─────────────────────────────────────────────────────────────────┘
                              ↕
                  Your Backend (LangChain Agent)
                  • ArangoDB RAG system
                  • Graph-based reasoning
                  • Custom business logic
```

---

## 1. Custom Instructions: Teaching Copilot

**File:** `.github/copilot-instructions.md`

Custom instructions are always-on context. They're injected before every request, guiding Copilot on your codebase conventions and expectations.

### Create the instructions file:

```markdown
# Codebase Guidelines

## Context
This is a specialized backend system for [your domain]. It integrates:
- LangChain agents for reasoning
- ArangoDB for knowledge graphs and RAG
- VSCode chat interface for user interactions

## When answering questions:
1. Reference stored knowledge from the knowledge graph first
2. Use the RAG system for up-to-date information
3. Explain reasoning chains from the agent
4. Provide actionable code examples

## Key patterns in this codebase:
- Graph queries use ArangoDB AQL syntax
- Agents communicate via JSON message format
- All tools return {success: bool, data: any, error?: string}

## Do not:
- Make up information not in the knowledge graph
- Ignore the context from MCP tools
- Suggest solutions not verified by the graph
```

### Register in `package.json`:

```json
{
  "contributes": {
    "copilot": {
      "instructions": "./.github/copilot-instructions.md"
    }
  }
}
```

---

## 2. MCP Servers: Bridge to Your Backend

**File:** `.vscode/mcp.json`

The Model Context Protocol (MCP) server acts as a bridge. It exposes your backend functionality as **tools** (callable functions) and **resources** (readable context).

### Create MCP configuration:

```json
{
  "mcpServers": {
    "backend-agent": {
      "type": "stdio",
      "command": "node",
      "args": ["./mcp-server.js"],
      "env": {
        "AGENT_URL": "http://localhost:3000",
        "ARANGODB_URL": "http://localhost:8529"
      }
    }
  }
}
```

### Implement the MCP server (`mcp-server.js`):

```typescript
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import axios from "axios";

// Initialize MCP server
const server = new Server({
  name: "backend-agent",
  version: "1.0.0",
});

// TOOLS: Callable functions exposed to Copilot
server.setRequestHandler(definitions.ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "query_knowledge_graph",
        description: "Query the ArangoDB knowledge graph for information",
        inputSchema: {
          type: "object",
          properties: {
            query: {
              type: "string",
              description: "Natural language query (e.g., 'Find all users who purchased products in Q1')",
            },
            context: {
              type: "string",
              description: "Optional domain context to narrow results",
            },
          },
          required: ["query"],
        },
      },
      {
        name: "invoke_reasoning_agent",
        description: "Send a reasoning task to the LangChain agent",
        inputSchema: {
          type: "object",
          properties: {
            task: { type: "string", description: "Task description" },
            history: {
              type: "array",
              description: "Previous messages in the reasoning chain",
              items: { type: "string" },
            },
          },
          required: ["task"],
        },
      },
    ],
  };
});

// TOOL EXECUTION: Handle when Copilot calls a tool
server.setRequestHandler(definitions.CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  if (name === "query_knowledge_graph") {
    try {
      const response = await axios.post("http://localhost:3000/knowledge/query", {
        query: args.query,
        context: args.context,
      });
      return {
        content: [
          {
            type: "text",
            text: JSON.stringify(response.data, null, 2),
          },
        ],
      };
    } catch (error) {
      return {
        content: [{ type: "text", text: `Error: ${error.message}` }],
        isError: true,
      };
    }
  }

  if (name === "invoke_reasoning_agent") {
    try {
      const response = await axios.post("http://localhost:3000/agent/reason", {
        task: args.task,
        history: args.history || [],
      });
      return {
        content: [
          {
            type: "text",
            text: JSON.stringify(response.data, null, 2),
          },
        ],
      };
    } catch (error) {
      return {
        content: [{ type: "text", text: `Error: ${error.message}` }],
        isError: true,
      };
    }
  }

  return { content: [{ type: "text", text: "Unknown tool" }], isError: true };
});

// RESOURCES: Read-only context available to Copilot
server.setRequestHandler(definitions.ListResourcesRequestSchema, async () => {
  return {
    resources: [
      {
        uri: "arangodb://schema",
        name: "ArangoDB Schema",
        description: "Current schema of the knowledge graph",
        mimeType: "application/json",
      },
      {
        uri: "agent://capabilities",
        name: "Agent Capabilities",
        description: "What the reasoning agent can do",
        mimeType: "text/plain",
      },
    ],
  };
});

// START SERVER
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("Backend Agent MCP Server running");
}

main().catch(console.error);
```

---

## 3. The Chat Flow: How It Works

```
User in VSCode Chat
       ↓
[Query: "What are the top recommendations for user 42?"]
       ↓
VSCode Copilot reads:
  • Custom Instructions (.github/copilot-instructions.md)
  • Chat history from session
  • Available MCP tools from .vscode/mcp.json
       ↓
Copilot decides: "I need data from the knowledge graph"
       ↓
Calls MCP tool: query_knowledge_graph({query: "...", context: "user:42"})
       ↓
MCP Server → Your backend → ArangoDB
       ↓
Response: [{recommendation: "...", score: 0.87}, ...]
       ↓
Copilot synthesizes response with reasoning
       ↓
Rendered in chat: "Based on the knowledge graph, user 42 should..."
```

---

## 4. Hooks: Automation at 8 Lifecycle Events

**File:** `.github/hooks/onUserPromptSubmit.json`

Hooks execute shell commands at specific points in the chat lifecycle. Use them to:
- Log usage metrics
- Update context before processing
- Validate user intent
- Inject dynamic data

### Example hook - inject context before each request:

**File:** `.github/hooks/OnUserPromptSubmit.json`

```json
{
  "description": "Inject dynamic context before processing user prompt",
  "command": "node",
  "args": ["./hooks/collect-context.js"],
  "input": {
    "properties": {
      "prompt": { "type": "string" },
      "sessionId": { "type": "string" }
    }
  },
  "output": {
    "contextItems": {
      "type": "array",
      "description": "Array of context to add to the request"
    }
  }
}
```

**Implementation:** `./hooks/collect-context.js`

```javascript
const fs = require("fs");

async function collectContext() {
  const input = JSON.parse(fs.readFileSync(0, "utf-8"));
  
  // Get current active file info
  const activeFile = process.env.ACTIVE_FILE || "unknown";
  
  // Query backend for recent context
  const contextItems = [
    {
      type: "text",
      text: `Current working file: ${activeFile}`,
      source: "hook:file-context",
    },
    {
      type: "text",
      text: "Recent graph queries showed high activity in user recommendations.",
      source: "hook:backend-metrics",
    },
  ];

  console.log(JSON.stringify({ contextItems }));
}

collectContext().catch(console.error);
```

---

## 5. Five Progressive Demos

**Timeline: 4 days of implementation**

### Demo 1: Dead Simple Connection (Day 1, 1 hour)

**Goal:** Ensure MCP server can be called; verify basic connectivity.

**What to build:**
1. Create `.vscode/mcp.json` with echo server
2. Create a simple tool that returns mock data
3. Test calling it from chat

**Success criteria:**
- Chat command: `@codebase Can you test the connection?` works
- Copilot calls your MCP tool
- Response appears in chat

**Code:**

```typescript
// Simple echo MCP server
server.setRequestHandler(definitions.CallToolRequestSchema, async (request) => {
  const { name } = request.params;
  
  if (name === "test_connection") {
    return {
      content: [{
        type: "text",
        text: "✓ Connection successful! Backend is responding."
      }]
    };
  }
  
  return { content: [{ type: "text", text: "Unknown tool" }], isError: true };
});
```

---

### Demo 2: Real Query Tool (Day 1, 2 hours)

**Goal:** Connect to your ArangoDB to fetch real data.

**What to build:**
1. Implement `query_knowledge_graph` tool (see section 2)
2. Add simple ArangoDB query that returns mock schema
3. Test from chat

**Success criteria:**
- Chat: `@codebase What's in the knowledge graph?`
- Copilot calls tool
- Returns actual (or mocked) ArangoDB schema

**Code:**

```typescript
server.setRequestHandler(definitions.CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  if (name === "query_knowledge_graph") {
    // For now, return mock schema
    const mockSchema = {
      collections: ["users", "products", "recommendations"],
      edges: ["purchased", "recommends", "similar_to"],
    };
    return {
      content: [{ type: "text", text: JSON.stringify(mockSchema, null, 2) }],
    };
  }
});
```

---

### Demo 3: Agent Reasoning Integration (Day 2, 2 hours)

**Goal:** Call your LangChain agent for multi-step reasoning.

**What to build:**
1. Add `invoke_reasoning_agent` tool
2. Connect to your backend endpoint
3. Test multi-turn reasoning from chat

**Success criteria:**
- Chat: `@codebase Analyze user 42's behavior across 3 dimensions`
- Copilot calls reasoning agent
- Agent returns structured reasoning steps
- Chat displays reasoning chain

**Code:**

```typescript
if (name === "invoke_reasoning_agent") {
  const { task, history } = args;
  
  // Call your backend LangChain agent
  const response = await axios.post("http://localhost:3000/agent/reason", {
    task,
    conversationHistory: history || [],
    maxSteps: 5,
  });

  return {
    content: [{
      type: "text",
      text: `Reasoning complete:\n${JSON.stringify(response.data.reasoning, null, 2)}\n\nConclusion: ${response.data.conclusion}`
    }]
  };
}
```

---

### Demo 4: Custom Instructions Guidance (Day 2, 1.5 hours)

**Goal:** Make Copilot domain-aware using instructions.

**What to build:**
1. Create `.github/copilot-instructions.md` with your domain knowledge
2. Add specific patterns Copilot should follow
3. Test that Copilot references instructions in responses

**Success criteria:**
- Chat: `@codebase How should I query recommendations?`
- Copilot answers using patterns from instructions
- Mentions "following the codebase guidelines"

**File:** `.github/copilot-instructions.md`

```markdown
# [Your Domain] Backend Guidelines

## Architecture
- ArangoDB stores: users (vertices), products (vertices), purchased/recommends (edges)
- LangChain agent orchestrates multi-hop queries
- RAG retrieval uses vector embeddings for semantic search

## When recommending solutions:
1. Always start with a graph query to validate data exists
2. Use the agent for multi-step reasoning
3. Return results in {success, data, reasoning} format

## When user asks about user behavior:
- Always query the graph for recent activity first
- Don't assume data; verify via ArangoDB
- Explain which edges were traversed
```

---

### Demo 5: Full Integration with Hooks (Day 4, 3 hours)

**Goal:** Complete integration with context injection and error handling.

**What to build:**
1. Create hook that injects dynamic context before each prompt (see section 4)
2. Add error handling for backend failures
3. Add resource definitions (.arangodb schema)
4. Test complete flow: prompt → instruction + hooks + MCP tools → response

**Success criteria:**
- Chat: `@codebase Recommend products for user 123 based on graph similarity`
- Copilot:
  - Injects context via hook
  - Calls query tool
  - Calls reasoning agent
  - Synthesizes response with reasoning explanation
  - Response appears with proper formatting

**Complete flow test:**

```bash
# 1. Start your backend
npm start

# 2. Open VSCode with workspace
code . --profile Copilot

# 3. Open Copilot Chat (Cmd+Shift+L)
# 4. Type: "@codebase Find all users similar to user:42 who haven't purchased recently"
# Expected: Copilot calls both tools, returns reasoning chain
```

---

## 6. Implementation Checklist

- [ ] Create `.vscode/mcp.json` with stderr endpoint
- [ ] Implement MCP server with `query_knowledge_graph` tool
- [ ] Implement MCP server with `invoke_reasoning_agent` tool
- [ ] Create `.github/copilot-instructions.md`
- [ ] Create `package.json` contribution point for instructions
- [ ] Test Demo 1: Connection works
- [ ] Test Demo 2: Real ArangoDB query works
- [ ] Test Demo 3: LangChain agent integration works
- [ ] Test Demo 4: Custom instructions guide responses
- [ ] Create `.github/hooks/OnUserPromptSubmit.json`
- [ ] Test Demo 5: Full flow end-to-end
- [ ] Document tool schemas for your domain
- [ ] Set up error handling in MCP server
- [ ] Add logging for debugging

---

## 7. API References

**VSCode APIs used:**

- [`lm.registerMcpServerDefinitionProvider`](https://code.visualstudio.com/api/references/vscode-api#lm) - Register MCP server
- [`LanguageModelChatTool`](https://code.visualstudio.com/api/references/vscode-api#LanguageModelChatTool) - Define callable tools
- Custom instructions via `package.json` contribution point

**MCP Protocol:**

- [`ListToolsRequest`](https://spec.modelcontextprotocol.io/specification/server/capabilities/#tools) - Advertise tools
- [`CallToolRequest`](https://spec.modelcontextprotocol.io/specification/server/capabilities/#call-tool) - Execute tools
- [`ListResourcesRequest`](https://spec.modelcontextprotocol.io/specification/server/capabilities/#resources) - Advertise resources

**Documentation:**

- [VSCode Custom Instructions](https://code.visualstudio.com/docs/copilot/customization/custom-instructions)
- [VSCode MCP Servers](https://code.visualstudio.com/docs/copilot/customization/mcp-servers)
- [Model Context Protocol Spec](https://spec.modelcontextprotocol.io/)

---

## 8. Troubleshooting

**Copilot doesn't see MCP server:**
- Check `.vscode/mcp.json` syntax (valid JSON)
- Verify command path in `args` is correct
- Check `env` variables are set
- Restart VSCode

**Tool calls fail silently:**
- Check MCP server logs (stderr)
- Verify backend is running on configured URL
- Add comprehensive error handling in tool implementation

**Instructions not being applied:**
- Clear Copilot context (may be cached)
- Verify `.github/copilot-instructions.md` path
- Check `package.json` contribution point

---

## Next: Quick Start

1. **Right now (10 min):** Create `.vscode/mcp.json` with mock server
2. **Next 30 min:** Implement MCP server skeleton with one test tool
3. **Next hour:** Connect to your ArangoDB endpoint
4. **Next 2 hours:** Add LangChain agent tool
5. **Next hour:** Create custom instructions
6. **Day 2:** Run all 5 demos

**You're 6 hours from full integration.** 🚀
