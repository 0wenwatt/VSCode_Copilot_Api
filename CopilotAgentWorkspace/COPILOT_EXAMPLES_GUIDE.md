# VSCode Copilot Examples Guide

A comprehensive guide to all Copilot-related examples in the vscode-extension-samples repository.

## Overview

The vscode-extension-samples repo contains 6 core Copilot-related examples that demonstrate different aspects of integrating with GitHub Copilot:

1. **Chat Interface** - Create custom chat participants
2. **Language Model API** - Use AI models directly in extensions
3. **Chat Tools** - Register tools for Copilot to invoke
4. **Chat Context** - Provide contextual information to Copilot
5. **MCP Integration** - Connect Model Context Protocol servers
6. **Chat Output** - Render custom widgets in chat

---

## Core Examples

### 1. Chat Sample
**Path:** `vscode-extension-samples/chat-sample/`

**What it demonstrates:**
- Creating custom chat participants (the `@participant` syntax)
- Using the Language Model API to request access to AI models
- Building chat participants with tools
- Two approaches to chat participant implementation

**Key Components:**
- `simple.ts` - Simple chat participant without tools
- `chatUtilsSample.ts` - Chat participant using `@vscode/chat-extension-utils`
- `toolParticipant.ts` - Advanced participant with LanguageModelTool API

**Features:**
- `@cat` participant - Simple cat tutor
- `@catTools` participant - Cat with tools support
- `@tool` participant - Advanced tool-based participant

**APIs Used:**
- `vscode.chat.registerChatParticipant()`
- `vscode.lm.selectChatModels()`
- `vscode.LanguageModelTool`

**Run it:**
```bash
cd chat-sample
npm install
# Run Extension target from Debug View
# See @cat, @catTools, @tool in Copilot Chat
```

---

### 2. Chat Tutorial
**Path:** `vscode-extension-samples/chat-tutorial/`

**What it demonstrates:**
- Step-by-step implementation of a chat participant
- Best practices for chat participant development
- Educational approach to Copilot Chat API

**Key Components:**
- Simple `@tutor` participant with `/exercise` command

**APIs Used:**
- `vscode.chat.registerChatParticipant()`
- `vscode.LanguageModelChatMessage`

**Run it:**
```bash
cd chat-tutorial
npm install
# Run Extension target from Debug View
# See @tutor participant in Copilot Chat
```

**Documentation:**
- https://code.visualstudio.com/api/extension-guides/chat-tutorial

---

### 3. Language Model API Tutorial
**Path:** `vscode-extension-samples/lm-api-tutorial/`

**What it demonstrates:**
- Using GitHub Copilot Language Model API directly
- Annotating code with inline tutoring tips
- Accessing language models without chat interface

**Key Features:**
- Analyzes code files and generates inline annotations
- Provides educational tips using AI
- `Toggle Tutor Annotations` command

**APIs Used:**
- `vscode.lm.selectChatModels()`
- `vscode.LanguageModelChatMessage`
- Inline editor decorations

**Run it:**
```bash
cd lm-api-tutorial
npm install
# Run Extension target from Debug View
# Open a code file
# Run "Toggle Tutor Annotations" from command palette
```

**Documentation:**
- https://code.visualstudio.com/api/extension-guides/language-model

---

### 4. Chat Context Provider Sample
**Path:** `vscode-extension-samples/chat-context-sample/`

**What it demonstrates:**
- Providing custom context to Copilot Chat
- Context provider API for specific file types
- How to make extension data available to Copilot

**Key Features:**
- Activates for JSON files
- Provides line count information as context
- Shows how to implement `ChatContextProvider`

**APIs Used:**
- `vscode.chat.registerChatResourceContextProvider()`
- `vscode.ChatContextProvider`
- `vscode.ChatContextItem`

**Run it:**
```bash
cd chat-context-sample
npm install
# Run Extension target from Debug View
# Context automatically available in chat for JSON files
```

**Contribution Points:**
- `chatContext` - Register custom context providers
- `onChatContextProvider` - Activation events

