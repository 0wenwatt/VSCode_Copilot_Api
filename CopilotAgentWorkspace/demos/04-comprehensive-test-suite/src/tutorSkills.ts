/**
 * Tutor Skills
 * 
 * Implements the capabilities advertised in .instructions.md:
 * - Generate exercises
 * - Provide hints
 * - Explain solutions
 */

// Type definitions for skill outputs
interface ExerciseOutput {
  title: string;
  difficulty: string;
  objective: string;
  description: string;
  starterCode?: string;
  requirements: string[];
}

interface HintOutput {
  steps: string[];
  concept: string;
  resources?: string[];
  encouragement: string;
}

interface ExplanationOutput {
  title: string;
  walkthrough: string[];
  keyConcepts: string[];
  alternatives?: string[];
}

// ============================================================================
// SKILL 1: GENERATE EXERCISE
// ============================================================================

/**
 * Generates coding exercises at specified difficulty level
 * 
 * This would be registered with vscode.lm.registerTool()
 */
export const generateExerciseSkill = {
  name: 'tutor.generateExercise',
  description: 'Generate a coding exercise at the specified difficulty level',
  
  parameters: {
    type: 'object',
    properties: {
      difficulty: {
        type: 'string',
        enum: ['beginner', 'intermediate', 'advanced'],
        description: 'Difficulty level for the exercise'
      },
      language: {
        type: 'string',
        enum: ['python', 'javascript', 'java', 'cpp', 'rust'],
        description: 'Programming language for exercise'
      },
      topic: {
        type: 'string',
        description: 'Topic area (e.g., "loops", "recursion", "data-structures")'
      }
    },
    required: ['difficulty', 'language']
  },

  async invoke(input: any): Promise<ExerciseOutput> {
    const { difficulty, language, topic } = input;

    // Exercise database (simplified - would be comprehensive in production)
    const exercises: Record<string, Record<string, ExerciseOutput>> = {
      beginner: {
        loops: {
          title: 'FizzBuzz',
          difficulty: 'Beginner',
          objective: 'Learn loops and conditionals',
          description: 'Write a program that prints numbers 1-100. For multiples of 3 print "Fizz", for multiples of 5 print "Buzz", for both print "FizzBuzz".',
          starterCode: language === 'python' 
            ? 'def fizzbuzz():\n    pass'
            : 'function fizzbuzz() {\n    // Your code here\n}',
          requirements: [
            'Use a loop from 1 to 100',
            'Check divisibility using modulo operator',
            'Handle multiple conditions'
          ]
        },
        variables: {
          title: 'Temperature Converter',
          difficulty: 'Beginner',
          objective: 'Learn variable assignment and arithmetic',
          description: 'Convert a temperature from Celsius to Fahrenheit using the formula: F = (C × 9/5) + 32',
          starterCode: language === 'python'
            ? 'celsius = 0\n# Your conversion here'
            : 'let celsius = 0;\n// Your conversion here',
          requirements: [
            'Accept input in Celsius',
            'Apply conversion formula',
            'Output result'
          ]
        }
      },
      intermediate: {
        recursion: {
          title: 'Fibonacci Sequence',
          difficulty: 'Intermediate',
          objective: 'Learn recursion and memoization',
          description: 'Write a function that efficiently calculates the nth Fibonacci number using recursion.',
          starterCode: language === 'python'
            ? 'def fibonacci(n):\n    pass'
            : 'function fibonacci(n) {\n    // Your code here\n}',
          requirements: [
            'Handle base cases',
            'Implement recursive logic',
            'Consider performance optimization'
          ]
        },
        'data-structures': {
          title: 'Reverse a List',
          difficulty: 'Intermediate',
          objective: 'Learn array/list manipulation',
          description: 'Implement a function that reverses a list in-place without using built-in reverse methods.',
          requirements: [
            'Use two pointers approach',
            'Modify array in-place',
            'Handle edge cases'
          ]
        }
      },
      advanced: {
        algorithms: {
          title: 'Quicksort Implementation',
          difficulty: 'Advanced',
          objective: 'Master sorting algorithms',
          description: 'Implement the Quicksort algorithm and analyze its time complexity.',
          requirements: [
            'Implement partition function',
            'Handle worst-case scenario',
            'Analyze O(n log n) performance'
          ]
        }
      }
    };

    // Get exercise, with fallback
    const topicExercises = exercises[difficulty] || exercises['beginner'];
    const exercise = topicExercises[topic || 'loops'] || Object.values(topicExercises)[0];

    return exercise;
  }
};

