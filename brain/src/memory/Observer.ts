import { MemoryStore } from './MemoryStore.js';

/**
 * Observer — extracts structured observations from conversations
 * Runs after each agent response (fire-and-forget)
 */
export class Observer {
  constructor(private memory: MemoryStore) {}

  async extractObservations(conversationId: string, responseText: string, messages: any[]): Promise<void> {
    try {
      // For now, use a simple rule-based extraction
      // In full implementation, would call LLM with observer role prompt
      const observations = this.extractWithRules(messages);

      for (const obs of observations) {
        await this.memory.addMemory({
          content: obs.content,
          metadata: {
            conversation_id: conversationId,
            type: obs.type as any,
            confidence: obs.confidence,
            related_tools: obs.related_tools || [],
            timestamp: Date.now(),
          },
        });
      }

      console.log(`[Observer] Extracted ${observations.length} observations`);
    } catch (err) {
      console.error('[Observer] Failed:', err);
    }
  }

  private extractWithRules(messages: any[]): Array<{ type: string; content: string; confidence: number; related_tools: string[] }> {
    const observations: any[] = [];

    const lastUser = messages.filter((m) => m.role === 'user').pop();
    const lastAssistant = messages.filter((m) => m.role === 'assistant').pop();

    if (!lastUser || !lastAssistant) return observations;

    const userText = typeof lastUser.content === 'string' ? lastUser.content : JSON.stringify(lastUser.content);
    const assistantText = typeof lastAssistant.content === 'string' ? lastAssistant.content : JSON.stringify(lastAssistant.content);

    // Pattern: User expresses preference
    const preferencePatterns = [
      /I (prefer|like|love|hate|dislike) ([^.]+)/i,
      /my favorite (.+) is ([^.]+)/i,
      /I always (.+)/i,
    ];

    for (const pattern of preferencePatterns) {
      const match = userText.match(pattern);
      if (match) {
        observations.push({
          type: 'preference',
          content: `User preference: ${match[0]}`,
          confidence: 0.8,
        });
      }
    }

    // Pattern: Decision made
    if (assistantText.includes('I will') || assistantText.includes('Let\'s') || assistantText.includes('I\'ll use')) {
      observations.push({
        type: 'decision',
        content: `Decision: ${assistantText.substring(0, 200)}...`,
        confidence: 0.7,
        related_tools: ['note'],
      });
    }

    // Pattern: Issue encountered
    if (assistantText.toLowerCase().includes('error') || assistantText.toLowerCase().includes('failed')) {
      observations.push({
        type: 'issue',
        content: `Error encountered: ${assistantText.substring(0, 200)}`,
        confidence: 0.9,
        related_tools: ['error_handler'],
      });
    }

    // Pattern: Fact stated
    const factPatterns = [
      /According to ([^,]+), (.+)/i,
      /Studies show that (.+)/i,
      /It is known that (.+)/i,
    ];
    for (const pattern of factPatterns) {
      if (pattern.test(assistantText)) {
        observations.push({
          type: 'fact',
          content: assistantText.substring(0, 300),
          confidence: 0.6,
        });
      }
    }

    // Pattern: Next step identified
    if (assistantText.includes('Next:') || assistantText.includes('Next step:') || assistantText.includes('Now I will')) {
      observations.push({
        type: 'nextstep',
        content: `Next action: ${assistantText.substring(0, 200)}`,
        confidence: 0.8,
      });
    }

    // Pattern: Outcome
    if (assistantText.includes('completed') || assistantText.includes('successful') || assistantText.includes('result:')) {
      observations.push({
        type: 'outcome',
        content: `Result: ${assistantText.substring(0, 200)}`,
        confidence: 0.85,
      });
    }

    return observations;
  }
}
