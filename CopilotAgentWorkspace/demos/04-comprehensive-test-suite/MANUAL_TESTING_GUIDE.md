# Manual Testing Guide

> Step-by-step instructions for testing Copilot examples in real VSCode

---

## Prerequisites

Before starting, ensure you have:

- ✅ VSCode >= 1.100.0 installed
- ✅ Node.js >= 18.0.0
- ✅ GitHub Copilot extension installed
- ✅ GitHub Copilot subscription (for LM features)
- ✅ vscode-extension-samples cloned in this workspace

---

## General Testing Workflow

### For Each Example:

```
1. LOAD         → Open example as VSCode extension
2. DEBUG        → Start debugging (F5)
3. ACTIVATE     → Verify extension activates
4. LIST         → Check chat participants available
5. TEST         → Try primary feature
6. VERIFY       → Check results are correct
7. DOCUMENT     → Record findings
```

---

## Example 1: chat-tutorial (Simplest)

### Setup

```bash
# Navigate to example directory
cd vscode-extension-samples/chat-tutorial

# Verify structure
ls src/extension.ts      # Should exist
cat package.json          # Should have activationEvents
```

### Load in VSCode

```bash
# Open extension in debug mode
code --extensionDevelopmentPath=./vscode-extension-samples/chat-tutorial

# Or if in VSCode:
# File > Open Folder -> select vscode-extension-samples/chat-tutorial
# Press Ctrl+Shift+D (Debug view)
# Click "Run Extension"
```

### Test Checklist

- [ ] VSCode opens new window with extension
- [ ] No errors in Debug Console
- [ ] No errors in Extension Host log
- [ ] Extension activates (check console output)

### Test Chat Participant

1. **Open Copilot Chat**
   - Press: `Cmd+Shift+L` (macOS) or `Ctrl+Shift+L` (Windows/Linux)
   - Chat view opens on right side

2. **Look for @tutor**
   - Type: `@`
   - Dropdown appears with available participants
   - You should see: `@tutor`

3. **Send Simple Message**
   - Type: `@tutor hello`
   - Press Enter
   - Response should appear

4. **Test /exercise Command**
   - Type: `@tutor /exercise`
   - Press Enter
   - Should generate a coding exercise

### Verify Results

✅ **If working:**
```
@tutor appears in participant list
Messages get responses
/exercise generates exercises
No errors in console
```

❌ **If not working:**
- Check Debug Console for errors
- Look for activation errors
- Verify vscode API calls in code

### Document Findings

Create file: `manual-tests/chat-tutorial-results.md`

```markdown
# Chat Tutorial - Manual Test Results

Date: April 11, 2026
VSCode Version: 1.100.0
Node Version: 18.0.0
Status: ✅ PASSED / ❌ FAILED

## Checks Performed

- [x] Extension loaded without errors
- [x] @tutor participant appears
- [x] Basic message generates response
- [x] /exercise command works
- [x] No console errors

## Issues Found
(none) / (list any issues)

## Notes
(any additional observations)
```

---

## Example 2: chat-sample (Most Complete)

### Setup

```bash
cd vscode-extension-samples/chat-sample
npm install  # Important: install dependencies
```

### Load in VSCode

```bash
code --extensionDevelopmentPath=./vscode-extension-samples/chat-sample
# Press F5 to debug
```

### Test Checklist

- [ ] Extension loads without errors
- [ ] Multiple participants appear (@cat, @catTools, @tool)
- [ ] Each participant responds to queries
- [ ] Tools are available (if using @tool)
- [ ] No errors in Extension Host

### Test Participants

#### Participant 1: @cat (Simple)
```
1. Type: @cat what is javascript?
2. Should: Receive response about JavaScript
3. Verify: Response is educational and clear
```

#### Participant 2: @catTools (With Utilities)
```
1. Type: @catTools list files in current directory
2. Should: Use tools to find files
3. Verify: Tool execution works
```

#### Participant 3: @tool (Advanced)
```
1. Type: @tool count lines in this file
2. Should: Use tools to analyze code
3. Verify: Complex tool interactions work
```

### Document Findings

```markdown
# Chat Sample - Manual Test Results

Status: ✅ PASSED / ❌ FAILED

## Participants Tested
- [x] @cat
- [x] @catTools
- [x] @tool

## Tools Verified
- [x] Tab count
- [x] Find files
- [x] Run in terminal

## Issues
(none found)
```

---

## Example 3: lm-api-tutorial

### Setup

```bash
cd vscode-extension-samples/lm-api-tutorial
npm install
```

### Load in VSCode

```bash
code --extensionDevelopmentPath=./vscode-extension-samples/lm-api-tutorial
# Press F5
```

### Test Checklist

- [ ] Extension loads
- [ ] "Toggle Tutor Annotations" command appears
- [ ] Command is executable
- [ ] Annotations appear in editor
- [ ] No errors

### Test Execution

```
1. Open a code file (JavaScript/Python/etc)
2. Run Command: "Toggle Tutor Annotations" (Cmd+Shift+P -> type command)
3. Verify: Inline annotations appear in code
4. Check: Annotations provide helpful hints
5. Run again: Toggles annotations off
```

