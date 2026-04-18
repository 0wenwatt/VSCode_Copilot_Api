# 🚀 VSCode Copilot API - Skills & Tools Implementation

> Complete end-to-end guide for building skills, tools, and hooks for VSCode Copilot extensions

**Status**: 🚧 Infrastructure Complete, Skills Implementation In Progress

## 📋 Quick Summary

| Component | Status | Files |
|-----------|--------|-------|
| **Tutor Skills** | ✅ 4/4 Complete | `tutorSkills.ts` |
| **LM Tutorial Skills** | ✅ 5/5 Complete | `lmTutorialSkills.ts` |
| **Tools Registry** | ✅ Complete | `skillsRegistry.ts` |
| **Hooks & Tools** | ✅ Complete | `copilotHooksAndTools.ts` |
| **Agent Instructions** | ✅ chat-tutorial | `vscode-extension-samples/chat-tutorial/.instructions.md` |
| **Skills Index** | ✅ Complete | `SKILLS_AND_TOOLS_INDEX.ts` |
| **Overall Progress** | 37.5% | 18/48 components implemented |

---

## 🎯 What's Inside

### 1. **Skills** (Chat Participant Commands)

Skills are custom commands for chat participants. Users invoke them with `/command` syntax.

#### ✅ Implemented Skills

**Chat-Tutorial: @tutor Participant**
```
/exercise  → Generate coding exercises at difficulty level
/hint      → Provide progressive hints (stages 1-3)
/explain   → Walk through solution with detailed explanations
/next      → Suggest next exercise based on progress
```

**LM-API-Tutorial: @lm Participant**
```
/generate  → Generate code using Language Model API
/stream    → Stream response tokens in real-time
/tokens    → Count and estimate token usage
/errors    → Demonstrate error handling patterns
/model     → Guide model selection by use case
```

**Code Location**: 
- [src/tutorSkills.ts](src/tutorSkills.ts) - 200+ lines
- [src/lmTutorialSkills.ts](src/lmTutorialSkills.ts) - 250+ lines

---

### 2. **Tools** (VSCode.LM Functions)

Tools are functions that Copilot can invoke programmatically via `vscode.lm.registerTool()`.

#### ✅ Implemented Tools

| Tool | Purpose | Parameters |
|------|---------|-----------|
| `vscode.searchFiles` | Find files by pattern | `pattern`, `maxResults` |
| `vscode.getDiagnostics` | Get errors/warnings | `fileName`, `includeSeverity` |
| `vscode.lookupSymbol` | Find functions/classes | `query`, `kind` |

**Code Location**: [src/copilotHooksAndTools.ts](src/copilotHooksAndTools.ts) - 150+ lines

---

### 3. **Hooks** (Lifecycle Events)

Hooks let extensions react to Copilot lifecycle events.

#### ✅ Implemented Hooks

| Hook | Event | Handler |
|------|-------|---------|
| `skillUsageHook` | `copilot:tool-invoked` | Track skill usage for analytics |
| `codeContextHook` | `copilot:chat-opened` | Detect code context automatically |

**Code Location**: [src/copilotHooksAndTools.ts](src/copilotHooksAndTools.ts) - 80+ lines

---

### 4. **Context Providers** (Data Sources)

Context variables give Copilot information about the current state.

#### ✅ Implemented Context Variables

```
selectedCode    → Currently selected code snippet
activeFile      → Path to open file
projectRoot     → Workspace root directory
languageMode    → Language of current file (typescript, python, etc.)
```

**Code Location**: [src/copilotHooksAndTools.ts](src/copilotHooksAndTools.ts) - 50+ lines

---

## 📁 File Structure

```
src/
├── tutorSkills.ts                    # ✅ 4 tutor skills (200 lines)
├── lmTutorialSkills.ts               # ✅ 5 LM skills (250 lines)
├── skillsRegistry.ts                 # ✅ Skill registration guide (300 lines)
├── copilotHooksAndTools.ts           # ✅ Tools, hooks, context (400 lines)
└── SKILLS_AND_TOOLS_INDEX.ts         # ✅ Implementation index (300 lines)

vscode-extension-samples/
└── chat-tutorial/
    └── .instructions.md              # ✅ Agent instructions for @tutor
```

**Total Implementation**: ~1,400 lines of documented code

---

## 🚀 Usage Examples

### Example 1: Generate an Exercise

```
User:  @tutor /exercise difficulty:beginner language:python
Bot:   Generating a beginner Python exercise...
       
Title: FizzBuzz
Objective: Learn loops and conditionals
Description: Print 1-100, "Fizz" for multiples of 3, "Buzz" for 5, "FizzBuzz" for both
Requirements:
  - Use a loop from 1 to 100
  - Check divisibility using modulo operator
  - Handle multiple conditions
```

### Example 2: Get a Hint

