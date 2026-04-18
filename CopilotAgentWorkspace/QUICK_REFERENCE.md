# Quick Reference Guide

**For**: VSCode Copilot API Integration  
**Purpose**: Fast lookup for common patterns, APIs, and workflows  
**Last Updated**: April 11, 2026

---

## 🎯 At a Glance

### What's in the Repo?
- **81 sample extensions** demonstrating VSCode APIs
- **11 categories** of functionality
- **100% TypeScript** examples
- **Production-quality** reference code

### Key Integration Points
1. **Chat Participants** - Custom Copilot commands
2. **Inline Completions** - Code suggestions while typing
3. **Language Model API** - Access to Copilot's AI
4. **Context Providers** - Share workspace context
5. **Custom Commands** - Copilot-callable actions

---

## 📚 Sample Lookup by Use Case

### "I want to add a chat command"
**Relevant Samples**:
- `chat-sample` - Basic chat participant
- `chat-context-sample` - Adding context
- `chat-model-provider-sample` - Using LM API

**Quick Pattern**:
```typescript
// In extension activation
export function activate(context: vscode.ExtensionContext) {
  // Register chat participant
  const participant = vscode.chat.createChatParticipant(
    'my-participant',
    async (request: vscode.LanguageModelChatRequest) => {
      const response = await request.model.sendRequest(
        request.messages,
        {},
        new vscode.CancellationTokenSource().token
      );
      return new vscode.LanguageModelChatResponse([response]);
    }
  );

  context.subscriptions.push(participant);
}
```

---

### "I want to provide inline code suggestions"
**Relevant Samples**:
- `inline-completions-sample` - Basic inline completions
- `completions-sample` - Code completion patterns
- `lm-api-tutorial` - Using language models

**Quick Pattern**:
```typescript
// Register inline completion provider
vscode.languages.registerInlineCompletionItemProvider('*', {
  provideInlineCompletionItems: async (document, position) => {
    // Get context and generate suggestions
    const suggestions = await generateSuggestions(document, position);
    return suggestions.map(s => new vscode.InlineCompletionItem(s));
  }
});
```

---

### "I want a sidebar panel/webview"
**Relevant Samples**:
- `webview-sample` - Creating webview panels
- `webview-view-sample` - Sidebar integration
- `tree-view-sample` - Tree structure UI

**Quick Pattern**:
```typescript
// Create webview panel in sidebar
const panel = vscode.window.createWebviewPanel(
  'myViewType',
  'My View',
  vscode.ViewColumn.Beside,
  { enableScripts: true }
);

panel.webview.html = getWebviewContent();

panel.webview.onDidReceiveMessage((message) => {
  // Handle messages from webview
  if (message.command === 'alert') {
    vscode.window.showInformationMessage(message.text);
  }
});
```

---

### "I want to analyze code and provide insights"
**Relevant Samples**:
- `lsp-sample` - Language server setup
- `semantic-tokens-sample` - Code understanding
- `codelens-sample` - Inline code insights

**Quick Pattern**:
```typescript
// Register code lens provider
vscode.languages.registerCodeLensProvider('typescript', {
  provideCodeLenses: (document) => {
    const lenses: vscode.CodeLens[] = [];
    // Analyze document and create code lenses
    return lenses;
  }
});
```

---

### "I want custom UI with commands"
**Relevant Samples**:
- `statusbar-sample` - Status bar items
- `quickinput-sample` - User input dialogs
- `notifications-sample` - Messages and notifications

**Quick Pattern**:
```typescript
// Create status bar item
const statusBar = vscode.window.createStatusBarItem(
  vscode.StatusBarAlignment.Right,
  100
);
statusBar.command = 'my-extension.someCommand';
statusBar.text = '$(loading~spin) Processing...';
statusBar.show();

// Show quick pick
const selection = await vscode.window.showQuickPick(
  ['Option 1', 'Option 2'],
  { placeHolder: 'Choose one' }
);
```

---

## 🔑 Key APIs by Category

### Extension Lifecycle
```typescript
export function activate(context: vscode.ExtensionContext)  // Runs on extension load
export function deactivate()                               // Runs on unload

context.subscriptions.push()                               // Register disposables
context.workspaceState.update(key, value)                 // Persistent workspace storage
context.globalState.update(key, value)                    // Persistent global storage
```