// ============================================================================
// SKILL 2: PROVIDE HINT
// ============================================================================

/**
 * Provides guided hints toward solution without spoiling answer
 */
export const provideHintSkill = {
  name: 'tutor.provideHint',
  description: 'Provide a hint for the current exercise',

  parameters: {
    type: 'object',
    properties: {
      exercise: {
        type: 'string',
        description: 'Name of the exercise'
      },
      stage: {
        type: 'number',
        description: 'Hint stage (1-3, with 1 being gentler than 3)'
      }
    }
  },

  async invoke(input: any): Promise<HintOutput> {
    const { exercise = 'FizzBuzz', stage = 1 } = input;

    // Hint progressions (stage 1 = gentle, stage 3 = detailed)
    const hints: Record<string, Record<number, HintOutput>> = {
      'FizzBuzz': {
        1: {
          steps: [
            '🎯 Think about the structure: You need to repeat something many times',
            '💡 Which type of loop lets you go from 1 to 100?',
            '🤔 What operation finds if a number is divisible?'
          ],
          concept: 'Loops and the modulo operator (%)',
          encouragement: 'You\'ve got this! Start with the loop structure.'
        },
        2: {
          steps: [
            '1. Use a for loop: `for i in range(1, 101)` or `for (let i = 1; i <= 100; i++)`',
            '2. Check divisibility: `i % 3 == 0` means divisible by 3',
            '3. You need multiple conditions: check 15 first, then 3, then 5'
          ],
          concept: 'Conditional logic and operator precedence',
          resources: ['https://docs.python.org/3/tutorial/controlflow.html'],
          encouragement: 'Almost there! Think about the order of your if statements.'
        },
        3: {
          steps: [
            'Here\'s the pattern:',
            'for i in range(1, 101):',
            '    if i % 15 == 0: print("FizzBuzz")  # Check this FIRST',
            '    elif i % 3 == 0: print("Fizz")',
            '    elif i % 5 == 0: print("Buzz")',
            '    else: print(i)',
            'Why check 15 first? Because 15 is divisible by both 3 and 5!'
          ],
          concept: 'Order of conditions matters in if/elif chains',
          encouragement: 'You\'ve learned an important lesson about condition ordering!'
        }
      }
    };

    const exerciseHints = hints[exercise] || hints['FizzBuzz'];
    return exerciseHints[stage] || exerciseHints[1];
  }
};

// ============================================================================
// SKILL 3: EXPLAIN SOLUTION
// ============================================================================

/**
 * Walks through solution explanation
 */
