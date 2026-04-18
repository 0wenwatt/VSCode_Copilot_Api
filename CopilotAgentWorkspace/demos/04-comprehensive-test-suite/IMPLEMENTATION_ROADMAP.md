# VSCode Copilot Implementation Roadmap

> Implementation guide for all 7 examples with real VSCode testing

**Status:** Starting implementation phase  
**Target:** Fully working examples with agent instructions, skills, and manual verification

---

## Overview

This roadmap provides a step-by-step implementation strategy to:
1. Load each example as a VSCode extension
2. Test manually in VSCode Copilot Chat
3. Add automated integration tests
4. Implement agent instructions & skills
5. Document and verify each feature

---

## What We're Implementing

### The 7 Examples
1. **chat-tutorial** ← Start here (simplest)
2. **chat-sample** (most complete)
3. **lm-api-tutorial**
4. **chat-context-sample**
5. **chat-model-provider-sample**
6. **chat-output-renderer-sample**
7. **mcp-extension-sample** (most complex)

### Key Features to Test
- ✅ **Agent Instructions** - Custom `.instructions.md` files (Copilot behavior)
- ✅ **Skills** - Custom capabilities for Copilot
- ✅ **Hooks** - Integration points with Copilot
- ✅ **Context Providers** - Custom context for chat
- ✅ **Tools** - Callable functions from Copilot
- ✅ **Models** - Custom LM providers
- ✅ **Output Renderers** - Custom chat output formatting

---

## Implementation Strategy

### Phase 1: Setup (Day 1)
- [ ] Create test infrastructure
- [ ] Document VSCode debug workflow
- [ ] Create integration test framework
- [ ] Set up manual testing checklist

### Phase 2: First Example - chat-tutorial (Day 2-3)
- [ ] Load in VSCode debug mode
- [ ] Test manually in Copilot Chat
- [ ] Create automated tests
- [ ] Add agent instructions
- [ ] Verify all features work

### Phase 3: Next Examples (Days 4-7)
- [ ] Repeat for each remaining example
- [ ] Test interactions between examples
- [ ] Document patterns discovered

### Phase 4: Integration & Polish (Days 8-10)
- [ ] Cross-example testing
- [ ] Performance optimization
- [ ] Documentation
- [ ] CI/CD integration

---

## Testing Strategy

### Manual Testing Workflow

**For each example:**

```
1. Open VSCode
2. Load extension: code --extensionDevelopmentPath=./path/to/example
3. Press F5 to debug
4. Open Copilot Chat (Cmd+Shift+L)
5. Try commands/features documented in example
6. Check output
7. Verify in console for errors
```

### Automated Testing Workflow

**Create tests for:**
```typescript
✅ Extension activates
✅ Chat participants register
✅ Commands available
✅ Tools callable
✅ Responses generated
✅ No console errors
```

---

## Implementation Details

### Step 1: Create Integration Test Framework

```typescript
// tests/integrationTestRunner.ts
interface TestCase {
  name: string;
  example: string;
  steps: TestStep[];
  expectedResults: string[];
}

interface TestStep {
  action: string;      // What to do
  expected: string;    // What should happen
  verify: () => boolean;
}
```

### Step 2: Manual Testing Checklist

For each example, verify:
```
[ ] Extension loads without errors
[ ] Chat participant appears in list
[ ] Commands are accessible
[ ] First message generates response
[ ] Tools execute (if applicable)
[ ] No runtime errors in console
[ ] Output formatting looks correct
```

### Step 3: Agent Instructions Setup

Create `.instructions.md` for each example:
```markdown
# Chat Tutorial Agent

## Role
Provides exercise-based coding tutoring

## Capabilities
- Generate coding exercises
- Explain solutions
- Provide hints

## Commands
- `/exercise` - Get a new exercise
- `/hint` - Get a hint for current exercise

## Behavior
- Always provide educational context
- Encourage learning by doing
- Progressively increase difficulty
```

### Step 4: Skills Implementation

Create custom skills for Copilot:
```typescript
vscode.lm.registerTool('tutorSkill.generateExercise', {
  invoke: async (options) => {
    // Generate exercise
  }
});
```

