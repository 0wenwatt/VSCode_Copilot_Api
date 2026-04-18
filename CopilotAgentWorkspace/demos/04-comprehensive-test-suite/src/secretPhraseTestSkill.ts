/**
 * SECRET PHRASE TEST SKILL
 * 
 * Use this to verify that skills are actually working
 * (Not cached responses, but real skill invocation)
 */

export const secretPhraseTestSkill = {
  name: 'tutor.secretTest',
  description: 'Secret phrase test - returns unique phrase only when skill is actually invoked',

  parameters: {
    type: 'object',
    properties: {
      testId: {
        type: 'string',
        description: 'Test identifier'
      }
    }
  },

  async invoke(input: any) {
    const { testId = 'unknown' } = input;
    const timestamp = new Date().toISOString();
    const randomNumber = Math.random().toString(36).substring(7);

    // This is the SECRET PHRASE - it changes every invocation
    const secretPhrase = `🔐 SKILL_VERIFIED_${testId}_${randomNumber}_${timestamp}`;

    return {
      status: 'success',
      message: secretPhrase,
      verification: 'This message is UNIQUE and proves the skill was actually invoked',
      timestamp: timestamp,
      randomComponent: randomNumber,
      testId: testId,
      proof: 'If this message changes every time, the skill is working (not cached)!',
      yourSecretPhrase: secretPhrase
    };
  }
};

export default secretPhraseTestSkill;
