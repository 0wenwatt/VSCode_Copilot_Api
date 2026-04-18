/**
 * VSCODE COPILOT HOOKS & TOOLS GUIDE
 * 
 * This guide demonstrates how to create and register custom hooks and tools
 * that extend VSCode Copilot's capabilities.
 * 
 * Key Concepts:
 * - Hooks: Lifecycle events that Copilot fires
 * - Tools: Custom capabilities that Copilot can invoke
 * - Context Providers: Data providers for Copilot Chat
 * - Participants: Domain-specific Copilot chat agents
 */

import * as vscode from 'vscode';

// ============================================================================
// CONCEPT 1: HOOKS
// ============================================================================

/**
 * Hooks are extension points where you can react to Copilot events
 */

export interface CopilotHook {
  name: string;
  handler: (context: any) => void | Promise<void>;
  priority?: number; // Lower = higher priority
}

/**
 * Available hooks in VSCode Copilot
 */
export const AVAILABLE_HOOKS = {
  'copilot:ready': 'Fired when Copilot is initialized',
  'copilot:chat-opened': 'Fired when a chat session is opened',
  'copilot:chat-closed': 'Fired when a chat session is closed',
  'copilot:inline-completion-shown': 'Fired when inline completion is shown',
  'copilot:completion-accepted': 'Fired when user accepts a completion',
  'copilot:completion-rejected': 'Fired when user rejects a completion',
  'copilot:tool-invoked': 'Fired when a tool/skill is invoked',
  'copilot:context-provided': 'Fired when context is provided to Copilot'
};

/**
 * Example: Hook for tracking skill usage
 */
export const skillUsageHook: CopilotHook = {
  name: 'copilot:tool-invoked',
  handler: async (context) => {
    const { toolName, userId, duration, success } = context;
    console.log(`📊 Skill Used: ${toolName}`);
    console.log(`   Duration: ${duration}ms`);
    console.log(`   Success: ${success ? '✅' : '❌'}`);
    // Send to analytics
  }
};

/**
 * Example: Hook for code context detection
 */
export const codeContextHook: CopilotHook = {
  name: 'copilot:chat-opened',
  handler: async (context) => {
    const { activeFile, language, selectedText } = context;
    console.log(`📝 Chat opened for ${language} file`);
    console.log(`   File: ${activeFile}`);
    if (selectedText) {
      console.log(`   Selection: ${selectedText.substring(0, 50)}...`);
    }
    // Provide relevant context to Copilot
  }
};

// ============================================================================
// CONCEPT 2: TOOLS (VSCODE.LM.REGISTERTOOL)
// ============================================================================

/**
 * Tools are functions that Copilot can call to extend its capabilities.
 * Tools are registered via vscode.lm.registerTool()
 */

export interface CopilotTool {
  name: string;
  description: string;
  parameters: {
    type: 'object';
    properties: Record<string, any>;
    required?: string[];
  };
  invoke: (input: any, token: vscode.CancellationToken) => Promise<any>;
}

/**
 * Example Tool 1: File search and analysis
 */
export const fileSearchTool: CopilotTool = {
  name: 'vscode.searchFiles',
  description: 'Search for files matching a pattern and return their contents',

  parameters: {
    type: 'object',
    properties: {
      pattern: {
        type: 'string',
        description: 'Glob pattern to search for (e.g., "**/*.ts")'
      },
      maxResults: {
        type: 'number',
        description: 'Maximum number of results to return',
        default: 10
      }
    },
    required: ['pattern']
  },

  invoke: async (input: any, token: vscode.CancellationToken) => {
    const { pattern, maxResults = 10 } = input;

    try {
      const files = await vscode.workspace.findFiles(pattern, null, maxResults);
      const results = [];

      for (const file of files) {
        if (token.isCancellationRequested) break;

        const content = await vscode.workspace.fs.readFile(file);
        const fileName = file.fsPath.split(/[\\\/]/).pop() || '';
        results.push({
          path: file.fsPath,
          name: fileName,
          size: content.length,
          language: fileName.split('.').pop()
        });
      }

      return {
        success: true,
        filesFound: results.length,
        results
      };
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error'
      };
    }
  }
};