---

## Phase-by-Phase Details

### PHASE 1: Setup Infrastructure

#### 1a. Create Integration Test Runner

**File:** `demos/04-comprehensive-test-suite/src/integrationTestRunner.ts`

Will support:
- Loading VSCode with extension
- Invoking chat participants
- Verifying responses
- Automated manual test steps
- Logging results

#### 1b. Create Manual Testing Guide

**File:** `MANUAL_TESTING_GUIDE.md`

Provides step-by-step instructions for:
- Loading each example
- Testing primary features
- Validation checklist

#### 1c. Create Test Data

Create sample inputs/outputs for each example:
```json
{
  "chat-tutorial": {
    "testCases": [
      {
        "input": "@tutor /exercise",
        "expectedResponse": "Here's your exercise:",
        "expectedType": "exercise"
      }
    ]
  }
}
```

---

### PHASE 2: Implement chat-tutorial

#### 2.1 Manual Testing

1. Navigate to example directory
2. Run: `code --extensionDevelopmentPath=vscode-extension-samples/chat-tutorial`
3. Press F5 to start debugging
4. Open Copilot Chat
5. Type: `@tutor hello`
6. Verify response appears

#### 2.2 Create Automated Tests

```typescript
describe('chat-tutorial', () => {
  it('should register @tutor participant', async () => {
    const extension = await activateExtension('chat-tutorial');
    const participants = extension.participants;
    expect(participants).toContain('tutor');
  });

  it('should respond to basic query', async () => {
    const response = await invokeParticipant('@tutor', 'hello');
    expect(response).toBeTruthy();
  });

  it('should handle /exercise command', async () => {
    const response = await invokeParticipant('@tutor', '/exercise');
    expect(response).toContain('exercise');
  });
});
```

#### 2.3 Add Agent Instructions

**File:** `vscode-extension-samples/chat-tutorial/.instructions.md`

```markdown
# @tutor Agent

Educational tutoring assistant that provides coding exercises and explanations.

## Role
Help users learn programming concepts through guided exercises.

## Commands
- `/exercise` - Generate a new programming exercise
- `/hint` - Get a hint for the current exercise
- Default: Answer questions about the exercise

## Behavior
- Provide exercises at an appropriate difficulty level
- Give hints that guide without spoiling the answer
- Explain concepts clearly with examples
- Encourage learning by doing
```

#### 2.4 Create Skills

```typescript
// Skill: Generate exercises
vscode.lm.registerTool('tutorSkill.generateExercise', {
  invoke: async (options, token) => {
    // Call LM to generate exercise
  }
});

// Skill: Provide hints
vscode.lm.registerTool('tutorSkill.provideHint', {
  invoke: async (options, token) => {
    // Provide educational hint
  }
});
```

#### 2.5 Verification

- ✅ Extension loads
- ✅ @tutor appears in chat
- ✅ /exercise command works
- ✅ Responses are educational
- ✅ No console errors

---

### PHASE 3: Implement Remaining Examples

#### Implementation Order (by complexity)

```
1. chat-tutorial        ← Simple participant
2. lm-api-tutorial      ← Direct LM API
3. chat-context-sample  ← Context providers
4. chat-sample          ← Full-featured
5. chat-model-provider  ← Custom models
6. output-renderer      ← Custom rendering
7. mcp-extension        ← MCP integration (hardest)
```

#### For Each Example:

1. **Manual Test** (10 mins)
   - Load in VSCode
   - Test primary feature
   - Check console

2. **Create Tests** (20 mins)
   - Write integration tests
   - Document expected behavior
   - Add to test suite

3. **Add Instructions** (10 mins)
   - Create `.instructions.md`
   - Define role & capabilities
   - Document behaviors

4. **Implement Skills** (20 mins)
   - Register tools with `vscode.lm.registerTool()`
   - Add skill descriptions
   - Test execution

5. **Document** (10 mins)
   - Update README
   - Add test coverage report
   - Record results

---

## Testing Tools & Commands

### Manual Test Commands

