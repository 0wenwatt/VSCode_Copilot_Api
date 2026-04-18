# Demo 01: Context Window Access

**Goal:** Learn how to access and read Copilot's context window to understand what information is available.

## What This Demo Shows

- ✅ Reading active editor information (file name, language, line count)
- ✅ Capturing cursor position and selection
- ✅ Accessing workspace information
- ✅ Listing all open editors
- ✅ Writing context snapshots to files
- ✅ Generating Markdown output of context

## Commands

Run from VSCode Command Palette (Cmd+Shift+P):

1. **Demo: Read Copilot Context Window**
   - Captures complete context snapshot
   - Writes to `DEMO_CONTEXT_WINDOW_RESULTS.md`
   - Shows all available context information

2. **Demo: Log Active Editor to Context**
   - Logs current editor details
   - Writes to `DEMO_ACTIVE_EDITOR_TEST.json`
   - Useful for testing editor access

3. **Demo: Log Selection to Context**
   - Logs current selection/cursor position
   - Writes to `DEMO_SELECTION_TEST.json`
   - Tests selection capture

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

Then:
- Open any file in the editor
- Open Command Palette (Cmd+Shift+P)
- Type "Demo: Read Copilot Context"
- Check generated `DEMO_CONTEXT_WINDOW_RESULTS.md`

### 3. Verify Output

After running a command, check:

- **`DEMO_CONTEXT_WINDOW_RESULTS.md`** - Full context snapshot in Markdown
- **`DEMO_ACTIVE_EDITOR_TEST.json`** - JSON with editor information
- **`DEMO_SELECTION_TEST.json`** - JSON with selection details
- **Console output** - Live logging of captured context

## What Gets Captured

### Active Editor Context
```json
{
  "fileName": "extension.ts",
  "language": "typescript",
  "lineCount": 42,
  "isDirty": false,
  "cursorLine": 10,
  "cursorCharacter": 5,
  "contentPreview": "import * as vscode"
}
```

### Selection Context
```json
{
  "selectedText": "vscode",
  "selectionStart": { "line": 10, "character": 5 },
  "selectionEnd": { "line": 10, "character": 11 }
}
```

### Workspace Context
```json
{
  "name": "my-workspace",
  "folders": ["src", "test", "dist"],
  "fileCount": 18
}
```

### Open Editors List
```json
[
  { "fileName": "extension.ts", "language": "typescript" },
  { "fileName": "package.json", "language": "json" },
  { "fileName": "README.md", "language": "markdown" }
]
```

## Test Results

Run tests with:
```bash
npm test
```

**Expected output:**
```
✓ PASS - Context snapshot has required structure
✓ PASS - Context can be serialized to JSON
✓ PASS - Markdown output can be generated
✓ PASS - Results can be written to file
✓ PASS - Timestamp is in valid ISO format

📊 Results: 5/5 tests passed
```

## Key VSCode APIs Used

- `vscode.window.activeTextEditor` - Get current editor
- `vscode.window.visibleTextEditors` - Get all open editors
- `vscode.workspace.workspaceFolders` - Get workspace info
- `editor.selection` - Get cursor/selection position
- `document.getText()` - Get file content
- `document.lineCount` - Get line count

## Files Generated

| File | Purpose | Format |
|------|---------|--------|
| `DEMO_CONTEXT_WINDOW_RESULTS.md` | Full context snapshot | Markdown |
| `DEMO_ACTIVE_EDITOR_TEST.json` | Editor details | JSON |
| `DEMO_SELECTION_TEST.json` | Selection/cursor info | JSON |

## Use Cases

- **Debug** - See what context Copilot has access to
- **Test** - Verify editor state capture works correctly
- **Learn** - Understand VSCode's context APIs
- **Integrate** - Build features that leverage editor context

## Notes

- Context is captured at the moment you run the command
- If no editor is active, some fields will be omitted
- File paths are shown relative to workspace root
- All timestamps are in ISO 8601 format

## Next Steps

After understanding context access, explore:
- **Demo 02:** Chat Participants - Create custom chat interactions
- **Demo 03:** Language Model Tools - Register callable tools
- **Demo 04:** MCP Servers - Bridge to external backends

---

*Part of VSCode Copilot API Demos Series*