### Commands
```typescript
vscode.commands.registerCommand('id', () => {})           // Register command
await vscode.commands.executeCommand('id', args)          // Execute command
vscode.commands.getCommands()                             // List all commands
```

### Editor & Selection
```typescript
vscode.window.activeTextEditor                            // Current editor
vscode.window.activeTextEditor.selection                  // User selection
vscode.window.activeTextEditor.edit((edit) => {           // Edit document
  edit.insert(position, text);
});
vscode.workspace.openTextDocument(uri)                    // Open file
```

### Chat & Language Model
```typescript
vscode.chat.createChatParticipant('id', handler)         // Chat participant
await request.model.sendRequest(messages, {}, token)     // Query LM
vscode.lm.selectChatModels()                             // Select model
```

### UI Elements
```typescript
vscode.window.createWebviewPanel()                        // Create webview
vscode.window.createStatusBarItem()                       // Status bar
vscode.window.showInformationMessage()                    // Message dialog
vscode.window.showQuickPick()                             // Quick select
vscode.window.showOpenDialog()                            // File picker
```

### File System
```typescript
vscode.workspace.findFiles(pattern)                       // Find files
vscode.workspace.getWorkspaceFolder(uri)                  // Get workspace
vscode.workspace.onDidChangeTextDocument                  // File changed event
vscode.workspace.onDidSaveTextDocument                    // File saved event
```

### Events & Listeners
```typescript
vscode.window.onDidChangeActiveTextEditor                 // Editor switched
vscode.window.onDidChangeTextEditorSelection              // Selection changed
vscode.workspace.onDidOpenTextDocument                    // File opened
vscode.workspace.onDidChangeConfiguration                 // Settings changed

// Always add to disposables when subscribing
context.subscriptions.push(event.onX(() => {}))
```

---

## 🏗️ Project Structure Template

Create this structure for each new module:

```
module-name/
├── src/
│   ├── index.ts                  # Main exports
│   ├── types.ts                  # Interfaces/types
│   └── implementation.ts         # Core logic
├── tests/
│   ├── unit.test.ts             # Unit tests
│   └── integration.test.ts       # Integration tests
├── examples/
│   └── usage.ts                 # Usage example
├── README.md                     # Module docs
└── package.json
```

---

## 🧪 Testing Templates

### Unit Test
```typescript
import { expect } from 'chai';
import * as mocha from 'mocha';

describe('MyModule', () => {
  it('should do something', () => {
    const result = myFunction('input');
    expect(result).to.equal('expected');
  });

  it('should handle errors', () => {
    expect(() => myFunction(null)).to.throw();
  });
});
```

### Integration Test
```typescript
import * as vscode from 'vscode';
import { expect } from 'chai';

suite('Extension Integration', () => {
  test('should activate', async () => {
    const ext = vscode.extensions.getExtension('my-publisher.my-ext');
    await ext?.activate();
    expect(ext?.isActive).to.be.true;
  });

  test('should register command', async () => {
    const commands = await vscode.commands.getCommands();
    expect(commands).to.include('my-extension.myCommand');
  });
});
```

---

## ⚡ Common Patterns

### Error Handling
```typescript
try {
  const result = await risky();
  return result;
} catch (error) {
  vscode.window.showErrorMessage(`Error: ${error}`);
  console.error('Detailed error:', error);
  return null;
}
```

### Resource Cleanup (Disposables)
```typescript
class MyExtension {
  private disposables: vscode.Disposable[] = [];

  activate() {
    // Register all
    this.disposables.push(
      vscode.commands.registerCommand('cmd', () => {}),
      vscode.window.onDidChangeActiveTextEditor(() => {})
    );
  }

  deactivate() {
    // Clean up all
    this.disposables.forEach(d => d.dispose());
  }
}
```

### Message Passing (Webview ↔ Extension)
```typescript
// From extension to webview
panel.webview.postMessage({ command: 'update', data: newData });

// From webview to extension
panel.webview.onDidReceiveMessage((message) => {
  switch (message.command) {
    case 'update':
      handleUpdate(message.data);
      break;
  }
});
```

