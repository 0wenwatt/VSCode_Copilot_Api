import * as vscode from "vscode";
import * as fs from "fs";
import * as path from "path";

/**
 * Chat Participant Demo
 *
 * Demonstrates how to:
 * 1. Create a custom chat participant
 * 2. Register it with VSCode
 * 3. Handle user requests
 * 4. Stream responses back to chat
 * 5. Log interactions
 */

let participantRegistered = false;
const interactionLog: unknown[] = [];
const workspaceDir = vscode.workspace.workspaceFolders?.[0]?.uri?.fsPath || "";
const logFile = path.join(workspaceDir, "DEMO_CHAT_PARTICIPANT_LOG.json");

/**
 * Main chat participant handler
 * Called when user sends a message with @demo prefix
 */
async function handleChatRequest(
  request: vscode.ChatRequest,
  context: vscode.ChatContext,
  stream: vscode.ChatResponseStream,
  token: vscode.CancellationToken
): Promise<void> {
  try {
    // Log the interaction
    const interaction = {
      timestamp: new Date().toISOString(),
      userMessage: request.prompt,
      commandRan: request.command,
      historyLength: context.history.length,
    };
    interactionLog.push(interaction);

    // Stream initial response
    stream.markdown("### Demo Chat Participant Response\n\n");

    // Echo the user's message
    stream.markdown(`You asked: **${request.prompt}**\n\n`);

    // Provide context about what was available
    stream.markdown("#### Available Context:\n");
    stream.markdown(`- History items: ${context.history.length}\n`);
    stream.markdown(`- Command: ${request.command || "default"}\n`);

    // Simulate some processing
    stream.markdown("\n#### Processing...\n");
    await new Promise((resolve) => setTimeout(resolve, 500));

    // Stream a response
    stream.markdown("✓ Successfully handled by demo chat participant!\n\n");

    // Show a code block
    stream.markdown("#### Request Details:\n```json\n");
    const details = {
      prompt: request.prompt,
      command: request.command,
      timestamp: new Date().toISOString(),
      responseType: "streaming markdown",
    };
    stream.markdown(JSON.stringify(details, null, 2));
    stream.markdown("\n```\n");

    // Save log
    fs.writeFileSync(logFile, JSON.stringify(interactionLog, null, 2));
  } catch (error) {
    stream.markdown(`❌ Error: ${String(error)}`);
  }
}

/**
 * Command: Test chat participant
 * Simulates what happens when user sends a message
 */
async function testChatParticipantCommand(): Promise<void> {
  if (!participantRegistered) {
    vscode.window.showErrorMessage(
      "Chat participant not yet registered. Reload window."
    );
    return;
  }

  const input = await vscode.window.showInputBox({
    prompt: "Enter test message for chat participant",
    value: "What can you help me with?",
  });

  if (!input) return;

  // Log the test
  const testLog = {
    test: "manual_chat_test",
    userInput: input,
    timestamp: new Date().toISOString(),
    participantRegistered: true,
  };

  const testFile = path.join(
    workspaceDir,
    "DEMO_CHAT_PARTICIPANT_TEST.json"
  );
  fs.writeFileSync(testFile, JSON.stringify(testLog, null, 2));

  vscode.window.showInformationMessage(
    `✓ Test logged to ${path.basename(testFile)}`
  );
  console.log("DEMO: Chat Participant Test");
  console.log(JSON.stringify(testLog, null, 2));
}

/**
 * Command: Verify registration
 */
async function verifyRegistrationCommand(): Promise<void> {
  const result = {
    success: participantRegistered,
    test: "participant_registration",
    timestamp: new Date().toISOString(),
    details: {
      participantId: "@demo",
      registered: participantRegistered,
      interactionCount: interactionLog.length,
      handlerFunction: "handleChatRequest",
    },
  };

  const testFile = path.join(
    workspaceDir,
    "DEMO_PARTICIPANT_REGISTRATION.json"
  );
  fs.writeFileSync(testFile, JSON.stringify(result, null, 2));

  vscode.window.showInformationMessage(
    `✓ Registration status: ${participantRegistered ? "ACTIVE" : "INACTIVE"}`
  );
  console.log("DEMO: Chat Participant Registration");
  console.log(JSON.stringify(result, null, 2));
}

export function activate(context: vscode.ExtensionContext) {
  console.log("✓ Chat Participant Demo activated");

  // Create and register the chat participant
  try {
    const participant = vscode.chat.createChatParticipant(
      "demo.chatParticipant",
      handleChatRequest
    );

    // Set metadata
    participant.iconPath = new vscode.ThemeIcon("lightbulb");

    participantRegistered = true;

    console.log("✓ Chat participant 'demo' registered successfully");
    console.log(
      "   Usage: In VSCode Chat, type '@demo' to interact with this participant"
    );

    // Log registration
    const registration = {
      timestamp: new Date().toISOString(),
      event: "participant_registered",
      participantId: "demo.chatParticipant",
      status: "active",
    };
    interactionLog.push(registration);
  } catch (error) {
    console.error("Failed to register chat participant:", error);
    participantRegistered = false;
  }

  // Register commands
  context.subscriptions.push(
    vscode.commands.registerCommand(
      "demo.chatParticipant.test",
      testChatParticipantCommand
    ),
    vscode.commands.registerCommand(
      "demo.chatParticipant.verifyRegistration",
      verifyRegistrationCommand
    )
  );

  // Show welcome message
  vscode.window.showInformationMessage(
    "Demo Chat Participant ready! Use @demo in VSCode Chat"
  );
}

export function deactivate() {
  // Save final log
  if (interactionLog.length > 0) {
    fs.writeFileSync(logFile, JSON.stringify(interactionLog, null, 2));
    console.log(`✓ Chat log saved to ${path.basename(logFile)}`);
  }
}
