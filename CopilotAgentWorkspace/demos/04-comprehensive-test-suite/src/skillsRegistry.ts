/**
 * SKILLS REGISTRATION GUIDE
 * 
 * This file demonstrates how to register all skills with the VSCode Copilot API.
 * 
 * Skills are tools that extend Copilot Chat capabilities by providing:
 * - Custom commands and actions
 * - Data processing and transformation
 * - API integrations
 * - Context-specific operations
 * 
 * Registration happens in the extension's activate() function.
 */

import * as vscode from 'vscode';
import { tutorSkills } from './tutorSkills';
import { lmTutorialSkills } from './lmTutorialSkills';

// ============================================================================
// SKILL REGISTRATION API
// ============================================================================

/**
 * Core skill registration interface
 * Each skill has:
 * - name: Unique identifier
 * - description: What the skill does
 * - parameters: Input schema (JSON Schema)
 * - invoke: Async function that executes the skill
 */
interface Skill {
  name: string;
  description: string;
  parameters: {
    type: string;
    properties: Record<string, any>;
    required?: string[];
  };
  invoke(input: any): Promise<any>;
}

// ============================================================================
// SKILL 1: TUTOR SKILLS - REGISTER WITH CHAT PARTICIPANT
// ============================================================================

/**
 * Example: Register tutor skills in chat-tutorial extension
 * 
 * These skills enable the @tutor participant to:
 * - Generate exercises
 * - Provide hints
 * - Explain solutions
 */
export async function registerTutorSkills(context: vscode.ExtensionContext): Promise<any[]> {
  const tutorSkillsArray = [
    tutorSkills.generateExercise,
    tutorSkills.provideHint,
    tutorSkills.explainSolution,
    tutorSkills.suggestNext
  ];

  // In actual implementation, register with:
  // context.subscriptions.push(
  //   vscode.chat.registerChatParticipant('tutor', new TutorChatParticipant(tutorSkillsArray))
  // );

  console.log(`✅ Registered ${tutorSkillsArray.length} tutor skills`);
  return tutorSkillsArray;
}

// ============================================================================
// SKILL 2: LM TUTORIAL SKILLS - REGISTER WITH LM API
// ============================================================================

/**
 * Example: Register LM API skills in lm-api-tutorial extension
 *
 * These skills demonstrate:
 * - Code generation via LM API
 * - Token counting and estimation
 * - Error handling patterns
 * - Model selection
 */
export async function registerLMTutorialSkills(context: vscode.ExtensionContext): Promise<any[]> {
  const lmSkillsArray = [
    lmTutorialSkills.generateCompletion,
    lmTutorialSkills.streamResponse,
    lmTutorialSkills.countTokens,
    lmTutorialSkills.handleError,
    lmTutorialSkills.configureModel
  ];

  // In actual implementation, these would be registered as tools:
  // Try to find available language models
  // const models = await vscode.lm.selectChatModels();
  // models.forEach(model => {
  //   lmSkillsArray.forEach(skill => {
  //     // Skills are available as @command actions in chat
  //   });
  // });

  console.log(`✅ Registered ${lmSkillsArray.length} LM tutorial skills`);
  return lmSkillsArray;
}

// ============================================================================
// SKILL REGISTRATION PATTERN - GENERAL TEMPLATE
// ============================================================================

/**
 * Generic skill registration function
 * Use this pattern to register any skill set
 */
export async function registerSkillSet(
  context: vscode.ExtensionContext,
  skillName: string,
  skills: Skill[]
) {
  const registered = [];

  for (const skill of skills) {
    try {
      // Validate skill structure
      if (!skill.name || !skill.description || !skill.invoke) {
        throw new Error(`Invalid skill structure: ${skill.name}`);
      }

      // Register skill
      // The actual registration depends on the extension type
      registered.push({
        name: skill.name,
        description: skill.description,
        status: 'registered'
      });

      console.log(`   ✅ ${skill.name}: ${skill.description}`);
    } catch (error) {
      console.error(`   ❌ Failed to register ${skill.name}:`, error);
    }
  }

  console.log(`\n📦 Registered ${skillName}: ${registered.length}/${skills.length} skills\n`);
  return registered;
}

// ============================================================================
// SKILLS DISCOVERY - HOW TO FIND AVAILABLE SKILLS
// ============================================================================

/**
 * Discover and list all available skills in the workspace
 */