### Async Operations with Progress
```typescript
vscode.window.withProgress(
  { location: vscode.ProgressLocation.Notification, title: 'Processing...' },
  async (progress) => {
    progress.report({ increment: 0 });
    const result = await doWork();
    progress.report({ increment: 100 });
    return result;
  }
);
```

---

## 🔄 Development Checklist - Module Creation

Before submitting a module:

- [ ] **Code Quality**
  - [ ] TypeScript strict mode enabled
  - [ ] All types defined
  - [ ] No `any` types
  - [ ] ESLint passes
  - [ ] Prettier formatted

- [ ] **Testing**
  - [ ] Unit tests written (80%+ coverage)
  - [ ] Integration tests pass
  - [ ] E2E scenario tested
  - [ ] Error cases covered

- [ ] **Documentation**
  - [ ] README.md with usage
  - [ ] API documented with JSDoc
  - [ ] Examples provided
  - [ ] Known issues listed

- [ ] **Performance**
  - [ ] No memory leaks (disposables cleanup)
  - [ ] Response time < threshold
  - [ ] CPU usage monitored
  - [ ] Concurrent requests handled

- [ ] **Security**
  - [ ] Input validated
  - [ ] Output sanitized
  - [ ] No secrets in code
  - [ ] No unsafe operations

---

## 🆘 Troubleshooting Quick Tips

| Problem | Solution |
|---------|----------|
| "Extension not activating" | Check `activationEvents` in package.json |
| "Command not found" | Verify registered with `vscode.commands.registerCommand()` |
| "Webview is blank" | Check webview HTML path and check browser console for errors |
| "Memory leak" | Ensure all subscriptions added to `context.subscriptions` |
| "Slow response" | Add performance .mark() calls, check for sync operations |
| "Type errors" | Run `tsc --noEmit`, enable strict mode in tsconfig.json |

---

## 📋 File Locations - Samples to Study

### Getting Started
```
vscode-extension-samples/helloworld-sample/
vscode-extension-samples/helloworld-test-sample/
```

### Chat Integration
```
vscode-extension-samples/chat-sample/
vscode-extension-samples/chat-model-provider-sample/
vscode-extension-samples/lm-api-tutorial/
```

### UI Components
```
vscode-extension-samples/webview-sample/
vscode-extension-samples/statusbar-sample/
vscode-extension-samples/tree-view-sample/
```

### Language Features
```
vscode-extension-samples/completions-sample/
vscode-extension-samples/lsp-sample/
vscode-extension-samples/semantic-tokens-sample/
```

### Advanced
```
vscode-extension-samples/vim-sample/
vscode-extension-samples/custom-editor-sample/
vscode-extension-samples/fsprovider-sample/
```

---

## 🚀 One-Minute Module Checklist

**Starting a new module**:
1. Create folder in `CopilotAgentWorkspace/modules/`
2. Copy template structure (src, tests, examples, docs)
3. Create `README.md` with description
4. Initialize `package.json` with typescript dependency
5. Create `tsconfig.json` with strict mode
6. Write first unit test
7. Implement one function
8. Make test pass
9. Repeat 6-8 until feature complete
10. Run full test suite and submit

---

## 📞 VSCode API Resources

- **Official Docs**: https://code.visualstudio.com/api
- **Type Definitions**: `@types/vscode` npm package
- **Examples**: The samples repository (81 examples!)
- **Chat API**: https://code.visualstudio.com/docs/editor/chat
- **LM API**: https://code.visualstudio.com/docs/editor/chat

---

## 💡 Pro Tips

1. **Always push to context.subscriptions** - Prevents memory leaks
2. **Use strict mode** - Catches errors at compile time
3. **Test early, test often** - Makes refactoring safe
4. **Study existing samples** - No need to reinvent patterns
5. **Performance matters** - Profile before optimizing
6. **Error handling first** - Better failures than mysterious hangs
7. **Document as you go** - Future you will thank you
8. **Keep modules small** - Easier to test and maintain

---

*Quick Reference - VSCode Copilot API Integration Project*  
*April 11, 2026*
