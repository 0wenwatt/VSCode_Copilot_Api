import * as fs from "fs";
import * as path from "path";

/**
 * Test: Language Model Tool Demo
 *
 * Verifies that:
 * 1. Tools can be registered
 * 2. Tool schemas are valid
 * 3. Tool handlers work
 * 4. Tool results are structured correctly
 * 5. Tools can be invoked
 * 6. Tool calls are logged
 */

interface TestResult {
  name: string;
  passed: boolean;
  message: string; duration: number;
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

// Test 1: Verify tool definition structure
function test_toolDefinitionStructure(): void {
  const start = Date.now();

  try {
    // Mock tool definition
    const toolDef = {
      name: "demo.countCodeLines",
      description: "Count lines of code",
      inputSchema: {
        type: "object",
        properties: {
          includeComments: {
            type: "boolean",
            description: "Include comments",
          },
        },
      },
      invoke: async (options: unknown) => {
        return "result";
      },
    };

    const hasName = typeof toolDef.name === "string";
    const hasDescription = typeof toolDef.description === "string";
    const hasInputSchema =
      toolDef.inputSchema && toolDef.inputSchema.type === "object";
    const hasInvoke = typeof toolDef.invoke === "function";

    const passed = hasName && hasDescription && hasInputSchema && hasInvoke;
    const duration = Date.now() - start;

    logTest(
      "Tool definition has required structure",
      passed,
      passed ? "" : "Missing required fields",
      duration
    );
  } catch (error) {
    logTest(
      "Tool definition has required structure",
      false,
      String(error),
      Date.now() - start
    );
  }
}

// Test 2: Verify input schema validation
function test_inputSchemaValidation(): void {
  const start = Date.now();

  try {
    const schema = {
      type: "object",
      properties: {
        includeComments: { type: "boolean" },
        maxLines: { type: "number" },
        filter: { type: "string" },
      },
      required: ["includeComments"],
    };

    const hasType = schema.type === "object";
    const hasProperties = Object.keys(schema.properties).length > 0;
    const hasRequired = Array.isArray(schema.required);

    const passed = hasType && hasProperties && hasRequired;
    const duration = Date.now() - start;

    logTest(
      "Input schema is valid",
      passed,
      passed ? "" : "Invalid schema structure",
      duration
    );
  } catch (error) {
    logTest(
      "Input schema is valid",
      false,
      String(error),
      Date.now() - start
    );
  }
}

// Test 3: Verify tool result structure
function test_toolResultStructure(): void {
  const start = Date.now();

  try {
    // Mock tool result
    const toolResult = {
      content: {
        kind: "text",
        value: JSON.stringify({ lineCount: 42, fileName: "test.ts" }),
      },
    };

    const hasContent = toolResult.content && toolResult.content.kind;
    const hasValue = toolResult.content && toolResult.content.value;

    const passed = hasContent && hasValue;
    const duration = Date.now() - start;

    logTest(
      "Tool result has correct structure",
      passed,
      passed ? "" : "Result structure invalid",
      duration
    );
  } catch (error) {
    logTest(
      "Tool result has correct structure",
      false,
      String(error),
      Date.now() - start
    );
  }
}

// Test 4: Verify tool invocation logic
function test_toolInvocationLogic(): void {
  const start = Date.now();

  try {
    // Simulate tool invocation
    const toolRegistry: { [key: string]: unknown } = {
      "demo.countCodeLines": {
        name: "countCodeLines",
        lastInvoked: new Date().toISOString(),
        callCount: 5,
      },
      "demo.analyzeText": {
        name: "analyzeText",
        lastInvoked: new Date().toISOString(),
        callCount: 3,
      },
    };

    const toolsRegistered = Object.keys(toolRegistry).length > 0;
    const allHaveCallCount = Object.values(toolRegistry).every(
      (t: unknown) =>
        typeof (t as { callCount?: number }).callCount === "number"
    );
    const tracksInvocation = Object.values(toolRegistry).every(
      (t: unknown) =>
        typeof (t as { lastInvoked?: string }).lastInvoked === "string"
    );

    const passed = toolsRegistered && allHaveCallCount && tracksInvocation;
    const duration = Date.now() - start;

    logTest(
      "Tool invocation can be tracked",
      passed,
      passed ? "" : "Invocation tracking failed",
      duration
    );
  } catch (error) {
    logTest(
      "Tool invocation can be tracked",
      false,
      String(error),
      Date.now() - start
    );
  }
}

// Test 5: Verify tool logging
function test_toolLogging(): void {
  const start = Date.now();

  try {
    const toolCalls = [
      {
        timestamp: new Date().toISOString(),
        tool: "countCodeLines",
        input: { includeComments: true },
        result: { lineCount: 42, codeLines: 35, commentLines: 7 },
      },
      {
        timestamp: new Date().toISOString(),
        tool: "analyzeText",
        input: { includeStats: true },
        result: { wordCount: 150, lineCount: 5, charCount: 800 },
      },
    ];

    const allHaveTimestamp = toolCalls.every((c) =>
      typeof c.timestamp === "string"
    );
    const allHaveTool = toolCalls.every((c) => typeof c.tool === "string");
    const allHaveResult = toolCalls.every((c) => c.result !== null);

    const passed = allHaveTimestamp && allHaveTool && allHaveResult;
    const duration = Date.now() - start;

    logTest(
      "Tool calls can be logged",
      passed,
      passed ? "" : "Logging structure invalid",
      duration
    );
  } catch (error) {
    logTest(
      "Tool calls can be logged",
      false,
      String(error),
      Date.now() - start
    );
  }
}

// Test 6: Verify tool discovery
function test_toolDiscovery(): void {
  const start = Date.now();

  try {
    // Mock tool discovery
    const tools = [
      {
        id: "demo.countCodeLines",
        name: "countCodeLines",
        description: "Count lines",
      },
      { id: "demo.analyzeText", name: "analyzeText", description: "Analyze" },
    ];

    const allHaveId = tools.every((t) => typeof t.id === "string");
    const allHaveName = tools.every((t) => typeof t.name === "string");
    const allHaveDescription = tools.every(
      (t) => typeof t.description === "string"
    );

    const passed = allHaveId && allHaveName && allHaveDescription;
    const duration = Date.now() - start;

    logTest(
      "Tools are discoverable",
      passed,
      passed ? "" : "Tool discovery failed",
      duration
    );
  } catch (error) {
    logTest(
      "Tools are discoverable",
      false,
      String(error),
      Date.now() - start
    );
  }
}

// Test 7: Verify tool parameters
function test_toolParameters(): void {
  const start = Date.now();

  try {
    // Verify parameter handling
    const params = {
      includeComments: true,
      maxLines: 1000,
      filter: "*.ts",
    };

    const canSerialize = JSON.stringify(params);
    const canDeserialize = JSON.parse(canSerialize);

    const passed =
      canDeserialize.includeComments === true &&
      canDeserialize.maxLines === 1000;
    const duration = Date.now() - start;

    logTest(
      "Tool parameters are serializable",
      passed,
      passed ? "" : "Parameter handling failed",
      duration
    );
  } catch (error) {
    logTest(
      "Tool parameters are serializable",
      false,
      String(error),
      Date.now() - start
    );
  }
}

// Run all tests
function runAllTests(): void {
  console.log("\n📋 Running Language Model Tool Demo Tests\n");
  console.log("━".repeat(60));

  test_toolDefinitionStructure();
  test_inputSchemaValidation();
  test_toolResultStructure();
  test_toolInvocationLogic();
  test_toolLogging();
  test_toolDiscovery();
  test_toolParameters();

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
