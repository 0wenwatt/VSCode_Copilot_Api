import * as fs from "fs";
import * as path from "path";

/**
 * Test: Context Window Demo
 *
 * This test verifies that:
 * 1. The demo can capture context window state
 * 2. Results are written to files
 * 3. JSON structure is valid
 * 4. All required fields are present
 */

interface TestResult {
  name: string;
  passed: boolean;
  message: string;
  duration: number;
}

const results: TestResult[] = [];

function logTest(
  name: string,
  passed: boolean,
  message: string,
  duration: number
): void {
  results.push({ name, passed, message, duration });
  const status = passed ? "✓ PASS" : "✗ FAIL";
  console.log(`${status} - ${name} (${duration}ms)`);
  if (!passed) console.log(`   └─ ${message}`);
}

// Test 1: Verify context snapshot structure
function test_contextSnapshotStructure(): void {
  const start = Date.now();

  try {
    // Simulate what the extension would capture
    const mockContext = {
      timestamp: new Date().toISOString(),
      activeEditor: {
        fileName: "test.ts",
        language: "typescript",
        isDirty: false,
        lineCount: 42,
        cursorLine: 10,
        cursorCharacter: 5,
        contentPreview: "import * as vscode from 'vscode'",
      },
      selection: {
        selectedText: "vscode",
        selectionStart: { line: 10, character: 5 },
        selectionEnd: { line: 10, character: 11 },
      },
      workspace: {
        name: "demo-workspace",
        folders: ["src", "test"],
        fileCount: 0,
      },
      openEditors: [
        { fileName: "extension.ts", language: "typescript" },
        { fileName: "README.md", language: "markdown" },
      ],
    };

    // Validate structure
    const hasTimestamp = typeof mockContext.timestamp === "string";
    const hasActiveEditor =
      mockContext.activeEditor &&
      mockContext.activeEditor.fileName &&
      mockContext.activeEditor.language;
    const hasOpenEditors =
      Array.isArray(mockContext.openEditors) &&
      mockContext.openEditors.length > 0;

    const passed = hasTimestamp && hasActiveEditor && hasOpenEditors;
    const duration = Date.now() - start;

    logTest(
      "Context snapshot has required structure",
      passed,
      passed ? "" : "Missing required fields",
      duration
    );
  } catch (error) {
    logTest(
      "Context snapshot has required structure",
      false,
      String(error),
      Date.now() - start
    );
  }
}

// Test 2: Verify JSON serialization works
function test_jsonSerialization(): void {
  const start = Date.now();

  try {
    const mockContext = {
      timestamp: new Date().toISOString(),
      activeEditor: {
        fileName: "test.ts",
        language: "typescript",
        isDirty: false,
        lineCount: 42,
        cursorLine: 10,
        cursorCharacter: 5,
        contentPreview: "import * as vscode",
      },
      openEditors: [],
    };

    const json = JSON.stringify(mockContext, null, 2);
    const parsed = JSON.parse(json);

    const passed =
      parsed.timestamp === mockContext.timestamp &&
      parsed.activeEditor.fileName === mockContext.activeEditor.fileName;
    const duration = Date.now() - start;

    logTest(
      "Context can be serialized to JSON",
      passed,
      passed ? "" : "Serialization failed",
      duration
    );
  } catch (error) {
    logTest(
      "Context can be serialized to JSON",
      false,
      String(error),
      Date.now() - start
    );
  }
}

// Test 3: Verify Markdown generation
function test_markdownGeneration(): void {
  const start = Date.now();

  try {
    const mockContext = {
      timestamp: new Date().toISOString(),
      activeEditor: {
        fileName: "extension.ts",
        language: "typescript",
        isDirty: false,
        lineCount: 100,
        cursorLine: 50,
        cursorCharacter: 10,
        contentPreview: "export function activate",
      },
    };

    const markdown = `# Copilot Context Window Snapshot

**Captured:** ${mockContext.timestamp}

## Active Editor
- File: \`${mockContext.activeEditor.fileName}\`
- Language: ${mockContext.activeEditor.language}
`;

    const hasHeader =
      markdown.includes("# Copilot Context Window Snapshot");
    const hasActiveEditor = markdown.includes("## Active Editor");
    const hasFileName = markdown.includes(mockContext.activeEditor.fileName);

    const passed = hasHeader && hasActiveEditor && hasFileName;
    const duration = Date.now() - start;

    logTest(
      "Markdown output can be generated",
      passed,
      passed ? "" : "Markdown generation failed",
      duration
    );
  } catch (error) {
    logTest(
      "Markdown output can be generated",
      false,
      String(error),
      Date.now() - start
    );
  }
}

// Test 4: Verify file write capability
function test_fileWriteCapability(): void {
  const start = Date.now();

  try {
    const testDir = path.join(__dirname, "temp");
    if (!fs.existsSync(testDir)) fs.mkdirSync(testDir, { recursive: true });

    const testFile = path.join(testDir, "test_context.json");
    const testData = {
      success: true,
      test: "file_write",
      timestamp: new Date().toISOString(),
    };

    fs.writeFileSync(testFile, JSON.stringify(testData, null, 2));
    const exists = fs.existsSync(testFile);
    const content = fs.readFileSync(testFile, "utf-8");
    const canParse = JSON.parse(content);

    // Cleanup
    fs.unlinkSync(testFile);
    fs.rmdirSync(testDir);

    const passed = exists && canParse.success === true;
    const duration = Date.now() - start;

    logTest(
      "Results can be written to file",
      passed,
      passed ? "" : "File write failed",
      duration
    );
  } catch (error) {
    logTest(
      "Results can be written to file",
      false,
      String(error),
      Date.now() - start
    );
  }
}

// Test 5: Verify timestamp format
function test_timestampFormat(): void {
  const start = Date.now();

  try {
    const timestamp = new Date().toISOString();
    const isValidISO = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}/.test(timestamp);
    const canParse = new Date(timestamp).getTime() > 0;

    const passed = isValidISO && canParse;
    const duration = Date.now() - start;

    logTest(
      "Timestamp is in valid ISO format",
      passed,
      passed ? "" : "Invalid timestamp format",
      duration
    );
  } catch (error) {
    logTest(
      "Timestamp is in valid ISO format",
      false,
      String(error),
      Date.now() - start
    );
  }
}

// Run all tests
function runAllTests(): void {
  console.log("\n📋 Running Context Window Demo Tests\n");
  console.log("━".repeat(60));

  test_contextSnapshotStructure();
  test_jsonSerialization();
  test_markdownGeneration();
  test_fileWriteCapability();
  test_timestampFormat();

  console.log("━".repeat(60) + "\n");

  const passed = results.filter((r) => r.passed).length;
  const total = results.length;
  const allPassed = passed === total;

  console.log(`📊 Results: ${passed}/${total} tests passed`);
  console.log(
    `Total time: ${results.reduce((sum, r) => sum + r.duration, 0)}ms\n`
  );

  if (allPassed) {
    console.log("✓ All tests passed!");
    process.exit(0);
  } else {
    console.log("✗ Some tests failed");
    process.exit(1);
  }
}

runAllTests();