/**
 * Example Tool 2: Code diagnostics
 */
export const diagnosticsTool: CopilotTool = {
  name: 'vscode.getDiagnostics',
  description: 'Get diagnostics (errors/warnings) for the current file',

  parameters: {
    type: 'object',
    properties: {
      fileName: {
        type: 'string',
        description: 'File to get diagnostics for (relative to workspace)'
      },
      includeSeverity: {
        type: 'array',
        items: {
          enum: ['error', 'warning', 'information', 'hint']
        },
        description: 'Diagnostic severities to include'
      }
    },
    required: ['fileName']
  },

  invoke: async (input: any, token: vscode.CancellationToken) => {
    const { fileName, includeSeverity = ['error', 'warning'] } = input;

    try {
      // Get all diagnostics
      const allDiags = vscode.languages.getDiagnostics();
      const severityMap = { error: 0, warning: 1, information: 2, hint: 3 };

      const relevantDiags = allDiags
        .filter(([uri]) => uri.fsPath.endsWith(fileName))
        .flatMap(([_, diags]) => diags)
        .filter(d => includeSeverity.includes(
          Object.keys(severityMap)[Object.values(severityMap).indexOf(d.severity || 0)]
        ))
        .map(d => ({
          message: d.message,
          range: `${d.range.start.line}:${d.range.start.character}`,
          severity: Object.keys(severityMap)[d.severity || 0],
          source: d.source
        }));

      return {
        success: true,
        file: fileName,
        diagnosticCount: relevantDiags.length,
        diagnostics: relevantDiags
      };
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error'
      };
    }
  }
};

/**
 * Example Tool 3: Symbol lookup
 */
export const symbolLookupTool: CopilotTool = {
  name: 'vscode.lookupSymbol',
  description: 'Look up symbols (functions, classes, etc.) in the workspace',

  parameters: {
    type: 'object',
    properties: {
      query: {
        type: 'string',
        description: 'Symbol name to search for'
      },
      kind: {
        type: 'string',
        enum: ['function', 'class', 'interface', 'method', 'property', 'variable'],
        description: 'Type of symbol'
      }
    },
    required: ['query']
  },

  invoke: async (input: any, token: vscode.CancellationToken) => {
    const { query, kind } = input;

    try {
      const symbols = await vscode.commands.executeCommand(
        'workbench.action.quickOpen',
        `@${kind ? kind + ' ' : ''}${query}`
      );

      return {
        success: true,
        query,
        found: symbols ? true : false,
        message: 'Symbol lookup completed (manual action required)'
      };
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error'
      };
    }
  }
};

// ============================================================================
// CONCEPT 3: CONTEXT PROVIDERS
// ============================================================================

/**
 * Context providers give Copilot information about the current state
 */

export interface ContextVariable {
  name: string;
  description: string;
  value: string | (() => Promise<string>);
  icon?: string;
}

/**
 * Example: Code context provider
 */
export const codeContextVariables: ContextVariable[] = [
  {
    name: 'selectedCode',
    description: 'Currently selected code',
    icon: '📝',
    value: async () => {
      const editor = vscode.window.activeTextEditor;
      return editor?.document.getText(editor.selection) || '';
    }
  },
  {
    name: 'activeFile',
    description: 'Currently open file',
    icon: '📄',
    value: async () => {
      return vscode.window.activeTextEditor?.document.fileName || 'none';
    }
  },
  {
    name: 'projectRoot',
    description: 'Project root directory',
    icon: '📁',
    value: vscode.workspace.workspaceFolders?.[0]?.uri?.fsPath || 'none'
  },
  {
    name: 'languageMode',
    description: 'Current file language',
    icon: '🔤',
    value: async () => {
      return vscode.window.activeTextEditor?.document.languageId || 'unknown';
    }
  }
];

// ============================================================================
// CONCEPT 4: CHAT PARTICIPANTS
// ============================================================================

