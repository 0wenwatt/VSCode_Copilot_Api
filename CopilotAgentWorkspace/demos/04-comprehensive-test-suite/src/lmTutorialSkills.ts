/**
 * LM API Tutorial Skills
 * 
 * Demonstrates Language Model API usage:
 * - Generate completions
 * - Stream responses
 * - Count tokens
 * - Handle errors
 */

interface CompletionResponse {
  text: string;
  model: string;
  tokensUsed?: number;
  finishReason?: string;
}

interface StreamToken {
  token: string;
  accumulated: string;
}

interface TokenCountResponse {
  tokensNeeded: number;
  tokensUsed: number;
  tokensRemaining: number;
}

// ============================================================================
// SKILL 1: GENERATE CODE COMPLETION
// ============================================================================

/**
 * Uses LM API to generate code snippets
 * This would call vscode.lm.selectChatModels() and invoke them
 */
export const generateCodeCompletionSkill = {
  name: 'lmtutorial.generateCompletion',
  description: 'Generate code completion using the Language Model API',

  parameters: {
    type: 'object',
    properties: {
      prompt: {
        type: 'string',
        description: 'Code or description to complete'
      },
      language: {
        type: 'string',
        enum: ['python', 'javascript', 'typescript', 'java'],
        description: 'Programming language'
      },
      style: {
        type: 'string',
        enum: ['function', 'class', 'snippet'],
        description: 'Type of code to generate'
      }
    },
    required: ['prompt', 'language']
  },

  async invoke(input: any): Promise<CompletionResponse> {
    const { prompt, language, style = 'function' } = input;

    // Simulated completions (in real implementation, would call vscode.lm API)
    const templateCompletions: Record<string, string> = {
      'python_function': `def process_data(items):
    """Process a list of items and return results."""
    results = []
    for item in items:
        if item and len(str(item)) > 0:
            results.append(item.upper() if isinstance(item, str) else item)
    return results`,

      'javascript_function': `function processData(items) {
  // Process array items and return transformed results
  return items
    .filter(item => item != null)
    .map(item => typeof item === 'string' ? item.toUpperCase() : item);
}`,

      'typescript_class': `class DataProcessor {
  private data: Array<any> = [];

  constructor(initialData?: Array<any>) {
    if (initialData) {
      this.data = initialData;
    }
  }

  process(): Array<any> {
    return this.data.map(item => ({
      ...item,
      processed: true,
      timestamp: new Date()
    }));
  }
}`,

      'java_function': `public static List<String> processData(List<String> items) {
    return items.stream()
        .filter(item -> item != null && !item.isEmpty())
        .map(String::toUpperCase)
        .collect(Collectors.toList());
}`
    };

    const key = `${language}_${style}`;
    const completion = templateCompletions[key] || templateCompletions['python_function'];

    return {
      text: completion,
      model: 'claude-3-5-sonnet',
      tokensUsed: Math.floor(completion.length / 4),
      finishReason: 'stop'
    };
  }
};

// ============================================================================
// SKILL 2: STREAM RESPONSE
// ============================================================================

/**
 * Demonstrates streaming responses from LM API
 */
export const streamResponseSkill = {
  name: 'lmtutorial.streamResponse',
  description: 'Stream a response token-by-token from the language model',

  parameters: {
    type: 'object',
    properties: {
      prompt: {
        type: 'string',
        description: 'Prompt to stream response for'
      },
      maxTokens: {
        type: 'number',
        description: 'Maximum tokens to stream',
        default: 100
      }
    },
    required: ['prompt']
  },

  async invoke(input: any): Promise<object> {
    const { prompt, maxTokens = 100 } = input;

    // Simulated streaming response
    const streamedText = `Based on your request: "${prompt.substring(0, 50)}..."

Here's a detailed response:
1. This demonstrates the streaming capability of the Language Model API
2. Tokens are sent one at a time as they're generated
3. This is useful for real-time feedback in the UI
4. You can show a loading indicator and update as tokens arrive

The streaming completes when the model finishes or token limit is reached.`;

    const tokens = streamedText.split(/(\s+)/).filter((t: string) => t.trim());

    return {
      status: 'streaming_complete',
      totalTokensStreamed: tokens.length,
      maxTokensRequested: maxTokens,
      completionReason: tokens.length >= maxTokens ? 'max_tokens' : 'stop',
      preview: `${streamedText.substring(0, 200)}...`
    };
  }
};

// ============================================================================
// SKILL 3: COUNT TOKENS
// ============================================================================

/**
 * Estimates token usage before making requests
 */
export const countTokensSkill = {
  name: 'lmtutorial.countTokens',
  description: 'Count tokens in a prompt to estimate API usage',

  parameters: {
    type: 'object',
    properties: {
      text: {
        type: 'string',
        description: 'Text to count tokens for'
      }
    },
    required: ['text']
  },

  async invoke(input: any): Promise<TokenCountResponse> {
    const { text } = input;

    // Rough estimation: ~1 token per 4 characters (Anthropic Claude tokens)
    const estimatedTokens = Math.ceil(text.length / 4);
    const contextWindow = 200000; // Claude 3.5 Sonnet context window

    return {
      tokensNeeded: estimatedTokens,
      tokensUsed: estimatedTokens,
      tokensRemaining: contextWindow - estimatedTokens
    };
  }
};

