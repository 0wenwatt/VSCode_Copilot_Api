# VSCode Copilot API - Folder Guide

Quick reference for what goes in each folder during development.

## Folder Descriptions & Usage

### 📦 vscode-extension-samples/
**Purpose**: Reference implementation from Microsoft

**What to Put Here**: Nothing - this is a read-only reference repository

**Usage**:
- Study existing patterns
- Copy boilerplate when needed
- Reference best practices

**Example Files**:
```
- helloworld-sample/
- webview-sample/
- language-server-sample/
- etc.
```

---

### 📚 docs/

**Purpose**: All documentation and guides

#### docs/api_reference/
- Complete VSCode Copilot API documentation
- Method signatures and parameters
- Return types and exceptions
- Usage examples for each API
- Limitations and gotchas

#### docs/guides/
- Setup and environment guides
- Integration tutorials
- Troubleshooting guides
- Best practices
- Common patterns

#### docs/tutorials/
- Step-by-step learning paths
- Hello World extension
- Building your first Copilot integration
- Progressive complexity tutorials

---

### 📋 implementation_plans/

**Purpose**: Design documents and development roadmaps

**What to Put Here**:
- System architecture documents
- Feature specifications
- Development roadmaps
- Technical decisions (ADRs)
- Sprint plans
- Risk analysis

**File Naming**:
- `PHASE_X_<description>.md`
- `ARCHITECTURE.md`
- `FEATURE_<feature_name>.md`
- `DECISION_<topic>.md`

---

### 🎯 demos/

**Purpose**: Proof-of-concept and demo implementations

#### demos/simple_extension/
- Minimal viable extension
- Demonstrates basic API usage
- Entry point for getting started

#### demos/advanced_scenarios/
- Complex use cases
- Multiple feature integration
- Performance optimization examples
- Advanced patterns

**What to Put Here**:
- Complete, runnable extension projects
- package.json, tsconfig.json
- Source code with explanations
- README with run instructions

---

### ✅ tests/

**Purpose**: Test suites and test planning

#### tests/unit/
- Tests for individual functions/methods
- Mock-heavy, fast execution
- File naming: `*.test.ts` or `*.spec.ts`

#### tests/integration/
- Tests for API interactions
- Tests between components
- Partial mocking or real dependencies

#### tests/e2e/
- Full workflow tests
- VSCode instance spinning up
- Real extension testing
- Scenario validation

**Files to Add**:
- `test-setup.md` - How to run tests
- `fixtures/` - Test data files
- `mocks/` - Mock implementations

---

### 🔖 reference_implementations/

**Purpose**: Reusable patterns and code templates

**What to Put Here**:
- Code snippets (commands, handlers, etc.)
- Design patterns (singleton, observer, factory, etc.)
- Utility modules
- Common configurations
- Boilerplate templates

**Organization**:
```
reference_implementations/
├── patterns/
│   ├── command-handler.ts
│   ├── event-listener.ts
│   └── state-manager.ts
├── utilities/
│   ├── logger.ts
│   ├── config-loader.ts
│   └── error-handler.ts
└── templates/
    └── extension-scaffold/
```

---

### 🔬 research/

**Purpose**: Investigation and analysis

#### research/api_analysis/
- API capability inventory
- API limitations document
- Compatibility matrix
- Performance characteristics
- Security analysis

#### research/feature_exploration/
- Experimental implementations
- Feature comparison
- Integration possibilities
- Edge cases and gotchas

**File Types**:
- Markdown analysis documents
- JSON data files
- Jupyter notebooks (if data-heavy)
- Benchmark reports

---

### 🏗️ architecture/

**Purpose**: System design and architecture documentation

**What to Put Here**:
- System design documents
- Component diagrams
- Data flow diagrams
- Interaction patterns
- Integration points
- Deployment architecture

**File Naming**:
- `SYSTEM_DESIGN.md` - Overall architecture
- `COMPONENTS.md` - Component breakdown
- `INTEGRATIONS.md` - How systems link together
- Diagrams in Markdown (Mermaid) or images

---

### 📱 api_definitions/

**Purpose**: API contracts and type definitions

**What to Put Here**:
- TypeScript interfaces
- Type definitions
- API schemas
- Data models
- Contract specifications

**File Organization**:
```
api_definitions/
├── vscode-copilot-types.ts
├── chat-types.ts
├── command-types.ts
├── schemas.json
└── interfaces/
```

---

### ⚙️ config/

**Purpose**: Configuration and build setup

**What to Put Here**:
- TypeScript configurations
- ESLint/Prettier configs
- Environment templates
- Build configurations
- Docker configs (if applicable)
- Dependency management files

**Standard Files**:
```
tsconfig.json
.eslintrc.json
.prettierrc
.env.example
build.config.ts
```

---

### 💼 project_workspace/

**Purpose**: Active development area for actual implementations

**Typical Structure**:
```
project_workspace/
├── copilot-integration/        # Main integration project
│   ├── src/
│   ├── test/
│   ├── package.json
│   └── tsconfig.json
├── custom-commands/           # Custom command implementations
├── ui-components/             # Reusable UI components
├── shared-utils/              # Shared utilities library
└── experiments/               # Experimental features
```

**What to Put Here**:
- Working extension code
- Actual implementations
- Deployable projects
- Integration code
- Active development branches

---

## Development Workflow by Phase

### Phase 1: Research & Planning
1. Add research documents to `research/`
2. Create implementation plans in `implementation_plans/`
3. Sketch architecture in `architecture/`
4. Document findings in `docs/`

### Phase 2: Documentation & Design
1. Complete `docs/` with comprehensive guides
2. Finalize architecture documents
3. Create detailed specifications in `implementation_plans/`
4. Define API contracts in `api_definitions/`

### Phase 3: Prototyping
1. Create demo projects in `demos/`
2. Reference `vscode-extension-samples/` frequently
3. Document patterns in `reference_implementations/`
4. Test concepts and document findings

### Phase 4: Implementation
1. Set up projects in `project_workspace/`
2. Use `reference_implementations/` for patterns
3. Apply architecture from `architecture/`
4. Add tests to `tests/` as you build

### Phase 5: Testing & Polish
1. Complete test suites in `tests/`
2. Update documentation in `docs/`
3. Create comprehensive demos
4. Package for release

---

## Cross-Folder References

When working on implementation:
1. Check `architecture/` for design decisions
2. Reference `reference_implementations/` for patterns
3. Consult `docs/` for guidelines
4. Review `research/` for limitations
5. Use `demos/` as examples
6. Run code from `project_workspace/`
7. Validate with tests in `tests/`

---

**This guide ensures organized, scalable development!**
