import * as vscode from "vscode";
import * as fs from "fs";
import * as path from "path";

/**
 * Language Model Tool Demo
 *
 * Demonstrates how to:
 * 1. Define custom tools that Copilot can use
 * 2. Register tools with vscode.lm.registerTool()
 * 3. Implement tool handlers
 * 4. Use input schemas for tool parameters
 * 5. Return structured tool results
 * 6. Handle tool invocation
 */

const workspaceDir = vscode.workspace.workspaceFolders?.[0]?.uri?.fsPath || "";
const toolCallLog: unknown[] = [];
const toolLogFile = path.join(workspaceDir, "DEMO_LM_TOOL_LOG.json");

let countCodeLinesCount = 0;
let analyzeTextCount = 0;

/**
 * Tool 1: Count Code Lines
 * Counts lines in the current file, excluding comments
 */
async function countCodeLines(options: { includeComments?: boolean }): Promise<
  vscode.LanguageModelToolResult
> {
  countCodeLinesCount++;

  try {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
      return new vscode.LanguageModelToolResult(
        [{ kind: "text", value: "No active editor" }]
      );
    }

    const doc = editor.document;
    const text = doc.getText();
    const lines = text.split("\n");

    let codeLines = 0;
    let commentLines = 0;

    for (const line of lines) {
      const trimmed = line.trim();
      if (!trimmed) continue;

      if (
        trimmed.startsWith("//") ||
        trimmed.startsWith("/*") ||
        trimmed.startsWith("*")
      ) {
        commentLines++;
      } else {
        codeLines++;
      }
    }

    const result = {
      fileName: path.basename(doc.fileName),
      totalLines: lines.length,
      codeLines,
      commentLines,
      includeComments: options.includeComments || false,
    };

    // Log the tool call
    toolCallLog.push({
      timestamp: new Date().toISOString(),
      tool: "countCodeLines",
      input: options,
      result,
    });

    return new vscode.LanguageModelToolResult([
      {
        kind: "text",
        value: JSON.stringify(result, null, 2),
      },
    ]);
  } catch (error) {
    return new vscode.LanguageModelToolResult(
      [{ kind: "text", value: `Error: ${String(error)}` }]
    );
  }
}

/**
 * Tool 2: Analyze Text
 * Analyzes selected text for word count, line count, etc.
 */
async function analyzeText(options: { includeStats?: boolean }): Promise<
  vscode.LanguageModelToolResult
> {
  analyzeTextCount++;

  try {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
      return new vscode.LanguageModelToolResult(
        [{ kind: "text", value: "No active editor" }]
      );
    }

    const selection = editor.selection;
    const text = editor.document.getText(selection);

    if (!text) {
      return new vscode.LanguageModelToolResult(
        [{ kind: "text", value: "No text selected" }]
      );
    }

    const wordCount = text.trim().split(/\s+/).length;
    const lineCount = text.split("\n").length;
    const charCount = text.length;

    const analysis = {
      textPreview: text.substring(0, 50) + "...",
      wordCount,
      lineCount,
      characterCount: charCount,
      averageWordLength: charCount / wordCount,
    };

    // Log the tool call
    toolCallLog.push({
      timestamp: new Date().toISOString(),
      tool: "analyzeText",
      input: options,
      result: analysis,
    });

    return new vscode.LanguageModelToolResult(
      [
        {
          kind: "text",
          value: JSON.stringify(analysis, null, 2),
        },
      ]
    );
  } catch (error) {
    return new vscode.LanguageModelToolResult(
      [{ kind: "text", value: `Error: ${String(error)}` }]
    );
  }
}

/**
 * Command: Invoke tool directly (not through chat)
 */
