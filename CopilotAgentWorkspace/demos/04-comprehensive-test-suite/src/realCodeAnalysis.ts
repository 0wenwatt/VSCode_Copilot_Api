/**
 * REAL Test Suite - Actually Reads and Validates Source Code
 * 
 * This suite ACTUALLY checks the source files instead of hardcoding results
 */

import * as fs from 'fs';
import * as path from 'path';

interface CodeAnalysisResult {
  file: string;
  found: string[];
  missing: string[];
  passed: boolean;
}

interface AnalysisTest {
  name: string;
  example: string;
  filePath: string;
  patterns: {
    required: string[];    // Patterns that MUST exist
    optional?: string[];   // Patterns that MIGHT exist
  };
}

// ============================================================================
// ACTUAL CODE ANALYSIS
// ============================================================================

class RealCodeAnalyzer {
  private baseDir: string;

  constructor(baseDir: string) {
    this.baseDir = baseDir;
  }

  /**
   * Read a file and check if it contains specified patterns
   */
  analyzeFile(filePath: string, requiredPatterns: string[], optionalPatterns: string[] = []): CodeAnalysisResult {
    const fullPath = path.join(this.baseDir, filePath);
    const result: CodeAnalysisResult = {
      file: filePath,
      found: [],
      missing: [],
      passed: true
    };

    // Check if file exists
    if (!fs.existsSync(fullPath)) {
      result.missing.push('FILE_NOT_FOUND');
      result.passed = false;
      return result;
    }

    // Read file contents
    let content: string;
    try {
      content = fs.readFileSync(fullPath, 'utf-8');
    } catch (error) {
      result.missing.push(`READ_ERROR: ${error}`);
      result.passed = false;
      return result;
    }

    // Check required patterns
    for (const pattern of requiredPatterns) {
      if (content.includes(pattern)) {
        result.found.push(pattern);
      } else {
        result.missing.push(pattern);
        result.passed = false;
      }
    }

    // Check optional patterns
    for (const pattern of optionalPatterns) {
      if (content.includes(pattern)) {
        result.found.push(pattern);
      }
    }

    return result;
  }

  /**
   * Analyze multiple files
   */
  analyzeMultiple(tests: AnalysisTest[]): CodeAnalysisResult[] {
    return tests.map(test => {
      const patterns = test.patterns.optional || [];
      return this.analyzeFile(test.filePath, test.patterns.required, patterns);
    });
  }

  /**
   * Format results for display
   */
  formatResults(results: CodeAnalysisResult[]): string {
    let output = '\n' + '='.repeat(80) + '\n';
    output += '🔬 REAL CODE ANALYSIS RESULTS\n';
    output += '='.repeat(80) + '\n\n';

    let passedCount = 0;
    let failedCount = 0;

    for (const result of results) {
      const icon = result.passed ? '✅' : '❌';
      output += `${icon} ${result.file}\n`;

      if (result.found.length > 0) {
        output += `   Found (${result.found.length}):\n`;
        for (const pattern of result.found) {
          output += `     ✓ "${pattern}"\n`;
        }
      }

      if (result.missing.length > 0) {
        output += `   Missing (${result.missing.length}):\n`;
        for (const pattern of result.missing) {
          output += `     ✗ "${pattern}"\n`;
        }
      }

      output += '\n';
      if (result.passed) passedCount++;
      else failedCount++;
    }

    output += '='.repeat(80) + '\n';
    output += `Results: ${passedCount} passed, ${failedCount} failed\n`;
    output += '='.repeat(80) + '\n\n';

    return output;
  }
}

// ============================================================================
// DEFINE ACTUAL TESTS
// ============================================================================

const testsToRun: AnalysisTest[] = [
  {
    name: 'Chat Sample - Extension Activation',
    example: 'chat-sample',
    filePath: 'vscode-extension-samples/chat-sample/src/extension.ts',
    patterns: {
      required: [
        'export function activate',
        'registerChatParticipant',
        'vscode.chat'
      ],
      optional: ['simple', 'toolParticipant', '@cat']
    }
  },
  {
    name: 'Chat Tutorial - Participant Definition',
    example: 'chat-tutorial',
    filePath: 'vscode-extension-samples/chat-tutorial/src/extension.ts',
    patterns: {
      required: [
        'export function activate',
        'vscode.chat.createChatParticipant',
        '@tutor'
      ],
      optional: ['sendRequest', 'LanguageModelChatMessage']
    }
  },
  {
    name: 'LM API Tutorial - Extension Activation',
    example: 'lm-api-tutorial',
    filePath: 'vscode-extension-samples/lm-api-tutorial/src/extension.ts',
    patterns: {
      required: [
        'export function activate',
        'vscode.commands.registerCommand',
        'selectChatModels'
      ],
      optional: ['Editor.decoration', 'inline']
    }
  },
  {
    name: 'Chat Context Sample - Provider',
    example: 'chat-context-sample',
    filePath: 'vscode-extension-samples/chat-context-sample/src/extension.ts',
    patterns: {
      required: [
        'registerChatResourceContextProvider',
        'ChatResourceContextProvider',
        'ChatContextItem'
      ],
      optional: ['JSON', 'lineCount']
    }
  },
  {
    name: 'Chat Model Provider - Provider Implementation',
    example: 'chat-model-provider-sample',
    filePath: 'vscode-extension-samples/chat-model-provider-sample/src/provider.ts',
    patterns: {
      required: [
        'LanguageModelChatProvider2',
        'sendRequest',
        'models'
      ],
      optional: ['Dog', 'Cat', 'vendor']
    }
  },
  {
    name: 'Chat Output Renderer - Renderer',
    example: 'chat-output-renderer-sample',
    filePath: 'vscode-extension-samples/chat-output-renderer-sample/src/extension.ts',
    patterns: {
      required: [
        'export function activate',
        'vscode.chat'
      ],
      optional: ['renderer', 'webview']
    }
  },
  {
    name: 'MCP Extension - MCP Server',
    example: 'mcp-extension-sample',
    filePath: 'vscode-extension-samples/mcp-extension-sample/src/extension.ts',
    patterns: {
      required: [
        'export function activate',
        'registerMCPServer'
      ],
      optional: ['gist', 'github']
    }
  }
];

// ============================================================================
// MAIN EXECUTION
// ============================================================================

function main() {
  const samplesDir = path.join(__dirname, '../../../..');
  const analyzer = new RealCodeAnalyzer(samplesDir);

  console.log('\n🔬 Running REAL Code Analysis on Examples\n');
  console.log(`Base directory: ${samplesDir}\n`);

  const results = analyzer.analyzeMultiple(testsToRun);
  console.log(analyzer.formatResults(results));

  // Summary
  const passedTests = results.filter(r => r.passed).length;
  const totalTests = results.length;
  const passRate = Math.round(passedTests / totalTests * 100);

  console.log(`✅ Real Validation Complete`);
  console.log(`   Passed: ${passedTests}/${totalTests} (${passRate}%)`);
  console.log(`   Timestamp: ${new Date().toISOString()}\n`);

  process.exit(passedTests === totalTests ? 0 : 1);
}

main();
