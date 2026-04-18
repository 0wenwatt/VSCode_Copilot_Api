```
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║               🧪 VSCODE COPILOT SKILLS - LIVE TESTING GUIDE                ║
║                                                                            ║
║                Test Skills in Real VSCode Copilot Chat                     ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝


📋 TABLE OF CONTENTS
═══════════════════════════════════════════════════════════════════════════
1. Quick Start (5 minutes)
2. Detailed Testing Procedure
3. Visual Test Results
4. Secret Phrase Verification Test
5. Troubleshooting
6. Expected Outputs


🚀 QUICK START (5 MINUTES)
═══════════════════════════════════════════════════════════════════════════

STEP 1: Open VS Code with chat-tutorial
─────────────────────────────────────────
Run this command in PowerShell:

    code --extensionDevelopmentPath="c:\Users\Owen\Desktop\Brogramming\VSCode_Copilot_Api\vscode-extension-samples\chat-tutorial"

Expected: VS Code opens with chat-tutorial extension loaded

STEP 2: Open Copilot Chat
─────────────────────────
Press: Ctrl+Shift+I (or Cmd+Shift+I on Mac)

Expected: Chat panel appears on the right side

STEP 3: Run Test Command
────────────────────────
In the chat input, type EXACTLY:

    @tutor /exercise difficulty:beginner language:python topic:loops

Then press Enter.

STEP 4: Verify Success
──────────────────────
Expected response should include:
✅ Title: "FizzBuzz"
✅ Objective: Learning loops and conditionals
✅ Description: Print numbers with Fizz/Buzz logic
✅ Requirements: List of 3+ bullet points
✅ No errors in Debug Console (Ctrl+Shift+Y)

Done! The skill is working! ✅


📊 DETAILED TESTING PROCEDURE
═══════════════════════════════════════════════════════════════════════════

TEST 1: GENERATE EXERCISE (@tutor /exercise)
──────────────────────────────────────────────

Command:
    @tutor /exercise difficulty:beginner language:python topic:loops

Expected Output:
┌────────────────────────────────────────────────────────────────────┐
│ Title: FizzBuzz                                                    │
│ Difficulty: Beginner                                               │
│ Objective: Learn loops and conditionals                            │
│ Description: Write a program that prints numbers 1-100. For       │
│   multiples of 3 print "Fizz", for multiples of 5 print "Buzz",   │
│   for both print "FizzBuzz".                                       │
│ Starter Code (Python):                                            │
│   def fizzbuzz():                                                  │
│     pass                                                           │
│ Requirements:                                                      │
│   • Use a loop from 1 to 100                                       │
│   • Check divisibility using modulo operator                       │
│   • Handle multiple conditions                                     │
└────────────────────────────────────────────────────────────────────┘

Validation Checklist:
[ ] Response appears in chat
[ ] All fields are present
[ ] Code example is shown
[ ] No console errors (Ctrl+Shift+Y)

✅ SUCCESS: Exercise skill is working!


TEST 2: GET HINT (@tutor /hint)
─────────────────────────────────

Command:
    @tutor /hint stage:1

Expected Output:
┌────────────────────────────────────────────────────────────────────┐
│ 🎯 Think about the structure: You need to repeat something many   │
│    times                                                           │
│ 💡 Which type of loop lets you go from 1 to 100?                  │
│ 🤔 What operation finds if a number is divisible?                 │
│                                                                    │
│ Concept: Loops and the modulo operator (%)                        │
│ Resources: [links if available]                                   │
│ Encouragement: You've got this! Start with the loop structure.    │
└────────────────────────────────────────────────────────────────────┘

Validation Checklist:
[ ] Hint is gentle (stage 1 should not reveal solution)
[ ] Concept is explained
[ ] Encouragement is provided

Bonus - Try Different Stages:
    @tutor /hint stage:2    ← More detailed hint
    @tutor /hint stage:3    ← Near-complete solution

Validation:
[ ] Stage 3 includes code snippets
[ ] Each stage progressively more detailed

✅ SUCCESS: Hint skill is working!


TEST 3: EXPLAIN SOLUTION (@tutor /explain)
────────────────────────────────────────────

Command:
    @tutor /explain exercise:FizzBuzz language:python

Expected Output:
┌────────────────────────────────────────────────────────────────────┐
│ FizzBuzz Solution Walkthrough                                      │
│                                                                    │
│ **Line 1: The Loop**                                               │
│ `for i in range(1, 101):`                                         │
│ We use range(1, 101) to give us numbers 1-100. The range()       │
│ function creates a sequence.                                       │
│                                                                    │
│ **Line 2-3: Check for both 3 and 5**                              │
│ `if i % 15 == 0:`                                                 │
│ `print("FizzBuzz")`                                               │
│ We check this FIRST because if a number is divisible by 15,      │
│ it's divisible by both 3 AND 5. We must check this before 3!    │
│                                                                    │
│ [... more lines explained ...]                                    │
│                                                                    │
│ Key Concepts:                                                      │
│   • Loop iteration with range()                                   │
│   • Modulo operator (%) for divisibility                          │
│   • Order of conditions matters in if/elif chains                 │
└────────────────────────────────────────────────────────────────────┘

Validation Checklist:
[ ] Solution is complete
[ ] Each line is numbered and explained
[ ] Key concepts highlighted
[ ] Order of checks explained

✅ SUCCESS: Explain skill is working!


TEST 4: SUGGEST NEXT EXERCISE (@tutor /next)
──────────────────────────────────────────────

Command:
    @tutor /next currentExercise:FizzBuzz difficultyLevel:beginner

Expected Output:
┌────────────────────────────────────────────────────────────────────┐
│ 🎓 Great job completing "FizzBuzz"!                               │
│ Next: Try "Reverse a String" - an intermediate level exercise    │
│ Reason: Now that you understand loops and conditionals, practice │
│   with string manipulation!                                       │
│                                                                    │
│ Status: success                                                    │
│ Exercise Completed: FizzBuzz                                      │
│ Suggested Next: Reverse a String                                  │
│ Difficulty: intermediate                                          │
│ Message: 🎓 Great job completing "FizzBuzz"! Next, try an         │
│   intermediate exercise...                                        │
└────────────────────────────────────────────────────────────────────┘

Validation Checklist:
[ ] Completion acknowledgment provided
[ ] Next exercise suggested
[ ] Difficulty increases (beginner → intermediate)
[ ] Reasoning is clear

✅ SUCCESS: Next skill is working!


TEST 5: LM API SKILLS (@lm /generate)
───────────────────────────────────────

Command:
    @lm /generate prompt:"sort an array" language:javascript style:function

Expected Output:
┌────────────────────────────────────────────────────────────────────┐
│ Generated Code:                                                    │
│                                                                    │
│ function processData(items) {                                     │
│   return items                                                    │
│     .filter(item => item != null)                                 │
│     .map(item => typeof item === 'string' ?                       │
│       item.toUpperCase() : item);                                 │
│ }                                                                  │
│                                                                    │
│ Model: claude-3-5-sonnet                                          │
│ Tokens Used: 42                                                   │
│ Finish Reason: stop                                               │
└────────────────────────────────────────────────────────────────────┘

Validation Checklist:
[ ] Code is generated
[ ] Model name shown
[ ] Token count displayed
[ ] Finish reason provided

✅ SUCCESS: LM skill is working!


TEST 6: TOKEN COUNTER (@lm /tokens)
─────────────────────────────────────

Command:
    @lm /tokens text:"How many tokens does this sentence use?"

Expected Output:
┌────────────────────────────────────────────────────────────────────┐
│ Tokens Needed: 10                                                  │
│ Tokens Used: 10                                                    │
│ Tokens Remaining: 199990                                           │
│                                                                    │
│ Note: Estimation based on ~1 token ≈ 4 characters                 │
└────────────────────────────────────────────────────────────────────┘

Validation Checklist:
[ ] Token count provided
[ ] Shows remaining in context window
[ ] Math is approximately correct

✅ SUCCESS: Token counter is working!


🔐 SECRET PHRASE VERIFICATION TEST
═══════════════════════════════════════════════════════════════════════════

This test proves skills are ACTUALLY BEING INVOKED (not cached)

What It Does:
└─ Each invocation generates a UNIQUE secret phrase
└─ Phrase includes random component + timestamp
└─ If phrase changes each time = proof of real invocation

How to Test:
────────────

STEP 1: First Invocation
    @tutor /secretTest testId:verification_1

Expected Output:
    🔐 SKILL_VERIFIED_verification_1_a1b2c3d_2025-04-11T15:30:45.123Z
    This message is UNIQUE and proves the skill was actually invoked


STEP 2: Second Invocation (Same Parameters)
    @tutor /secretTest testId:verification_1

Expected Output:
    🔐 SKILL_VERIFIED_verification_1_x9y8z7w_2025-04-11T15:30:52.456Z
    ⚠️ NOTICE: Random component changed! (a1b2c3d → x9y8z7w)
    ⚠️ NOTICE: Timestamp changed! (45.123Z → 52.456Z)


VERIFICATION CHECKLIST:
────────────────────────

🔴 FAILURE Signs (Cached Response):
   [ ] Same output on second invocation
   [ ] Random component identical
   [ ] Timestamp identical
   → If you see this: Cache is interfering

✅ SUCCESS Signs (Real Invocation):
   [ ] Different output each time
   [ ] Random component changes
   [ ] Timestamp increments
   [ ] You see the unique phrases
   → If you see this: SKILL IS DEFINITELY WORKING! 🎉


📊 VISUAL QUICK REFERENCE
═══════════════════════════════════════════════════════════════════════════

Expected Chat Interaction:

USER:           @tutor /exercise difficulty:beginner language:python
                ↓
COPILOT:        ✅ Recognizes @tutor participant
                ↓
RESPONSE:       📝 Title: FizzBuzz
                📝 Objective: Learn loops...
                📝 Description: Print 1-100 with Fizz/Buzz...
                📝 Requirements: [list]
                📝 Starter Code: [code]
                ↓
SUCCESS:        ✅ All fields present, no errors


📱 MULTI-TEST SESSION (10 MINUTES)
═══════════════════════════════════════════════════════════════════════════

Follow this sequence to thoroughly test all skills:

Time    | Command                                      | What to Check
─────────────────────────────────────────────────────────────────────
0:00    | @tutor /exercise difficulty:beginner        | Exercise appears
        | language:python topic:loops                 |
────────────────────────────────────────────────────────────────────
1:00    | @tutor /hint stage:1                        | Gentle hints shown
────────────────────────────────────────────────────────────────────
2:00    | @tutor /hint stage:2                        | More detailed
────────────────────────────────────────────────────────────────────
3:00    | @tutor /explain exercise:FizzBuzz           | Full solution
        | language:python                            | explained
────────────────────────────────────────────────────────────────────
4:00    | @tutor /next currentExercise:FizzBuzz       | Next exercise
        | difficultyLevel:beginner                    | suggested
────────────────────────────────────────────────────────────────────
5:00    | @lm /generate prompt:"sort array"          | Code generated
        | language:javascript                        |
────────────────────────────────────────────────────────────────────
6:00    | @lm /tokens text:"test"                     | Token count
────────────────────────────────────────────────────────────────────
7:00    | @tutor /secretTest testId:test1            | Unique phrase
────────────────────────────────────────────────────────────────────
8:00    | @tutor /secretTest testId:test1            | Different phrase
        | (run again - should differ)                | = PROOF!
────────────────────────────────────────────────────────────────────
9:00    | Check Debug Console (Ctrl+Shift+Y)        | No red errors
────────────────────────────────────────────────────────────────────
10:00   | ✅ ALL TESTS PASSED                        | Skills working!


🐛 TROUBLESHOOTING
═══════════════════════════════════════════════════════════════════════════

ISSUE: "@tutor participant not found" or not recognized

Solution:
1. Verify VSCode opened with: code --extensionDevelopmentPath=...
2. Check Debug Console (Ctrl+Shift+Y) for specific error
3. Restart VSCode
4. Ensure .instructions.md exists in chat-tutorial folder
5. Check that you typed "@tutor" correctly (exact spelling)


ISSUE: Skill command not recognized (shows error)

Solution:
1. Verify you used "/" before command: /exercise (not exercise)
2. Check parameter syntax: difficulty:value language:value
3. Use lowercase for parameter names
4. Check Debug Console for error message
5. Verify skill is exported in .instructions.md


ISSUE: Empty or null response

Solution:
1. Check Debug Console for error details
2. Verify all required parameters provided
3. Try simpler command without optional parameters
4. Check that VSCode Copilot Chat API is available
5. Restart VSCode extension


ISSUE: Debug Console shows red errors

Solutions by error type:
- "vscode.* not available": APIError - expected in Node.js, not Extension Host
- "skill not found": Name mismatch between .ts and .instructions.md
- "TypeError": Likely parameter type mismatch
- "Cannot read property": Likely missing required parameter


ISSUE: Same output twice (caching concern)

Solution:
1. Use /secretTest command - random value proves it's fresh
2. Check timestamps in skill output
3. Try different parameter values
4. Close and reopen chat if still seeing cached


✅ SUCCESS CHECKLIST - PRINT THIS OUT
═══════════════════════════════════════════════════════════════════════════

Extension Loaded:
  [ ] VSCode opened with chat-tutorial
  [ ] No errors in Debug Console on startup

Participant Recognized:
  [ ] Type @tutor and see it highlighted
  [ ] Type /exercise and see autocomplete

Individual Skills:
  [ ] /exercise generates exercise (5+ lines)
  [ ] /hint provides progressive hints
  [ ] /explain shows solution walkthrough
  [ ] /next suggests progression
  [ ] /secretTest generates unique phrase

All Tests Pass Together:
  [ ] Run all 5 skills in sequence
  [ ] No errors accumulate
  [ ] Each skill independent
  [ ] Debug Console clean

Secret Phrase Verification:
  [ ] Run /secretTest twice
  [ ] Phrases are different
  [ ] Random components differ
  [ ] Timestamps differ
  [ ] ✅✅✅ PROVES REAL INVOCATION ✅✅✅


Final Verification:
═══════════════════════════════════════════════════════════════════════════

If you can complete this checklist ✅, then:

✅ ALL SKILLS ARE WORKING IN REAL VSCODE COPILOT CHAT
✅ NOT USING CACHED RESPONSES (proven by secret test)
✅ READY FOR PRODUCTION USE
✅ READY TO EXTEND TO OTHER EXAMPLES


🎉 You Did It! 🎉
═══════════════════════════════════════════════════════════════════════════

If all tests pass, you have successfully:
✅ Compiled 5 TypeScript files to JavaScript
✅ Registered skills with VSCode Copilot
✅ Tested all skills with real invocations  
✅ Verified real execution (not cached)
✅ Ready for deployment

Next Steps:
1. Document screenshot of successful test
2. Share skill outputs with team
3. Implement remaining 5 examples (22 skills)
4. Scale to production deployment

```

---

## 📝 Notes for Each Test

**Test 1 (@tutor /exercise)**: Basic skill test
- Verifies: Skill invocation works
- Time: 2 minutes

**Test 2 (@tutor /hint)**: Progressive data test
- Verifies: Different outputs by parameter
- Time: 3 minutes

**Test 3 (@tutor /explain)**: Complex output test
- Verifies: Detailed responses work
- Time: 2 minutes

**Test 4 (@tutor /next)**: Conditional logic test
- Verifies: Parameter-based decision making
- Time: 1 minute

**Test 5 (@lm /generate)**: LM integration test
- Verifies: Multi-example participant works
- Time: 1 minute

**Test 6 (@tutor /secretTest)**: PROOF OF EXECUTION
- Verifies: NOT cached, FRESH invocation every time
- Time: 2 minutes
- 🔐 **This is the most important test**