```bash
# Load example in debug mode
code --extensionDevelopmentPath=vscode-extension-samples/chat-tutorial

# Run integration tests
npm run test:integration

# Run specific example tests
npm run test:integration -- --example chat-tutorial

# Run with verbose logging
npm run test:integration -- --verbose

# Run manual test checklist
npm run manual-test -- --example chat-tutorial
```

### Automated Test Framework

```typescript
class IntegrationTestRunner {
  async loadExtension(exampleName: string): Promise<Extension>;
  async invokeParticipant(name: string, input: string): Promise<string>;
  async invokeSkill(skillName: string, args: any): Promise<any>;
  async captureConsoleOutput(): Promise<string[]>;
  async captureErrors(): Promise<Error[]>;
}
```

---

## File Structure for Implementation

```
CopilotAgentWorkspace/
├── demos/
│   └── 04-comprehensive-test-suite/
│       ├── src/
│       │   ├── realCodeAnalysis.ts
│       │   ├── testHarness.ts
│       │   └── integrationTestRunner.ts      ← NEW
│       ├── tests/
│       │   ├── chat-tutorial.test.ts         ← NEW
│       │   ├── chat-sample.test.ts           ← NEW
│       │   └── shared.test.ts                ← NEW
│       ├── manual-tests/
│       │   ├── MANUAL_TESTING_GUIDE.md       ← NEW
│       │   └── checklists/
│       │       └── chat-tutorial.md          ← NEW
│       └── results/
│           ├── manual-test-results/
│           ├── automated-test-results/
│           └── integration-report.md
├── instructions/
│   ├── chat-tutorial.instructions.md         ← NEW
│   ├── chat-sample.instructions.md
│   └── README.md
└── skills/
    ├── tutor.skill.ts                        ← NEW
    ├── chat.skill.ts
    └── README.md
```

---

## Success Criteria

For each example to be considered "done":

- ✅ Loads without errors in VSCode
- ✅ Manual test checklist passes
- ✅ Automated tests pass 100%
- ✅ Agent instructions provided
- ✅ 2+ skills implemented and tested
- ✅ Documentation complete
- ✅ CI/CD integration working
- ✅ No console errors or warnings

---

## Timeline

| Phase | Task | Timeline |
|-------|------|----------|
| **1** | Setup infrastructure | 2 hours |
| **2** | Implement chat-tutorial | 3 hours |
| **3a** | Implement lm-api-tutorial | 2 hours |
| **3b** | Implement chat-context-sample | 2 hours |
| **3c** | Implement chat-sample | 3 hours |
| **3d** | Implement remaining 3 | 6 hours |
| **4** | Integration & polish | 4 hours |
| **Total** | | ~22 hours |

---

## Risk Mitigation

### Known Risks

1. **VSCode not installed** → Use VS Code Server as fallback
2. **No GitHub Copilot** → Mock LM responses for testing
3. **Extension conflicts** → Test in clean workspace
4. **API changes** → Document versions used
5. **Performance issues** → Add performance benchmarks

### Mitigations

1. Docker-based test environment
2. Mock LM API for tests
3. Isolated test workspaces
4. Version pinning in package.json
5. Performance monitoring

---

## Getting Started

### Prerequisites

```bash
# Required
- VSCode >= 1.100.0
- Node.js >= 18.0.0
- GitHub Copilot subscription (for full features)

# Optional
- @vscode/test-electron (for advanced testing)
- Docker (for isolated environments)
```

### Quick Start

```bash
# Step 1: Navigate to implementation directory
cd CopilotAgentWorkspace/demos/04-comprehensive-test-suite

# Step 2: Install dependencies
npm install

# Step 3: Create integration test runner
npm run compile

# Step 4: Start first implementation
npm run implement:chat-tutorial
```

---

## Next Steps

1. ✅ Create this roadmap (done)
2. → Create integration test framework
3. → Implement chat-tutorial
4. → Add manual testing guide
5. → Create agent instructions
6. → Implement remaining examples

---

**Roadmap Version:** 1.0  
**Created:** April 11, 2026  
**Status:** 🟢 Ready to implement  
**Estimated Completion:** 22 hours