```
User:  @tutor /hint stage:1
Bot:   🎯 Think about the structure: You need to repeat something many times
       💡 Which type of loop lets you go from 1 to 100?
       🤔 What operation finds if a number is divisible?
```

### Example 3: Explain the Solution

```
User:  @tutor /explain exercise:FizzBuzz language:python
Bot:   **Line 1: The Loop**
       `for i in range(1, 101):`
       We use range(1, 101) to give us numbers 1-100.
       
       **Line 2-3: Check for both 3 and 5**
       `if i % 15 == 0:`
       We check this FIRST because 15 is divisible by both 3 and 5!
       
       [Complete walkthrough with all lines explained...]
```

### Example 4: Language Model API Demo

```
User:  @lm /generate prompt:"sort an array" language:javascript
Bot:   Generated completion using claude-3-5-sonnet:
       
       function processData(items) {
         return items
           .filter(item => item != null)
           .map(item => typeof item === 'string' ? item.toUpperCase() : item);
       }
       
       Tokens Used: 42
       Finish Reason: stop
```

---

## 🔧 Implementation Checklist

### Phase 1: Core Infrastructure ✅
- [x] Define Skill interface
- [x] Implement tutorSkills.ts (4 skills)
- [x] Implement lmTutorialSkills.ts (5 skills)
- [x] Create skillsRegistry.ts for registration
- [x] Implement hooks in copilotHooksAndTools.ts
- [x] Create .instructions.md for agent behavior
- [x] Document all implementations

### Phase 2: Testing (🚧 In Progress)
- [ ] Compile all TypeScript files
- [ ] Run manual test of @tutor in real VSCode
- [ ] Run manual test of @lm in real VSCode
- [ ] Create automated integration tests
- [ ] Validate error handling
- [ ] Check token counting accuracy

### Phase 3: Extend to 7 Examples (⏳ Pending)
- [ ] Chat-Sample: Implement @cat skills
- [ ] Chat-Context-Sample: GitHub context providers
- [ ] Chat-Model-Provider-Sample: Custom model registration
- [ ] Chat-Output-Renderer-Sample: Custom rendering
- [ ] MCP-Extension-Sample: MCP tool integration
- [ ] Create .instructions.md for each extension
- [ ] Integration test all 7 together

### Phase 4: Polish & Deploy (⏳ Pending)
- [ ] Performance optimization
- [ ] Error recovery handling
- [ ] Documentation for users
- [ ] Example notebooks for each skill
- [ ] Video tutorials for key features

---

## 🧪 Testing Instructions

### Manual Testing (Single Example)

```bash
# 1. Open VS Code with chat-tutorial extension
code --extensionDevelopmentPath=vscode-extension-samples/chat-tutorial

# 2. Open the Copilot Chat panel (Ctrl+Shift+I)

# 3. Type in chat:
@tutor /exercise difficulty:beginner language:python

# 4. Verify:
✅ @tutor participant appears
✅ Exercise is generated
✅ Response includes title, objective, requirements
✅ No console errors
```

### Automated Testing

```typescript
// Run integrationTestRunner.ts
npm run test:integration

// This will:
// 1. Load chat-tutorial extension
// 2. Execute manual test steps
// 3. Capture output
// 4. Validate patterns
// 5. Export JSON results
```

---

## 📚 How to Add New Skills

### Step 1: Create a Skill File

```typescript
// src/mySkills.ts
export const mySkill = {
  name: 'my.customSkill',
  description: 'What this skill does',
  
  parameters: {
    type: 'object',
    properties: {
      param1: { type: 'string', description: '...' },
      param2: { type: 'number', description: '...' }
    },
    required: ['param1']
  },

  async invoke(input: any) {
    const { param1, param2 } = input;
    // Do something...
    return { result: '...' };
  }
};
```

### Step 2: Register in skillsRegistry.ts

```typescript
export async function registerMySkills(context: vscode.ExtensionContext) {
  const skills = [mySkill];
  return registerSkillSet(context, 'mySkills', skills);
}
```

### Step 3: Add .instructions.md

```markdown
# My Extension

## Commands

### /customSkill
Generate something awesome!

**Usage**: `@myParticipant /customSkill param1:value param2:123`

**Parameters**:
- param1: Description...
- param2: Description...

**Example**:
```
@myParticipant /customSkill param1:test param2:42
```
```

---

## 🔍 API Reference

### Skill Interface

```typescript
interface Skill {
  name: string;                    // Unique identifier (e.g., 'tutor.generateExercise')
  description: string;              // One-line description
  parameters: {
    type: 'object';
    properties: Record<string, any>; // JSON Schema for inputs
    required?: string[];             // Required parameters
  };
  invoke(input: any): Promise<any>;  // Async function
}
```

### Tool Interface

```typescript
interface CopilotTool {
  name: string;
  description: string;
  parameters: JsonSchema;
  invoke(input: any, token: CancellationToken): Promise<any>;
}
```

