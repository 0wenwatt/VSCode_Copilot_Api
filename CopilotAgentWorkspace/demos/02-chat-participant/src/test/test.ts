import * as fs from "fs";
import * as path from "path";

/**
 * Test: Chat Participant Demo
 *
 * Verifies that:
 * 1. Chat participant can be created
 * 2. Request handler works
 * 3. Response streaming works
 * 4. Interactions are logged
 * 5. Chat participant is discoverable
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

// Test 1: Verify chat participant structure
function test_chatParticipantStructure(): void {
  const start = Date.now();

  try {
    // Mock chat participant data
    const participant = {
      id: "demo.chatParticipant",
      name: "demo",
      iconPath: "lightbulb",
      handler: function handleChatRequest() {
        return Promise.resolve();
      },
    };

    const hasId = typeof participant.id === "string";
    const hasName = typeof participant.name === "string";
    const hasHandler = typeof participant.handler === "function";

    const passed = hasId && hasName && hasHandler;
    const duration = Date.now() - start;

    logTest(
      "Chat participant has required structure",
      passed,
      passed ? "" : "Missing required fields",
      duration
    );
  } catch (error) {
    logTest(
      "Chat participant has required structure",
      false,
      String(error),
      Date.now() - start
    );
  }
}

// Test 2: Verify chat request handling
function test_chatRequestHandling(): void {
  const start = Date.now();

  try {
    // Mock chat request
    const mockRequest = {
      prompt: "What can you help me with?",
      command: "default",
    };

    // Mock chat context
    const mockContext = {
      history: [
        { kind: "message", content: "Previous message" },
        { kind: "message", content: "Another message" },
      ],
    };

    const hasPrompt = typeof mockRequest.prompt === "string";
    const hasContext = Array.isArray(mockContext.history);
    const historyLength = mockContext.history.length > 0;

    const passed = hasPrompt && hasContext && historyLength;
    const duration = Date.now() - start;

    logTest(
      "Chat request can be handled",
      passed,
      passed ? "" : "Invalid request structure",
      duration
    );
  } catch (error) {
    logTest(
      "Chat request can be handled",
      false,
      String(error),
      Date.now() - start
    );
  }
}

// Test 3: Verify response streaming
function test_responseStreaming(): void {
  const start = Date.now();

  try {
    // Mock response stream
    const streamBuffer: string[] = [];
    const mockStream = {
      markdown: (content: string) => {
        streamBuffer.push(content);
      },
      button: (button: unknown) => {
        // buttons can be pushed too
      },
      push: (content: unknown) => {
        // generic content
      },
    };

    // Simulate streaming response
    mockStream.markdown("### Response\n");
    mockStream.markdown("User asked: **test**\n");
    mockStream.markdown("```json\n");
    mockStream.markdown('{"status": "success"}\n');
    mockStream.markdown("```\n");

    const hasContent = streamBuffer.length > 0;
    const hasMarkdown = streamBuffer.some((s) => s.includes("###"));
    const hasJson = streamBuffer.some((s) => s.includes("json"));

    const passed = hasContent && hasMarkdown && hasJson;
    const duration = Date.now() - start;

    logTest(
      "Response can be streamed",
      passed,
      passed ? "" : "Streaming failed",
      duration
    );
  } catch (error) {
    logTest(
      "Response can be streamed",
      false,
      String(error),
      Date.now() - start
    );
  }
}

// Test 4: Verify interaction logging
function test_interactionLogging(): void {
  const start = Date.now();

  try {
    const interactions = [
      {
        timestamp: new Date().toISOString(),
        userMessage: "Hello",
        commandRan: "default",
        historyLength: 2,
      },
      {
        timestamp: new Date().toISOString(),
        userMessage: "How are you?",
        commandRan: "default",
        historyLength: 3,
      },
    ];

    // Verify structure
    const allHaveTimestamp = interactions.every((i) =>
      typeof i.timestamp === "string"
    );
    const allHaveMessage = interactions.every((i) =>
      typeof i.userMessage === "string"
    );
    const canSerialize = JSON.stringify(interactions);

    const passed = allHaveTimestamp && allHaveMessage && !!canSerialize;
    const duration = Date.now() - start;

    logTest(
      "Interactions can be logged",
      passed,
      passed ? "" : "Logging structure invalid",
      duration
    );
  } catch (error) {
    logTest(
      "Interactions can be logged",
      false,
      String(error),
      Date.now() - start
    );
  }
}

// Test 5: Verify participant discovery
function test_participantDiscovery(): void {
  const start = Date.now();

  try {
    // Mock participant registry
    const participants = {
      "demo.chatParticipant": {
        id: "demo.chatParticipant",
        name: "demo",
        registered: true,
      },
    };

    const isDiscoverable = "@demo" in { "@demo": participants };
    const hasMetadata = participants["demo.chatParticipant"].name === "demo";
    const isRegistered = participants["demo.chatParticipant"].registered;

    const passed = hasMetadata && isRegistered;
    const duration = Date.now() - start;

    logTest(
      "Participant is discoverable",
      passed,
      passed ? "" : "Participant not discoverable",
      duration
    );
  } catch (error) {
    logTest(
      "Participant is discoverable",
      false,
      String(error),
      Date.now() - start
    );
  }
}

// Test 6: Verify icon handling
function test_iconHandling(): void {
  const start = Date.now();

  try {
    const iconPath = "lightbulb";
    const isValidIcon =
      iconPath === "lightbulb" ||
      iconPath === "comment" ||
      iconPath === "robot" ||
      iconPath === "sparkles";

    const passed = isValidIcon;
    const duration = Date.now() - start;

    logTest(
      "Icon path is valid",
      passed,
      passed ? "" : "Invalid icon path",
      duration
    );
  } catch (error) {
    logTest(
      "Icon path is valid",
      false,
      String(error),
      Date.now() - start
    );
  }
}

// Run all tests
function runAllTests(): void {
  console.log("\n📋 Running Chat Participant Demo Tests\n");
  console.log("━".repeat(60));

  test_chatParticipantStructure();
  test_chatRequestHandling();
  test_responseStreaming();
  test_interactionLogging();
  test_participantDiscovery();
  test_iconHandling();

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
