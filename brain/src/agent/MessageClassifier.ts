/**
 * MessageClassifier — determines what mode/role to use for a message
 *
 * Strategy:
 * - If message is short greeting/chit-chat → conversational
 * - If message contains research/analyze/generate → agent
 * - If triggered by system event → observer/reflector
 */

export class MessageClassifier {
  private greetings = ['hi', 'hello', 'hey', 'good morning', 'good afternoon', 'good evening'];
  private conversational = ['thanks', 'thank you', 'how are you', 'what\'s up', 'greetings'];

  classify(message: string, history?: any[]): 'agent' | 'conversational' | 'observer' | 'reflector' | 'reasoner' {
    const lower = message.toLowerCase().trim();

    // 1. Check for explicit mode request
    if (lower.includes('/reason') || lower.includes('think deeply')) {
      return 'reasoner';
    }

    // 2. Greetings & casual talk → conversational
    if (this.greetings.some((g) => lower.startsWith(g)) || this.conversational.some((c) => lower.includes(c))) {
      if (!history || history.length < 2) {
        return 'conversational';
      }
    }

    // 3. Research intent detection
    const researchKeywords = [
      'research', 'analyze', 'study', 'investigate', 'find', 'search',
      'what is', 'explain', 'how does', 'summarize', 'survey',
      'generate', 'create', 'write', 'code', 'script',
      'image', 'picture', 'diagram', 'chart', 'figure',
      'data', 'statistics', 'trend', 'correlation',
    ];
    if (researchKeywords.some((kw) => lower.includes(kw))) {
      return 'agent';
    }

    // 4. Question mark? Likely needs tools or reasoning
    if (message.includes('?')) {
      return 'agent';
    }

    // 5. Default to agent for anything substantive
    if (message.length > 20) {
      return 'agent';
    }

    // 6. Short messages → conversational
    return 'conversational';
  }
}