// ============================================================================
// SKILL 4: ERROR HANDLING
// ============================================================================

/**
 * Demonstrates error handling patterns for LM API
 */
export const handleLMErrorSkill = {
  name: 'lmtutorial.handleError',
  description: 'Handle and recover from Language Model API errors',

  parameters: {
    type: 'object',
    properties: {
      errorType: {
        type: 'string',
        enum: ['rate_limit', 'invalid_model', 'context_length', 'no_models'],
        description: 'Type of error to handle'
      }
    },
    required: ['errorType']
  },

  async invoke(input: any) {
    const { errorType } = input;

    const errorHandling: Record<string, object> = {
      rate_limit: {
        error: 'Rate limit exceeded',
        statusCode: 429,
        retryAfter: 60,
        recommendation: 'Wait 60 seconds before retrying or implement exponential backoff',
        recoveryCode: `
// Implement exponential backoff
async function retryWithBackoff(fn, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      if (error.statusCode !== 429) throw error;
      const delay = Math.pow(2, i) * 1000; // 1s, 2s, 4s
      await new Promise(r => setTimeout(r, delay));
    }
  }
}
        `.trim()
      },
      invalid_model: {
        error: 'Model not available or invalid',
        statusCode: 404,
        recommendation: 'Verify model ID with vscode.lm.selectChatModels()',
        recoveryCode: `
// Verify available models
const models = await vscode.lm.selectChatModels();
if (models.length === 0) {
  console.error('No language models available');
  return;
}
const model = models[0]; // Use first available model
        `.trim()
      },
      context_length: {
        error: 'Prompt exceeds model context length',
        statusCode: 400,
        recommendation: 'Reduce prompt size or use summarization',
        recoveryCode: `
// Truncate or summarize long prompts
function truncatePrompt(prompt, maxTokens) {
  const tokens = prompt.split(/\s+/);
  return tokens.slice(0, maxTokens).join(' ') + '...';
}
        `.trim()
      },
      no_models: {
        error: 'No language models available',
        statusCode: 503,
        recommendation: 'Install language model extension or check subscriptions',
        recoveryCode: `
// Check model availability and notify user
const models = await vscode.lm.selectChatModels();
if (models.length === 0) {
  vscode.window.showWarningMessage(
    'No language models available. Install a language model extension.'
  );
  return;
}
        `.trim()
      }
    };

    return errorHandling[errorType] || errorHandling['no_models'];
  }
};

// ============================================================================
// SKILL 5: SELECT AND CONFIGURE MODEL
// ============================================================================

/**
 * Demonstrates model selection and configuration
 */
export const configureModelSkill = {
  name: 'lmtutorial.configureModel',
  description: 'Select and configure a language model for use',

  parameters: {
    type: 'object',
    properties: {
      preference: {
        type: 'string',
        enum: ['fastest', 'best-quality', 'most-affordable'],
        description: 'Model selection preference'
      }
    }
  },

  async invoke(input: any) {
    const { preference = 'best-quality' } = input as { preference?: string };

    const modelConfigs: Record<string, any> = {
      fastest: {
        recommended: 'claude-3-haiku',
        context: 200000,
        speedRating: '⚡⚡⚡ Very Fast',
        costRating: '💰 Affordable',
        qualityRating: '⭐⭐⭐ Good',
        useCases: ['Quick code suggestions', 'Real-time completions', 'Fast iteration']
      },
      'best-quality': {
        recommended: 'claude-3-5-sonnet',
        context: 200000,
        speedRating: '⚡⚡ Fast',
        costRating: '💰💰 Moderate',
        qualityRating: '⭐⭐⭐⭐⭐ Excellent',
        useCases: ['Complex code generation', 'Architecture design', 'Detailed explanations']
      },
      'most-affordable': {
        recommended: 'claude-3-haiku',
        context: 200000,
        speedRating: '⚡⚡ Fast',
        costRating: '💰 Very Affordable',
        qualityRating: '⭐⭐⭐ Good',
        useCases: ['Bulk processing', 'Development testing', 'High-volume tasks']
      }
    };

    const config = modelConfigs[preference as string] || modelConfigs['best-quality'];

    return {
      ...config,
      setupCode: `
const models = await vscode.lm.selectChatModels({
  vendor: 'anthropic',
  id: '${config.recommended}'
});

if (models.length === 0) {
  throw new Error('Required model not available');
}

const selectedModel = models[0];
const messages = [
  { role: 'user', content: 'Your prompt here' }
];

const response = await selectedModel.sendRequest(messages);
console.log(response);
      `.trim()
    };
  }
};

// ============================================================================
// EXPORTS
// ============================================================================

export const lmTutorialSkills = {
  generateCompletion: generateCodeCompletionSkill,
  streamResponse: streamResponseSkill,
  countTokens: countTokensSkill,
  handleError: handleLMErrorSkill,
  configureModel: configureModelSkill
};

export default lmTutorialSkills;