---

### 5. Chat Model Provider Sample
**Path:** `vscode-extension-samples/chat-model-provider-sample/`

**What it demonstrates:**
- Implementing custom chat model providers
- Providing multiple AI models to Copilot
- Model capability declaration (tool calling, vision, token limits)

**Key Features:**
- **Dog Model** - Dog-themed responses
- **Cat Model** - Cat-themed responses
- Declares capabilities: tool calling, vision support
- Max input tokens: 120,000
- Max output tokens: 8,192

**Architecture:**
- `extension.ts` - Registers the LM API provider
- `provider.ts` - Implements `LanguageModelChatProvider2`

**APIs Used:**
- `vscode.lm.registerLanguageModelChatProvider()`
- `LanguageModelChatProvider2` interface
- `LanguageModelChatResponse`

**Run it:**
```bash
cd chat-model-provider-sample
npm install
# Run Extension target from Debug View
# Custom models available in chat
```

**Model Capabilities:**
```typescript
{
  toolCalling: true,
  vision: true,
  maxInputTokens: 120000,
  maxOutputTokens: 8192
}
```

---

### 6. Chat Output Renderer Sample
**Path:** `vscode-extension-samples/chat-output-renderer-sample/`

**What it demonstrates:**
- Custom rendering of chat output
- Tool invocation results displayed as widgets
- Webview integration for rich UI in chat

**Key Features:**
- Register custom output renderers
- Render tool results as custom widgets
- Webview-based rich UI

**APIs Used:**
- `vscode.chat.registerChatOutputRenderer()` (proposed)
- Webview API
- Tool invocation results

**Run it:**
```bash
cd chat-output-renderer-sample
npm install
# Requires VS Code 1.109+
# Run Extension target from Debug View
```

---

### 7. MCP Extension Sample
**Path:** `vscode-extension-samples/mcp-extension-sample/`

**What it demonstrates:**
- Model Context Protocol (MCP) integration
- Connecting external MCP servers to Copilot
- Server-based tool capabilities

**Key Features:**
- `Add Gist Source` command
- Load MCP servers from GitHub gist
- Use MCP-provided tools in Copilot Chat

**APIs Used:**
- `vscode.lm.registerMCPServer()` (proposed)
- MCP connection API

**Run it:**
```bash
cd mcp-extension-sample
npm install
# Run Extension target from Debug View
# Run "Add Gist Source" command
# Provide gist URL with MCP servers
```

**Example MCP Gist:**
- https://gist.github.com/connor4312/3939ae7f6e55b2e391b5d585df27465c

---

## Feature Matrix

| Example | Chat Participant | LM API | Tools | Context | Custom Model | Output Renderer | MCP |
|---------|------------------|--------|-------|---------|--------------|-----------------|-----|
| chat-sample | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| chat-tutorial | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| lm-api-tutorial | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| chat-context-sample | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ |
| chat-model-provider-sample | ❌ | ✅ | ❌ | ❌ | ✅ | ❌ | ❌ |
| chat-output-renderer-sample | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| mcp-extension-sample | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |

---

## API Reference Quick Links

### Chat APIs
- `vscode.chat.registerChatParticipant()` - Register a chat participant
- `vscode.chat.registerChatResourceContextProvider()` - Provide context
- `vscode.chat.registerChatOutputRenderer()` - Custom rendering (proposed)

### Language Model APIs
- `vscode.lm.selectChatModels()` - Select available models
- `vscode.lm.registerLanguageModelChatProvider()` - Provide models
- `vscode.lm.registerTool()` - Register callable tools

### Messages
- `vscode.LanguageModelChatMessage` - Chat message type
- `vscode.LanguageModelChatResponse` - Chat response
- `vscode.ChatContextItem` - Context item

### Tools
- `vscode.LanguageModelTool` - Tool interface
- `vscode.LanguageModelToolResult` - Tool result

### MCP
- `vscode.lm.registerMCPServer()` - Register MCP connection