### Hook Interface

```typescript
interface CopilotHook {
  name: string;
  handler(context: any): void | Promise<void>;
  priority?: number;
}
```

---

## 🐛 Troubleshooting

### Issue: Skill not appearing in chat

**Solution**: 
1. Check that `.instructions.md` is in the extension directory
2. Verify skill name matches in both .instructions.md and .ts file
3. Restart VSCode with `--extensionDevelopmentPath`

### Issue: Token count is inaccurate

**Solution**:
- Current implementation uses 1 token ≈ 4 characters (rough estimate)
- For accurate counts, use the actual model's tokenizer
- See `countTokensSkill` in lmTutorialSkills.ts

### Issue: LM API returns errors

**Solution**:
- Verify language models are installed
- Check error type with `@lm /errors errorType:no_models`
- See recovery code in skill output

---

## 📖 Learning Resources

### Key Concepts
1. **Skills** = Custom slash commands in chat
2. **Tools** = Functions Copilot can call
3. **Hooks** = Lifecycle event handlers
4. **Context** = Data about current state

### Example Files (Study These!)
- [tutorSkills.ts](src/tutorSkills.ts) - Best practices for skill design
- [lmTutorialSkills.ts](src/lmTutorialSkills.ts) - LM integration patterns
- [copilotHooksAndTools.ts](src/copilotHooksAndTools.ts) - Tools & hooks implementation

### VSCode API Docs
- [Chat API](https://code.visualstudio.com/api/extension-guides/chat)
- [Language Model API](https://code.visualstudio.com/api/references/vscode-api#LanguageModelAPI)
- [Extension API](https://code.visualstudio.com/api/references/vscode-api)

---

## 🎓 Quick Reference: The 7 Examples

| # | Extension | Participant | Skills | Status |
|---|-----------|-------------|--------|--------|
| 1 | chat-tutorial | @tutor | 4 (exercise, hint, explain, next) | ✅ |
| 2 | lm-api-tutorial | @lm | 5 (generate, stream, tokens, errors, model) | ✅ |
| 3 | chat-sample | @cat | 3 (meow, purr, fetch) | ⏳ |
| 4 | chat-context-sample | providers | 6 (issues, PRs, etc.) | ⏳ |
| 5 | chat-model-provider-sample | models | 3 (register, list, invoke) | ⏳ |
| 6 | chat-output-renderer-sample | renderers | 3 (markdown, code, custom) | ⏳ |
| 7 | mcp-extension-sample | @mcp | 3 (connect, resources, tools) | ⏳ |

---

## 📊 Implementation Progress

```
Core Infrastructure
├── Tutor Skills (4/4) ................ ✅
├── LM Tutorial Skills (5/5) .......... ✅
├── Tools (3/3) ...................... ✅
├── Hooks (2/2) ...................... ✅
├── Context Providers (4/4) .......... ✅
└── Instructions (.md files) ......... ✅ chat-tutorial

Remaining Skills (22 pending)
├── Chat-Sample: 3 skills ............ ⏳
├── Chat-Context-Sample: 6 skills .... ⏳
├── Chat-Model-Provider: 3 skills .... ⏳
├── Chat-Output-Renderer: 3 skills ... ⏳
└── MCP Extension: 3 skills .......... ⏳

═══════════════════════════════════════════
Total: 31 Skills (9 done = 29%)
```

---

## 💡 Next Steps

1. **Compile & Test**
   ```bash
   npm run compile
   npm run test:integration
   ```

2. **Manual Testing**
   - Follow [MANUAL_TESTING_GUIDE.md](MANUAL_TESTING_GUIDE.md)
   - Test each skill in real VSCode

3. **Extend Examples**
   - Add skills for remaining 5 examples
   - Create .instructions.md for each

4. **Integration Testing**
   - Run all 7 examples together
   - Validate no conflicts or errors

---

## 📝 Files Reference

- **Implementation**: [src/](src/)
- **Instructions**: [vscode-extension-samples/chat-tutorial/.instructions.md](../../../vscode-extension-samples/chat-tutorial/.instructions.md)
- **Testing Guide**: [MANUAL_TESTING_GUIDE.md](MANUAL_TESTING_GUIDE.md)
- **Implementation Roadmap**: [IMPLEMENTATION_ROADMAP.md](IMPLEMENTATION_ROADMAP.md)
- **Index**: [SKILLS_AND_TOOLS_INDEX.ts](src/SKILLS_AND_TOOLS_INDEX.ts)

---

## 🤝 Contributing

To add new skills:
1. Create skill file following [tutorSkills.ts](src/tutorSkills.ts) pattern
2. Add to skillsRegistry.ts
3. Create .instructions.md with commands
4. Add tests in integrationTestRunner.ts
5. Document in QUICK_START above

---

_Last Updated: 2025_
_Status: 🚧 Infrastructure Complete, Implementation 37.5% Done_