### Verify Results

- Annotations appear
- Information is relevant
- No performance issues
- Toggle works

---

## Example 4: chat-context-sample

### Setup

```bash
cd vscode-extension-samples/chat-context-sample
npm install
```

### Load & Test

```bash
code --extensionDevelopmentPath=./vscode-extension-samples/chat-context-sample
```

### Test Checklist

- [ ] Extension loads
- [ ] Open a JSON file
- [ ] Open Chat
- [ ] Context for JSON file appears
- [ ] Line count information shown

### Verify

```
1. Create test.json file with content
2. Ask @copilot "tell me about test.json"
3. Verify: Context is used in response
4. Check: Line count is accurate
```

---

## Example 5: chat-model-provider-sample

### Setup

```bash
cd vscode-extension-samples/chat-model-provider-sample
npm install
```

### Load & Test

```bash
code --extensionDevelopmentPath=./vscode-extension-samples/chat-model-provider-sample
```

### Test Checklist

- [ ] Extension loads
- [ ] Custom models appear in model selector
- [ ] Can switch to custom model
- [ ] Model responds to queries
- [ ] Responses match model type (Dog/Cat themed)

---

## Example 6: chat-output-renderer-sample

### Setup

```bash
cd vscode-extension-samples/chat-output-renderer-sample
npm install
```

### Load & Test

- [ ] Extension loads
- [ ] Custom rendering works
- [ ] Output formatting is correct
- [ ] Webview renders properly

---

## Example 7: mcp-extension-sample

### Setup

```bash
cd vscode-extension-samples/mcp-extension-sample
npm install
```

### Load & Test

- [ ] Extension loads  
- [ ] "Add Gist Source" command available
- [ ] Can load MCP servers from gist
- [ ] Tools from MCP servers work in chat

---

## Troubleshooting

### Extension Won't Load

```
Symptoms: "Extension failed to activate" or similar error

Solutions:
1. Check Debug Console for specific errors
2. Delete node_modules and reinstall: rm -rf node_modules && npm install
3. Verify VSCode version: code --version
4. Restart VSCode
5. Check vscode dependency in package.json matchess your version
```

### No Participants Appear

```
Symptoms: @participant doesn't appear in chat

Solutions:
1. Extension must activate first (check console)
2. Verify extension registered participant correctly
3. Reload VSCode window (Cmd+R)
4. Check Debug Console for registration errors
5. Verify engine versions in package.json
```

### Chat Doesn't Respond

```
Symptoms: Messages sent but no response

Solutions:
1. Verify GitHub Copilot is installed
2. Check Copilot subscription is active
3. Open Debug Console to see errors
4. Check Extension Host log
5. Try simple message first: "hello"
```

### Performance Issues

```
Symptoms: Slow responses, UI lag

Solutions:
1. Open fewer files
2. Disable other extensions
3. Check CPU usage in Activity Monitor
4. Restart VSCode
5. Check Extension Host performance
```

---

## Recording Results

For each example tested, create a results file:

```markdown
# [Example Name] - Manual Test Results

**Date:** April 11, 2026
**Tester:** Your Name
**VSCode Version:** 1.100.0
**Status:** ✅ WORKING / ⚠️ PARTIAL / ❌ BROKEN

## Checklist
- [ ] Extension loads
- [ ] Participants appear
- [ ] Primary feature works
- [ ] No console errors
- [ ] Performance acceptable

## Test Scenarios

### Scenario 1: Basic Usage
```
Steps:
1. [description]
Result: [description]
Status: ✅ PASS / ❌ FAIL
```

### Scenario 2: [Other test]
```
Steps: ...
Result: ...
Status: ...
```

## Issues Found

1. **Issue Title**
   - Description: ...
   - Severity: Critical/High/Medium/Low
   - Workaround: ...

## Recommendations

- [Any observations or improvements]

## Sign-off

- Tester: [Your Name]
- Date: [Date]
- Approved: [Yes/No]
```

---

## Automated Test After Manual Verification

Once manual testing passes, run automated tests:

```bash
cd ..
npm run test:integration -- --example=chat-tutorial
npm run test:integration -- --verbose
```

---

## Common Commands Quick Reference

```bash
# Load extension in debug mode
code --extensionDevelopmentPath=./path/to/example

# Start debugging (in VSCode)
F5 or Run > Start Debugging

# Reload extension window
Cmd+R (reload)

# Open Copilot Chat
Cmd+Shift+L

# Toggle Debug Console
Cmd+J

# Install dependencies
npm install

# Run automated tests
npm run test:integration

# Show all participants
 (type @ in chat)
```

---

## Next Steps

1. Complete manual tests for each example
2. Record results in result files
3. Run automated test suite
4. Compare manual vs automated results
5. Document any discrepancies
6. Fix issues found
7. Verify tests pass end-to-end

---

**Testing begins:** [timestamp]  
**Target completion:** All 7 examples manually tested within 24 hours
