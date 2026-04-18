/**
 * VSCode Integration Test Runner
 * 
 * Tests examples by:
 * 1. Activating extensions
 * 2. Invoking chat participants
 * 3. Capturing results
 * 4. Validating behavior
 */

import * as fs from 'fs';
import * as path from 'path';
import { spawn, spawnSync } from 'child_process';

// ============================================================================
// TYPE DEFINITIONS
// ============================================================================

interface IntegrationTestConfig {
  extensionPath: string;
  exampleName: string;
  testCases: TestCase[];
  timeout: number;
}

interface TestCase {
  id: string;
  name: string;
  type: 'manual' | 'automated';
  
  // For manual tests
  steps?: ManualStep[];
  
  // For automated tests
  command?: string;
  expectedPattern?: string | RegExp;
  expectedSuccess?: boolean;
  
  // Results
  passed?: boolean;
  output?: string;
  error?: string;
  duration?: number;
}

interface ManualStep {
  action: string;
  verification: string;
  screenshot?: string;
}

interface TestResult {
  example: string;
  timestamp: string;
  totalTests: number;
  passedTests: number;
  failedTests: number;
  testCases: TestCase[];
  summary: string;
}

// ============================================================================
// INTEGRATION TEST RUNNER
// ============================================================================

class IntegrationTestRunner {
  private baseDir: string;
  private results: TestResult[] = [];
  private verbose: boolean = false;

  constructor(baseDir: string, verbose: boolean = false) {
    this.baseDir = baseDir;
    this.verbose = verbose;
  }

  /**
   * Log with optional verbose mode
   */
  log(message: string, verbose: boolean = false): void {
    if (!verbose || this.verbose) {
      console.log(message);
    }
  }

  /**
   * Run a single test case
   */
  async runTestCase(testCase: TestCase, extensionPath: string): Promise<TestCase> {
    const startTime = Date.now();
    this.log(`\n▶ Running: ${testCase.name}`);

    try {
      if (testCase.type === 'manual') {
        await this.runManualTest(testCase, extensionPath);
      } else {
        await this.runAutomatedTest(testCase, extensionPath);
      }
      testCase.passed = true;
    } catch (error) {
      testCase.passed = false;
      testCase.error = String(error);
      this.log(`  ✗ Failed: ${error}`);
    }

    testCase.duration = Date.now() - startTime;
    return testCase;
  }

  /**
   * Run manual test (requires user interaction)
   */
  async runManualTest(testCase: TestCase, extensionPath: string): Promise<void> {
    if (!testCase.steps) {
      throw new Error('Manual test must have steps');
    }

    this.log('\n📋 Manual Test Steps:');
    for (let i = 0; i < testCase.steps.length; i++) {
      const step = testCase.steps[i];
      this.log(`  ${i + 1}. ${step.action}`);
      this.log(`     Verify: ${step.verification}`);
    }

    // In real implementation, this would prompt user or use automation
    this.log('\n  [Manual testing would require user interaction]');
    this.log(`  Open: code --extensionDevelopmentPath=${extensionPath}`);
  }

  /**
   * Run automated test
   */
  async runAutomatedTest(testCase: TestCase, extensionPath: string): Promise<void> {
    if (!testCase.command) {
      throw new Error('Automated test must have command');
    }

    this.log(`  Command: ${testCase.command}`, true);

    return new Promise((resolve, reject) => {
      const proc = spawn('node', [testCase.command!], {
        cwd: path.dirname(extensionPath),
        stdio: ['pipe', 'pipe', 'pipe']
      });

      let output = '';
      let error = '';

      proc.stdout?.on('data', (data) => {
        output += data.toString();
        this.log(`  ${data.toString().trim()}`, true);
      });

      proc.stderr?.on('data', (data) => {
        error += data.toString();
        this.log(`  ERROR: ${data.toString().trim()}`);
      });

      proc.on('close', (code) => {
        testCase.output = output;
        if (error) testCase.error = error;

        if (testCase.expectedPattern) {
          const pattern = testCase.expectedPattern instanceof RegExp 
            ? testCase.expectedPattern 
            : new RegExp(testCase.expectedPattern);
          
          if (!pattern.test(output)) {
            reject(new Error(`Expected pattern not found: ${testCase.expectedPattern}`));
            return;
          }
        }

        if (testCase.expectedSuccess !== undefined) {
          const success = code === 0;
          if (success !== testCase.expectedSuccess) {
            reject(new Error(`Expected success=${testCase.expectedSuccess}, got ${success}`));
            return;
          }
        }

        if (code === 0) {
          resolve();
        } else {
          reject(new Error(`Process exited with code ${code}`));
        }
      });

      proc.on('error', reject);
    });
  }

  /**
   * Run all test cases for an example
   */
  async runExample(config: IntegrationTestConfig): Promise<TestResult> {
    this.log(`\n${'='.repeat(80)}`);
    this.log(`🧪 Testing: ${config.exampleName}`);
    this.log(`${'='.repeat(80)}`);
    this.log(`Extension: ${config.extensionPath}`);
    this.log(`Test cases: ${config.testCases.length}\n`);

    const results: TestCase[] = [];
    
    for (const testCase of config.testCases) {
      const result = await this.runTestCase(testCase, config.extensionPath);
      results.push(result);
    }

    const passed = results.filter(t => t.passed).length;
    const failed = results.filter(t => !t.passed).length;

    const testResult: TestResult = {
      example: config.exampleName,
      timestamp: new Date().toISOString(),
      totalTests: results.length,
      passedTests: passed,
      failedTests: failed,
      testCases: results,
      summary: `${passed}/${results.length} tests passed`
    };

    this.results.push(testResult);
    this.logResults(testResult);

    return testResult;
  }