export async function discoverAvailableSkills() {
  const discoveredSkills = {
    chatTutorial: {
      participant: '@tutor',
      skills: [
        'tutor.generateExercise',
        'tutor.provideHint',
        'tutor.explainSolution',
        'tutor.suggestNext'
      ]
    },
    lmApiTutorial: {
      participant: '@lm',
      skills: [
        'lmtutorial.generateCompletion',
        'lmtutorial.streamResponse',
        'lmtutorial.countTokens',
        'lmtutorial.handleError',
        'lmtutorial.configureModel'
      ]
    },
    chatSample: {
      participant: '@cat',
      skills: [
        'cat.meow',
        'cat.purr',
        'cat.fetch'
      ]
    },
    contextSample: {
      contextProviders: [
        'github-issues',
        'github-pull-requests',
        'github-running-workflows'
      ]
    }
  };

  return discoveredSkills;
}

// ============================================================================
// HELPER: VALIDATE SKILL PARAMETERS
// ============================================================================

/**
 * Validate skill input parameters against the defined schema
 */
export function validateSkillParameters(skill: Skill, input: any): boolean {
  const { properties, required = [] } = skill.parameters;

  // Check required parameters
  for (const requiredParam of required) {
    if (!(requiredParam in input)) {
      console.error(`Missing required parameter: ${requiredParam}`);
      return false;
    }
  }

  // Validate parameter types
  for (const [key, value] of Object.entries(input)) {
    if (!(key in properties)) {
      console.warn(`Unknown parameter: ${key}`);
    }

    const paramSchema = properties[key];
    if (paramSchema.enum && !paramSchema.enum.includes(value)) {
      console.error(`Invalid value for ${key}: ${value}. Expected one of: ${paramSchema.enum.join(', ')}`);
      return false;
    }
  }

  return true;
}

// ============================================================================
// EXAMPLE: INVOKING A SKILL PROGRAMMATICALLY
// ============================================================================

/**
 * Example of how to invoke a skill from code
 */
export async function invokeSkillExample(): Promise<any> {
  // Get the tutor skill
  const generateExerciseSkill = tutorSkills.generateExercise;

  // Prepare parameters
  const input = {
    difficulty: 'beginner',
    language: 'python',
    topic: 'loops'
  };

  // Validate parameters
  if (!validateSkillParameters(generateExerciseSkill, input)) {
    console.error('Invalid parameters');
    return;
  }

  // Invoke the skill
  try {
    const result = await generateExerciseSkill.invoke(input);
    console.log('Skill result:', result);
    return result;
  } catch (error) {
    console.error('Skill invocation failed:', error);
  }
}

// ============================================================================
// INTEGRATION CHECKLIST
// ============================================================================

/**
 * Checklist for integrating skills into a VSCode extension
 */
export const SKILLS_INTEGRATION_CHECKLIST = `
✅ SKILLS INTEGRATION CHECKLIST

1. DISCOVERY PHASE
   [ ] Identify all skills in your extension
   [ ] Validate skill structure (name, description, parameters, invoke)
   [ ] Create Skill[] array for each skill set

2. REGISTRATION PHASE
   [ ] Add skill registration in extension's activate() function
   [ ] Register skills with appropriate VSCode API:
       - ChatParticipant for chat participants
       - vscode.lm for language model skills
       - vscode.chat for chat context providers
       - vscode.commands for command-based skills
   [ ] Handle skill registration errors gracefully

3. VALIDATION PHASE
   [ ] Validate skill parameters match JSON Schema
   [ ] Test skill invocation with sample inputs
   [ ] Verify skill return types match documented output

4. INTEGRATION PHASE
   [ ] Make skills discoverable to users (slash commands, chat participants)
   [ ] Add telemetry for skill usage
   [ ] Document each skill with examples
   [ ] Add TypeScript types for skill inputs/outputs

5. TESTING PHASE
   [ ] Unit test each skill's invoke() function
   [ ] Integration test skills with VSCode API
   [ ] Manual test in VSCode chat interface
   [ ] Test error handling and edge cases

6. DOCUMENTATION PHASE
   [ ] Create / update README with skill list
   [ ] Add examples for each skill
   [ ] Document parameter requirements
   [ ] Include troubleshooting tips

7. DEPLOYMENT PHASE
   [ ] Add skills to package.json contributes
   [ ] Test in clean VSCode installation
   [ ] Verify telemetry is working
   [ ] Monitor for skill usage and errors
`;

// ============================================================================
// EXPORT SUMMARY
// ============================================================================

export const skillsRegistry = {
  // Skill sets
  tutorSkills,
  lmTutorialSkills,

  // Registration functions
  registerTutorSkills,
  registerLMTutorialSkills,
  registerSkillSet,

  // Discovery
  discoverAvailableSkills,

  // Utilities
  validateSkillParameters,
  invokeSkillExample,

  // Checklist
  SKILLS_INTEGRATION_CHECKLIST
} as any;

export default skillsRegistry;