async function invokeToolCommand(): Promise<void> {
  const toolNames = ["countCodeLines", "analyzeText"];

  const selected = await vscode.window.showQuickPick(toolNames, {
    placeHolder: "Select a tool to invoke",
  });

  if (!selected) return;

  try {
    let result;

    if (selected === "countCodeLines") {
      result = await countCodeLines({ includeComments: true });
    } else if (selected === "analyzeText") {
      result = await analyzeText({ includeStats: true });
    }

    vscode.window.showInformationMessage(`✓ Tool executed: ${selected}`);

    // Log execution
    const logEntry = {
      timestamp: new Date().toISOString(),
      event: "tool_invoked_directly",
      tool: selected,
      success: true,
    };

    const testFile = path.join(
      workspaceDir,
      "DEMO_TOOL_INVOCATION_TEST.json"
    );
    fs.writeFileSync(testFile, JSON.stringify(logEntry, null, 2));

    console.log("DEMO: Tool Invoked");
    console.log(JSON.stringify(logEntry, null, 2));
  } catch (error) {
    vscode.window.showErrorMessage(`Failed to invoke tool: ${String(error)}`);
  }
}

/**
 * Command: List registered tools
 */
async function listToolsCommand(): Promise<void> {
  // Mock list of registered tools
  const tools = [
    {
      name: "countCodeLines",
      description: "Count lines of code in current file",
      invocationCount: countCodeLinesCount,
    },
    {
      name: "analyzeText",
      description: "Analyze selected text",
      invocationCount: analyzeTextCount,
    },
  ];

  const toolsInfo = {
    timestamp: new Date().toISOString(),
    registeredTools: tools,
    totalCalls: countCodeLinesCount + analyzeTextCount,
  };

  const testFile = path.join(workspaceDir, "DEMO_REGISTERED_TOOLS.json");
  fs.writeFileSync(testFile, JSON.stringify(toolsInfo, null, 2));

  vscode.window.showInformationMessage(
    `✓ ${tools.length} tools registered. Check ${path.basename(testFile)}`
  );

  console.log("DEMO: Registered Tools");
  console.log(JSON.stringify(toolsInfo, null, 2));
}

export function activate(context: vscode.ExtensionContext) {
  console.log("✓ Language Model Tool Demo activated");

  // Register Tool 1: Count Code Lines
  const countCodeLinesTool = vscode.lm.registerTool("demo.countCodeLines", {
    name: "countCodeLines",
    description: "Count lines of code in the active editor",
    inputSchema: {
      type: "object" as const,
      properties: {
        includeComments: {
          type: "boolean",
          description: "Include comment lines in the count",
        },
      },
    },
    invoke: async (options: unknown) => {
      return await countCodeLines(
        options as { includeComments?: boolean }
      );
    },
  });

  console.log('✓ Tool registered: "countCodeLines"');

  // Register Tool 2: Analyze Text
  const analyzeTextTool = vscode.lm.registerTool("demo.analyzeText", {
    name: "analyzeText",
    description: "Analyze selected text for statistics",
    inputSchema: {
      type: "object" as const,
      properties: {
        includeStats: {
          type: "boolean",
          description: "Include detailed statistics",
        },
      },
    },
    invoke: async (options: unknown) => {
      return await analyzeText(options as { includeStats?: boolean });
    },
  });

  console.log('✓ Tool registered: "analyzeText"');

  // Log registration
  const registration = {
    timestamp: new Date().toISOString(),
    event: "tools_registered",
    tools: ["demo.countCodeLines", "demo.analyzeText"],
    status: "active",
  };

  toolCallLog.push(registration);
  fs.writeFileSync(toolLogFile, JSON.stringify(toolCallLog, null, 2));

  // Register commands
  context.subscriptions.push(
    vscode.commands.registerCommand("demo.lmTool.invoke", invokeToolCommand),
    vscode.commands.registerCommand("demo.lmTool.listTools", listToolsCommand),
    countCodeLinesTool,
    analyzeTextTool
  );

  vscode.window.showInformationMessage(
    "✓ Language Model Tools registered (2 tools available to Copilot)"
  );
}

export function deactivate() {
  // Save final log
  if (toolCallLog.length > 0) {
    fs.writeFileSync(toolLogFile, JSON.stringify(toolCallLog, null, 2));
    console.log(`✓ Tool log saved to ${path.basename(toolLogFile)}`);
  }
}