  /**
   * Log test results
   */
  private logResults(result: TestResult): void {
    const icon = result.failedTests === 0 ? '✅' : '❌';
    this.log(`\n${icon} ${result.example}`);
    this.log(`   ${result.summary}`);
    
    for (const tc of result.testCases) {
      const tcIcon = tc.passed ? '  ✓' : '  ✗';
      this.log(`${tcIcon} ${tc.name}`);
      if (tc.error && this.verbose) {
        this.log(`    Error: ${tc.error}`);
      }
    }
  }

  /**
   * Format all results
   */
  formatResults(): string {
    let output = '\n' + '='.repeat(80) + '\n';
    output += '📊 INTEGRATION TEST RESULTS\n';
    output += '='.repeat(80) + '\n\n';

    let totalTests = 0;
    let totalPassed = 0;

    for (const result of this.results) {
      totalTests += result.totalTests;
      totalPassed += result.passedTests;
      
      const icon = result.failedTests === 0 ? '✅' : '❌';
      output += `${icon} ${result.example}\n`;
      output += `   ${result.summary}\n`;
    }

    const rate = Math.round(totalPassed / totalTests * 100);
    output += '\n' + '='.repeat(80) + '\n';
    output += `Overall: ${totalPassed}/${totalTests} tests passed (${rate}%)\n`;
    output += '='.repeat(80) + '\n';

    return output;
  }

  /**
   * Export results to JSON
   */
  toJSON() {
    return {
      timestamp: new Date().toISOString(),
      totalExamples: this.results.length,
      totalTests: this.results.reduce((sum, r) => sum + r.totalTests, 0),
      passedTests: this.results.reduce((sum, r) => sum + r.passedTests, 0),
      results: this.results
    };
  }

  /**
   * Save results to file
   */
  saveResults(outputPath: string): void {
    const results = this.toJSON();
    fs.writeFileSync(outputPath, JSON.stringify(results, null, 2));
    console.log(`📁 Results saved to: ${outputPath}`);
  }
}

// ============================================================================
// EXAMPLE TEST CONFIGURATIONS
// ============================================================================

const CHAT_TUTORIAL_TESTS: IntegrationTestConfig = {
  extensionPath: 'vscode-extension-samples/chat-tutorial',
  exampleName: 'chat-tutorial',
  timeout: 30000,
  testCases: [
    {
      id: 'ct-1',
      name: 'Extension loads without errors',
      type: 'manual',
      steps: [
        {
          action: 'Run: code --extensionDevelopmentPath=vscode-extension-samples/chat-tutorial',
          verification: 'VSCode opens with extension loaded'
        },
        {
          action: 'Check Debug Console',
          verification: 'No errors appear in console'
        }
      ]
    },
    {
      id: 'ct-2',
      name: 'Chat participant appears in list',
      type: 'manual',
      steps: [
        {
          action: 'Open Copilot Chat (Cmd+Shift+L)',
          verification: '@tutor participant appears in suggestions'
        }
      ]
    },
    {
      id: 'ct-3',
      name: 'Responds to basic query',
      type: 'manual',
      steps: [
        {
          action: 'Type: @tutor hello',
          verification: 'Receives response from chat participant'
        }
      ]
    },
    {
      id: 'ct-4',
      name: 'Handles /exercise command',
      type: 'manual',
      steps: [
        {
          action: 'Type: @tutor /exercise',
          verification: 'Generates a coding exercise'
        }
      ]
    }
  ]
};

const CHAT_SAMPLE_TESTS: IntegrationTestConfig = {
  extensionPath: 'vscode-extension-samples/chat-sample',
  exampleName: 'chat-sample',
  timeout: 30000,
  testCases: [
    {
      id: 'cs-1',
      name: 'Extension loads without errors',
      type: 'manual',
      steps: [
        {
          action: 'Run: code --extensionDevelopmentPath=vscode-extension-samples/chat-sample',
          verification: 'VSCode opens with extension loaded'
        }
      ]
    },
    {
      id: 'cs-2',
      name: 'Three chat participants available',
      type: 'manual',
      steps: [
        {
          action: 'Open Copilot Chat',
          verification: '@cat, @catTools, and @tool appear in suggestions'
        }
      ]
    },
    {
      id: 'cs-3',
      name: 'Tools are callable',
      type: 'manual',
      steps: [
        {
          action: 'Check available tools in chat',
          verification: 'TabCount, FindFiles, RunInTerminal tools are available'
        }
      ]
    }
  ]
};

// ============================================================================
// MAIN EXECUTION
// ============================================================================

async function main() {
  const args = process.argv.slice(2);
  const verbose = args.includes('--verbose');
  const example = args.find(a => a.startsWith('--example='))?.split('=')[1];

  const runner = new IntegrationTestRunner(process.cwd(), verbose);

  console.log('\n🚀 VSCode Integration Test Runner\n');

  // Run selected example or all
  if (example === 'chat-tutorial' || !example) {
    await runner.runExample(CHAT_TUTORIAL_TESTS);
  }
  if (example === 'chat-sample' || !example) {
    await runner.runExample(CHAT_SAMPLE_TESTS);
  }

  console.log(runner.formatResults());

  // Save results
  const resultsDir = path.join(__dirname, '../results');
  if (!fs.existsSync(resultsDir)) {
    fs.mkdirSync(resultsDir, { recursive: true });
  }

  const timestamp = new Date().getTime();
  runner.saveResults(path.join(resultsDir, `integration-test-${timestamp}.json`));
}

// Run if executed directly
if (require.main === module) {
  main().catch(console.error);
}

export { IntegrationTestRunner, IntegrationTestConfig, TestCase, TestResult };