---

## Common Patterns

### Pattern 1: Simple Chat Participant

```typescript
const participant = vscode.chat.registerChatParticipant('chat-sample.cat', {
  handler: async (request, context, stream, token) => {
    const models = await vscode.lm.selectChatModels();
    if (models.length === 0) {
      stream.markdown('No language models available.');
      return;
    }

    const response = await models[0].sendRequest(
      [new vscode.LanguageModelChatMessage(vscode.LanguageModelChatMessageRole.User, request.prompt)],
      {},
      token
    );

    for await (const chunk of response.text) {
      stream.markdown(chunk);
    }
  }
});
```

### Pattern 2: Chat Participant with Tools

```typescript
const participant = vscode.chat.registerChatParticipant('chat-sample.tools', {
  handler: async (request, context, stream, token) => {
    // Handle tool invocations
    for (const toolUse of request.toolUses) {
      const result = await invokeTool(toolUse);
      stream.markdown(`Tool result: ${result}`);
    }
  }
});
```

### Pattern 3: Context Provider

```typescript
const provider = vscode.chat.registerChatResourceContextProvider('myid.context', {
  provideResourceChatContext: async (resource, token) => {
    // Analyze the resource
    const info = await analyzeFile(resource);
    return {
      value: info,
      description: 'File analysis'
    };
  }
});
```

### Pattern 4: Custom Model Provider

```typescript
vscode.lm.registerLanguageModelChatProvider('vendor.model', {
  models: [
    {
      id: 'model1',
      vendor: 'vendor',
      family: 'model',
      name: 'Model 1',
      version: '1.0',
      maxInputTokens: 120000,
      maxOutputTokens: 8192,
    }
  ],
  async sendRequest(message, from, options, token) {
    // Handle chat request
    return new vscode.LanguageModelChatResponse(...);
  }
});
```

---

## Dependencies

Most examples use common dependencies:

```json
{
  "vscode": "^1.90.0",
  "@types/vscode": "^1.90.0",
  "@vscode/prompt-tsx": "^0.1.0",
  "@vscode/chat-extension-utils": "^0.0.0-alpha.1"
}
```

---

## Learning Path

### Beginner
1. Start with **chat-tutorial** - Simplest example
2. Move to **chat-sample** (simple.ts) - Basic participant

### Intermediate
1. **chat-sample** (chatUtilsSample.ts) - Tools and utilities
2. **lm-api-tutorial** - Direct LM API usage
3. **chat-context-sample** - Providing context

### Advanced
1. **chat-sample** (toolParticipant.ts) - Complex tool handling
2. **chat-model-provider-sample** - Custom models
3. **chat-output-renderer-sample** - Custom rendering
4. **mcp-extension-sample** - MCP integration

---

## Troubleshooting

### Models not available
- Make sure GitHub Copilot extension is installed
- Check extension is activated properly
- Verify models are selected correctly

### Chat participant not appearing
- Check onChatParticipant activation event is defined
- Ensure extension is properly activated
- Look at extension output for errors

### Tools not working
- Verify tool schema is valid JSON Schema
- Check tool name matches handler registration
- Ensure token is passed to async operations

### Context not showing
- Check onChatContextProvider activation event
- Verify resource URI matches provider pattern
- Look at chat context panel for registered providers

---

## Official Documentation

- **Chat API Guide**: https://code.visualstudio.com/api/extension-guides/chat
- **Language Model API**: https://code.visualstudio.com/api/extension-guides/language-model
- **Chat Tutorial**: https://code.visualstudio.com/api/extension-guides/chat-tutorial
- **API Reference**: https://code.visualstudio.com/api/references/vscode-api

---

## Additional Resources

- **VSCode Extension Samples GitHub**: https://github.com/microsoft/vscode-extension-samples
- **Copilot Chat Extensions**: https://marketplace.visualstudio.com/search?target=VSCode&category=Chat
- **MCP Protocol**: https://modelcontextprotocol.io/

---

*Last updated: April 11, 2026*
