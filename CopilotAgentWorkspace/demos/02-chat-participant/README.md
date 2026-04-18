# Demo 02: Chat Participant

**Goal:** Learn how to create and register a custom chat participant that responds to @mentions in VSCode Chat.

## What This Demo Shows

- ✅ Creating a custom chat participant
- ✅ Registering with `vscode.chat.createChatParticipant()`
- ✅ Handling chat requests
- ✅ Streaming markdown responses
- ✅ Accessing chat history and context
- ✅ Logging interactions
- ✅ Setting participant metadata (icons, etc.)

## How It Works

### 1. Participant Registration

```typescript
const participant = vscode.chat.createChatParticipant(
  "demo.chatParticipant",
  handleChatRequest
);
participant.iconPath = new vscode.ThemeIcon("lightbulb");
```

### 2. Handler Function

```typescript
async function handleChatRequest(
  request: vscode.ChatRequest,        // User message + command
  context: vscode.ChatContext,        // Chat history
  stream: vscode.ChatResponseStream,  // For streaming response
  token: vscode.CancellationToken     // For cancellation
): Promise<void> {
  // ... handle request
  stream.markdown("Your response here");
}
```

### 3. Usage in VSCode Chat

In VSCode Chat (Cmd+Shift+L):
```
@demo What can you help me with?
```

## Commands

1. **Demo: Test Chat Participant**
   - Prompts for test message
   - Logs test interaction
   - Writes to `DEMO_CHAT_PARTICIPANT_TEST.json`

2. **Demo: Verify Chat Participant Registered**
   - Checks if participant is active
   - Shows registration status
   - Writes to `DEMO_PARTICIPANT_REGISTRATION.json`

## How to Use

### 1. Install and Run

```bash
npm install
npm run compile
npm test
```

### 2. Load in VSCode

```bash
code --extensionDevelopmentPath=$(pwd) .
```

### 3. Test the Participant

- Open VSCode Chat (Cmd+Shift+L)
- Type: `@demo Hello` followed by Enter
- You should see a response from the demo participant

### 4. Run Commands

From Command Palette (Cmd+Shift+P):
- "Demo: Test Chat Participant" - Manual test
- "Demo: Verify Chat Participant Registered" - Check status

### 5. Verify Output

Files generated:
- `DEMO_CHAT_PARTICIPANT_LOG.json` - All chat interactions
- `DEMO_CHAT_PARTICIPANT_TEST.json` - Manual test result
- `DEMO_PARTICIPANT_REGISTRATION.json` - Registration status

## What Gets Logged

### Chat Interaction
```json
{
  "timestamp": "2026-04-11T14:30:00.000Z",
  "userMessage": "Hello, how are you?",
  "commandRan": "default",
  "historyLength": 2
}
```

### Chat History Access
```typescript
context.history.forEach(turn => {
  if (turn instanceof vscode.ChatRequestTurn) {
    console.log("User said:", turn.prompt);
  } else if (turn instanceof vscode.ChatResponseTurn) {
    console.log("Bot responded:", turn.response);
  }
});
```

### Streaming Response Types

```typescript
// Markdown text
stream.markdown("**Bold text** with `code`");

// Code blocks
stream.markdown("```typescript\nconst x = 1;\n```");

// Buttons
stream.button({
  title: "Click Me",
  command: "my.command",
  arguments: ["arg1"]
});

// Anchor links
stream.anchor(
  vscode.Uri.file("/path/to/file"),
  "Link Text"
);
```

## Test Results

Runtime tests verify:
```
✓ PASS - Chat participant has required structure
✓ PASS - Chat request can be handled
✓ PASS - Response can be streamed
✓ PASS - Interactions can be logged
✓ PASS - Participant is discoverable
✓ PASS - Icon path is valid

📊 Results: 6/6 tests passed
```

## Key VSCode APIs Used

- `vscode.chat.createChatParticipant()` - Create participant
- `vscode.ChatRequest` - User message interface
- `vscode.ChatContext` - Chat history and context
- `vscode.ChatResponseStream` - Response streaming
- `vscode.ThemeIcon` - Participant icon

## Files Generated

| File | Purpose | Format |
|------|---------|--------|
| `DEMO_CHAT_PARTICIPANT_LOG.json` | All interactions | JSON |
| `DEMO_CHAT_PARTICIPANT_TEST.json` | Test result | JSON |
| `DEMO_PARTICIPANT_REGISTRATION.json` | Registration check | JSON |

## Chat Participant Features

### What You Can Do

1. **Access User Message** - `request.prompt`
2. **Access Chat History** - `context.history`
3. **Stream Responses** - `stream.markdown()`, `stream.button()`, etc.
4. **Handle Commands** - `request.command`
5. **Support Cancellation** - `token.isCancellationRequested`
6. **Provide Context** - Set icon, name, metadata
7. **Follow-up Questions** - Return ChatFollowup objects
8. **Provide Feedback Handler** - `onDidReceiveFeedback` event

### Response Types

- **Markdown** - Rich text formatting
- **Code Blocks** - Syntax-highlighted code
- **Buttons** - Interactive buttons
- **References** - Links to files/locations
- **File Trees** - Directory structure
- **Custom Renderers** - Can extend with custom rendering

## Common Patterns

### Handling Different Commands

```typescript
async function handleChatRequest(
  request: vscode.ChatRequest,
  context: vscode.ChatContext,
  stream: vscode.ChatResponseStream,
  token: vscode.CancellationToken
): Promise<void> {
  switch (request.command) {
    case "explain":
      stream.markdown("### Explanation\n...");
      break;
    case "refactor":
      stream.markdown("### Refactored Code\n...");
      break;
    default:
      stream.markdown("### Default Response\n...");
  }
}
```

### Accessing Chat History

```typescript
for (const historyItem of context.history) {
  if (historyItem instanceof vscode.ChatRequestTurn) {
    const userMessage = historyItem.prompt;
    // Process...
  }
}
```

### Streaming Multiple Chunks

```typescript
stream.markdown("First chunk...");
await someAsyncOperation();
stream.markdown("Second chunk...");
```

## Troubleshooting

**Chat participant not appearing in chat?**
- Ensure extension is loaded (Debug: Show Running Extensions)
- Check browser console for errors
- Try reloading window

**Messages not being received?**
- Verify participant ID matches in logs
- Check handler function is registered
- Check for errors in console output

**Response not streaming?**
- Ensure you're calling `stream.markdown()` or other methods
- Check token isn't cancelled
- Verify response has content

## Use Cases

- **Code Assistant** - Explain or refactor code
- **Documentation** - Generate docs from code
- **Debugging** - Analyze error messages
- **Learning** - Teach Copilot domain concepts
- **Integration** - Bridge to external services

## Next Steps

After this demo, explore:
- **Demo 03:** Language Model Tools - Create callable tools
- **Demo 04:** MCP Servers - Bridge to complex backends
- **Demo 05:** Custom Instructions - Guide Copilot behavior

---

*Part of VSCode Copilot API Demos Series*
