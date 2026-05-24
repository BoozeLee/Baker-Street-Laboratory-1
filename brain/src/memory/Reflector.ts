import { MemoryStore } from './MemoryStore.js';

/**
 * Reflector — compresses and consolidates the observation log
 * Runs periodically when memory exceeds threshold
 */
export class Reflector {
  private intervalId: NodeJS.Timeout | null = null;
  private readonly MAX_OBSERVATIONS = 200; // compress when we have > 200
  private readonly TOKEN_BUDGET = 4000; // ~3000-4000 tokens for observation log

  constructor(private memory: MemoryStore) {}

  startCompactionCycle(): void {
    // Run every 30 minutes
    this.intervalId = setInterval(() => this.runCompaction(), 30 * 60 * 1000);
    console.log('[Reflector] Started compaction cycle (every 30min)');
  }

  async runCompaction(): Promise<void> {
    try {
      console.log('[Reflector] Running compaction...');

      // Get all observations (across all conversations)
      const sqlite = (this.memory as any).sqlite as any;
      const rows = sqlite
        .prepare(`
          SELECT id, type, content, confidence, created_at
          FROM observations
          ORDER BY created_at DESC
        `)
        .all() as any[];

      if (rows.length <= this.MAX_OBSERVATIONS) {
        console.log(`[Reflector] ${rows.length} observations — no compaction needed`);
        return;
      }

      console.log(`[Reflector] Compacting ${rows.length} observations...`);

      // Group related observations into summaries (simple approach: by type + date)
      const grouped: Record<string, any[]> = {};
      for (const row of rows) {
        const day = new Date(row.created_at).toISOString().split('T')[0];
        const key = `${row.type}-${day}`;
        if (!grouped[key]) grouped[key] = [];
        grouped[key].push(row);
      }

      // Create summary observations from groups
      const toDelete: number[] = [];
      const summaries: any[] = [];

      for (const [key, group] of Object.entries(grouped)) {
        if (group.length <= 3) continue; // Keep small groups as-is

        // Create summary
        const types = [...new Set(group.map((g) => g.type))];
        const avgConfidence = group.reduce((sum, g) => sum + g.confidence, 0) / group.length;

        summaries.push({
          type: 'summary',
          content: `Batch summary (${key}): ${group.length} observations of types [${types.join(', ')}]. Topics: ${this.extractTopics(group).join(', ')}`,
          confidence: avgConfidence,
          related_tools: ['reflector'],
        });

        // Mark originals for deletion
        toDelete.push(...group.map((g) => g.id));
      }

      // Delete old observations
      if (toDelete.length > 0) {
        const deleteStmt = sqlite.prepare('DELETE FROM observations WHERE id = ?');
        for (const id of toDelete) {
          deleteStmt.run(id);
        }
      }

      // Insert summaries
      for (const summary of summaries) {
        await this.memory.addMemory({
          content: summary.content,
          metadata: {
            type: summary.type as any,
            confidence: summary.confidence,
            related_tools: summary.related_tools,
            timestamp: Date.now(),
          },
        });
      }

      console.log(`[Reflector] Compacted ${toDelete.length} observations → ${summaries.length} summaries`);
    } catch (err) {
      console.error('[Reflector] Compaction error:', err);
    }
  }

  private extractTopics(observations: any[]): string[] {
    // Naive keyword extraction (full version would use NLP or LLM)
    const words: string[] = [];
    for (const obs of observations) {
      const tokens = obs.content.toLowerCase().split(/\W+/);
      words.push(...tokens.filter((w: string) => w.length > 4));
    }
    const counts = new Map<string, number>();
    for (const w of words) {
      counts.set(w, (counts.get(w) || 0) + 1);
    }
    return Array.from(counts.entries())
      .sort((a, b) => b[1] - a[1])
      .slice(0, 5)
      .map((e) => e[0]);
  }
}
