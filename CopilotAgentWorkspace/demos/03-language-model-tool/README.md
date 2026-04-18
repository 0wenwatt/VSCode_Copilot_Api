# Demo 03: Language Model Tool

**Goal:** Learn how to register and invoke tools that Copilot can call directly.

## What This Demo Shows

- ✅ Registering custom tools with `vscode.lm.registerTool()`
- ✅ Defining tool input schemas (JSON Schema)
- ✅ Implementing tool handlers
- ✅ Returning structured tool results
- ✅ Making tools available to Copilot chat
- ✅ Invoking tools programmatically
- ✅ Tracking tool invocations and logging

## How It Works

### 1. Tool Registration

```typescript
const tool = vscode.lm.registerTool("demo.countCodeLines", {
  name: "countCodeLines",
  description: "Count lines of code",
  inputSchema: {
    type: "object",
    properties: {
      includeComments: { type: "boolean" }
    }
  },
  invoke: async (options) => {
    // Handle tool invocation
    return new vscode.LanguageModelToolResult([{
      kind: "text",
      value: "Result here"
    }]);
  }
});
```

### 2. Tool Invocation Flow

```
Copilot in Chat
   ↓
Decides to use a tool (e.g., countCodeLines)
   ↓
Calls: lm.invokeTool("demo.countCodeLines", { includeComments: true })
   ↓
Extension handler runs
   ↓
Returns LanguageModelToolResult
   ↓
Copilot receives result and continues reasoning
```

## Tools in This Demo

### Tool 1: Count Code Lines
- **Purpose:** Count lines in active file, separate code from comments
- **Parameters:** `includeComments` (boolean)
- **Output:** Line counts by type

### Tool 2: Analyze Text
- **Purpose:** Analyze selected text for word/line/char counts
- **Parameters:** `includeStats` (boolean)
- **Output:** Text statistics

## Commands

1. **Demo: Invoke LM Tool Directly**
   - Pick a tool from list
   - Tool executes immediately
   - Log written to `DEMO_TOOL_INVOCATION_TEST.json`

2. **Demo: List Registered Tools**
   - Shows all registered tools
   - Call counts
   - Writes to `DEMO_REGISTERED_TOOLS.json`

## How to Use

### 1. Install and Test

```bash
npm install
npm run compile
npm test
```

### 2. Load in VSCode

```bash
code --extensionDevelopmentPath=$(pwd) .
```

### 3. Use Tools in Two Ways

#### Method 1: Direct Invocation
- From Command Palette: "Demo: Invoke LM Tool Directly"
- Select tool from list
- Tool executes
- Results logged

#### Method 2: Through Copilot Chat
- Open Chat (Cmd+Shift+L)
- Copilot can automatically use your tools
- Example: "Count the lines in my file" → Copilot uses `countCodeLines` tool

### 4. Verify Output

Files generated:
- `DEMO_LM_TOOL_LOG.json` - All tool invocations
- `DEMO_REGISTERED_TOOLS.json` - Tool list and call counts
- `DEMO_TOOL_INVOCATION_TEST.json` - Direct invocation test

## Input Schemas

Tools use JSON Schema to describe their parameters:

```json
{
  "type": "object",
  "properties": {
    "includeComments": {
      "type": "boolean",
      "description": "Include comment lines in the count"
    },
    "maxLines": {
      "type": "number",
      "description": "Maximum lines to process"
    }
  },
  "required": ["includeComments"]
}
```

Common schema types:
- `"type": "object"` - Object with properties
- `"type": "string"` - Text input
- `"type": "number"` - Numeric value
- `"type": "boolean"` - True/false
- `"type": "array"` - List of items
- `"enum": ["option1", "option2"]` - Fixed choices

## Tool Results

Tools return `LanguageModelToolResult`:

```typescript
new vscode.LanguageModelToolResult([
  {
    kind: "text",         // or "markdown"
    value: "Result text"
  }
])
```