/**
 * A chat participant is a specialized agent in Copilot Chat
 * Users invoke it with @participantName
 */

export interface ChatParticipant {
  name: string;
  description: string;
  commands: ChatCommand[];
}

export interface ChatCommand {
  name: string;
  description: string;
  handler: (context: any) => Promise<string>;
}

/**
 * Example: Helper chat participant
 */
export const helperParticipant: ChatParticipant = {
  name: 'helper',
  description: 'VSCode helper and assistant',

  commands: [
    {
      name: 'analyze',
      description: 'Analyze current code and provide suggestions',
      handler: async (context) => {
        const editor = vscode.window.activeTextEditor;
        if (!editor) return 'No active editor';

        const code = editor.document.getText();
        return `Analyzing ${code.split('\n').length} lines of code...`;
      }
    },
    {
      name: 'explain',
      description: 'Explain the selected code',
      handler: async (context) => {
        const editor = vscode.window.activeTextEditor;
        if (!editor) return 'No active editor';

        const selectedText = editor.document.getText(editor.selection);
        if (!selectedText) return 'No code selected';

        return `Explaining: ${selectedText.substring(0, 50)}...`;
      }
    },
    {
      name: 'generate',
      description: 'Generate code based on requirements',
      handler: async (context) => {
        const prompt = context.input || 'No requirements provided';
        return `Generating code for: ${prompt}`;
      }
    }
  ]
};

// ============================================================================
// HOOK REGISTRATION
// ============================================================================

/**
 * Register hooks in extension
 */
export function registerHooks(context: vscode.ExtensionContext, hooks: CopilotHook[]) {
  for (const hook of hooks) {
    // In actual implementation, would subscribe to Copilot events
    console.log(`✅ Registered hook: ${hook.name} (priority: ${hook.priority || 0})`);
  }
}

// ============================================================================
// TOOL REGISTRATION
// ============================================================================

/**
 * Register tools in extension
 */
export async function registerTools(context: vscode.ExtensionContext, tools: CopilotTool[]) {
  for (const tool of tools) {
    try {
      // In actual implementation, would call:
      // vscode.lm.registerTool(tool.name, tool);
      console.log(`✅ Registered tool: ${tool.name}`);
      console.log(`   Description: ${tool.description}`);
    } catch (error) {
      console.error(`❌ Failed to register tool: ${tool.name}`, error);
    }
  }
}

// ============================================================================
// INTEGRATION EXAMPLE
// ============================================================================

/**
 * Complete example of registering hooks, tools, and context
 */
export async function activateCopilotExtension(context: vscode.ExtensionContext) {
  console.log('🚀 Activating Copilot integration...\n');

  // Register hooks
  console.log('📌 Registering Hooks:');
  registerHooks(context, [skillUsageHook, codeContextHook]);

  // Register tools
  console.log('\n🔧 Registering Tools:');
  await registerTools(context, [fileSearchTool, diagnosticsTool, symbolLookupTool]);

  // Register context variables
  console.log('\n📊 Context Variables Available:');
  for (const variable of codeContextVariables) {
    console.log(`   ${variable.icon} ${variable.name}: ${variable.description}`);
  }

  // Register chat participant
  console.log('\n💬 Chat Participants:');
  console.log(`   @${helperParticipant.name}: ${helperParticipant.description}`);
  for (const cmd of helperParticipant.commands) {
    console.log(`      /${cmd.name}: ${cmd.description}`);
  }

  console.log('\n✅ Copilot integration complete!\n');
}

// ============================================================================
// EXPORTS
// ============================================================================

export const copilotHooksAndTools = {
  // Hooks
  AVAILABLE_HOOKS,
  skillUsageHook,
  codeContextHook,

  // Tools
  fileSearchTool,
  diagnosticsTool,
  symbolLookupTool,

  // Context
  codeContextVariables,

  // Chat Participants
  helperParticipant,

  // Registration
  registerHooks,
  registerTools,
  activateCopilotExtension
};

export default copilotHooksAndTools;