export const explainSolutionSkill = {
  name: 'tutor.explainSolution',
  description: 'Explain the solution to an exercise',

  parameters: {
    type: 'object',
    properties: {
      exercise: {
        type: 'string',
        description: 'Name of the exercise'
      },
      language: {
        type: 'string',
        enum: ['python', 'javascript'],
        description: 'Programming language for explanation'
      }
    }
  },

  async invoke(input: any): Promise<ExplanationOutput> {
    const { exercise = 'FizzBuzz', language = 'python' } = input;

    const solutions: Record<string, Record<string, ExplanationOutput>> = {
      'FizzBuzz': {
        python: {
          title: 'FizzBuzz Solution Walkthrough',
          walkthrough: [
            '**Line 1: The Loop**\n`for i in range(1, 101):`\nWe use `range(1, 101)` to give us numbers 1-100. The `range()` function creates a sequence.',
            
            '**Line 2-3: Check for both 3 and 5**\n`if i % 15 == 0:`\n`print("FizzBuzz")`\nWe check this FIRST because if a number is divisible by 15, it\'s divisible by both 3 AND 5. We must check this before checking 3 or 5 alone!',
            
            '**Line 4-5: Check for 3 only**\n`elif i % 3 == 0:`\n`print("Fizz")`\nIf we get here, we already know it\'s not divisible by 15, so this is divisible by 3 but not 5.',
            
            '**Line 6-7: Check for 5 only**\n`elif i % 5 == 0:`\n`print("Buzz")`\nSimilarly, if we get here, it\'s divisible by 5 but not 3.',
            
            '**Line 8-9: No match**\n`else:`\n`print(i)`\nIf none of the conditions matched, just print the number itself.'
          ],
          keyConcepts: [
            'Loop iteration with range()',
            'Modulo operator (%) for divisibility',
            'Order of conditions in if/elif chains',
            'That 15 is the LCM of 3 and 5, so check it first!'
          ],
          alternatives: [
            'You could use a while loop instead of for',
            'You could use a list comprehension (more advanced)',
            'You could use multiple if statements instead of elif (less efficient)'
          ]
        },
        javascript: {
          title: 'FizzBuzz Solution Walkthrough',
          walkthrough: [
            '**Line 1: The Loop**\n`for (let i = 1; i <= 100; i++)`\nWe start at 1, continue while i is <= 100, and increment i each iteration.',
            
            '**Lines 2-4: Check for both**\n`if (i % 15 === 0)`\n`console.log("FizzBuzz");`\nWe check for 15 first (the LCM of 3 and 5).',
            
            '**Lines 5-7: Check for 3**\n`else if (i % 3 === 0)`\n`console.log("Fizz");`\nIf not 15, check if divisible by 3.',
            
            '**Lines 8-10: Check for 5**\n`else if (i % 5 === 0)`\n`console.log("Buzz");`\nIf not 15 or 3, check if divisible by 5.',
            
            '**Lines 11-13: Default**\n`else`\n`console.log(i);`\nOtherwise, print the number.'
          ],
          keyConcepts: [
            'For loop syntax: init; condition; increment',
            'Modulo operator (%) in JavaScript',
            'The importance of === (strict equality)',
            'Logical flow with if/else if/else'
          ],
          alternatives: [
            'Array.from(Array(100), (_, i) => i + 1) with map()',
            'While loop instead of for loop',
            'Ternary operator for more compact code'
          ]
        }
      }
    };

    const solutionData = solutions[exercise]?.[language];
    return solutionData || {
      title: 'Solution Not Found',
      walkthrough: ['Please specify a valid exercise and language.'],
      keyConcepts: []
    };
  }
};

// ============================================================================
// SKILL 4: SUGGEST NEXT EXERCISE
// ============================================================================

/**
 * Suggests the next exercise based on progress
 */
export const suggestNextExerciseSkill = {
  name: 'tutor.suggestNext',
  description: 'Suggest the next exercise based on current progress',

  parameters: {
    type: 'object',
    properties: {
      currentExercise: {
        type: 'string',
        description: 'Current exercise completed'
      },
      difficultyLevel: {
        type: 'string',
        enum: ['beginner', 'intermediate', 'advanced'],
        description: 'Current difficulty level'
      }
    }
  },

  async invoke(input: any) {
    const { currentExercise = 'FizzBuzz', difficultyLevel = 'beginner' } = input;

    const progressPath: Record<string, Record<string, any>> = {
      beginner: {
        'FizzBuzz': {
          next: 'Reverse a String',
          difficulty: 'beginner',
            reason: 'Now that you understand loops and conditionals, practice with string manipulation!'
        }
      },
      intermediate: {
        'Reverse a String': {
          next: 'Fibonacci Sequence',
          difficulty: 'intermediate',
          reason: 'Time to learn recursion! Fibonacci is the classic example.'
        }
      },
      advanced: {
        'Fibonacci Sequence': {
          next: 'Quicksort Implementation',
          difficulty: 'advanced',
          reason: 'Master sorting algorithms and time complexity analysis.'
        }
      }
    };

    const nextExercise = progressPath[difficultyLevel as string]?.[currentExercise];

    return {
      status: 'success',
      exerciseCompleted: currentExercise,
      suggestedNext: nextExercise?.next || 'Choose any intermediate level exercise',
      difficulty: nextExercise?.difficulty || 'intermediate',
      reason: nextExercise?.reason || 'You\'ve completed great exercises! Choose your next challenge.',
      message: `🎓 Great job completing "${currentExercise}"! Next, try "${nextExercise?.next || 'an intermediate exercise'}" - ${nextExercise?.reason || 'to continue learning'}`
    };
  }
};

// ============================================================================
// EXPORTS
// ============================================================================

export const tutorSkills = {
  generateExercise: generateExerciseSkill,
  provideHint: provideHintSkill,
  explainSolution: explainSolutionSkill,
  suggestNext: suggestNextExerciseSkill
};

export default tutorSkills;