Result kinds:
- **"text"** - Plain text
- **"markdown"** - Markdown formatted
- **"error"** - Error message

## Test Results

Runtime tests verify:
```
✓ PASS - Tool definition has required structure
✓ PASS - Input schema is valid
✓ PASS - Tool result has correct structure
✓ PASS - Tool invocation can be tracked
✓ PASS - Tool calls can be logged
✓ PASS - Tools are discoverable
✓ PASS - Tool parameters are serializable

📊 Results: 7/7 tests passed
```

## What Gets Logged

### Tool Invocation
```json
{
  "timestamp": "2026-04-11T14:30:00.000Z",
  "tool": "countCodeLines",
  "input": { "includeComments": true },
  "result": {
    "fileName": "extension.ts",
    "totalLines": 150,
    "codeLines": 120,
    "commentLines": 30
  }
}
```

### Tool Registration
```json
{
  "timestamp": "2026-04-11T14:29:00.000Z",
  "event": "tools_registered",
  "tools": ["demo.countCodeLines", "demo.analyzeText"],
  "status": "active"
}
```

## Key VSCode APIs Used

- `vscode.lm.registerTool()` - Register a tool
- `vscode.LanguageModelToolResult` - Tool result
- `vscode.lm.invokeTool()` - Invoke tool programmatically
- `vscode.lm.tools` - List registered tools

## Files Generated

| File | Purpose | Format |
|------|---------|--------|
| `DEMO_LM_TOOL_LOG.json` | All tool calls | JSON |
| `DEMO_REGISTERED_TOOLS.json` | Tool list | JSON |
| `DEMO_TOOL_INVOCATION_TEST.json` | Invocation test | JSON |

## Tool Life cycle

```
1. Registration
   └─ Tool defined and registered
   
2. Discovery
   └─ Copilot discovers available tools
   
3. Invocation Decision
   └─ Copilot decides to use a tool
   
4. Execution
   └─ Tool handler runs with parameters
   
5. Result Handling
   └─ Copilot receives result
   
6. Reasoning
   └─ Copilot uses result to answer user
```

## Best Practices

### 1. Clear Descriptions
```typescript
description: "Count non-empty, non-comment lines of code in the current editor"
// Good - specific and actionable
```

### 2. Precise Input Schema
```typescript
inputSchema: {
  type: "object",
  properties: {
    includeComments: { type: "boolean", description: "..." }
  },
  required: ["includeComments"]  // Explicit requirements
}
```

### 3. Meaningful Results
```typescript
return new vscode.LanguageModelToolResult([{
  kind: "text",
  value: JSON.stringify({ lineCount: 42, type: "code" }, null, 2)
}]);
```

### 4. Error Handling
```typescript
try {
  // tool logic
} catch (error) {
  return new vscode.LanguageModelToolResult([{
    kind: "text",
    value: `Error: ${error.message}`
  }]);
}
```

## Common Use Cases

1. **File Analysis** - Count lines, analyze structure
2. **Text Processing** - Extract, transform, summarize
3. **Project Queries** - Find files, analyze dependencies
4. **Testing** - Run tests, check coverage
5. **Formatting** - Apply code style, lint
6. **Compilation** - Check syntax, compile code
7. **Documentation** - Generate docs, update READMEs

## Troubleshooting

**Tool not appearing in Copilot?**
- Ensure tool is registered during activation
- Check extension logs for registration errors
- Verify tool ID is unique

**Tool invocation fails?**
- Check input schema matches call
- Add error handling in tool handler
- Log handler execution

**Results not showing?**
- Ensure LanguageModelToolResult is returned
- Check result contains valid content
- Verify kind is "text" or "markdown"

## Next Steps

After this demo, explore:
- **Demo 04:** MCP Servers - Bridge to complex backends
- **Demo 05:** Custom Instructions - Guide Copilot behavior
- **Demo 06:** Chat Hooks - Automate chat workflows

---

*Part of VSCode Copilot API Demos Series*
