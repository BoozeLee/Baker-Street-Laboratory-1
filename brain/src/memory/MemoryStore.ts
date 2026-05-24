import Database from 'better-sqlite3';
import axios from 'axios';
import path from 'path';

export interface Message {
  role: 'user' | 'assistant' | 'tool' | 'system';
  content: string;
  timestamp?: number;
  tool_call_id?: string;
  tool_calls?: any[];
}

export interface MemoryItem {
  id?: string;
  content: string;
  embedding?: number[];
  metadata: {
    conversation_id?: string;
    type: 'message' | 'observation' | 'fact' | 'decision' | 'preference' | 'issue' | 'nextstep' | 'outcome';
    confidence: number;
    source?: string;
    timestamp: number;
    related_tools?: string[];
  };
}

export class MemoryStore {
  private sqlite: Database.Database;
  private qdrantUrl: string;
  private collectionName = 'bakerst_memories';
  private axiosInstance: any;

  constructor(private dbPath: string, qdrantUrl: string) {
    this.sqlite = new Database(dbPath);
    this.qdrantUrl = qdrantUrl.replace(/\/$/, '');
    this.axiosInstance = axios.create({
      baseURL: this.qdrantUrl,
      timeout: 10000,
    });
  }

  async initialize(): Promise<void> {
    // Initialize SQLite
    this.initSQLite();

    // Initialize Qdrant (optional — if unavailable, log warning and continue)
    try {
      await this.initQdrant();
    } catch (err: any) {
      console.warn('[Memory] Qdrant unavailable — vector search disabled:', err.message);
    }
  }

  private initSQLite(): void {
    this.sqlite.exec(`
      CREATE TABLE IF NOT EXISTS conversations (
        id TEXT PRIMARY KEY,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
      );

      CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        conversation_id TEXT NOT NULL,
        role TEXT NOT NULL,
        content TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        tool_call_id TEXT,
        FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
      );

      CREATE TABLE IF NOT EXISTS observations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        conversation_id TEXT,
        type TEXT NOT NULL,
        content TEXT NOT NULL,
        confidence REAL DEFAULT 0.5,
        related_tools TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (conversation_id) REFERENCES conversations(id)
      );

      CREATE INDEX IF NOT EXISTS idx_messages_conversation ON messages(conversation_id);
      CREATE INDEX IF NOT EXISTS idx_observations_conversation ON observations(conversation_id);
      CREATE INDEX IF NOT EXISTS idx_observations_created ON observations(created_at);
    `);
  }

  private async initQdrant(): Promise<void> {
    try {
      // Check if collection exists
      const response = await this.axiosInstance.get(`/collections/${this.collectionName}`);
      if (response.status === 200) {
        console.log(`[Memory] Qdrant collection exists: ${this.collectionName}`);
        return;
      }
    } catch (err: any) {
      if (err.response?.status === 404) {
        // Create collection
        try {
          await this.axiosInstance.put(`/collections/${this.collectionName}`, {
            vectors: {
              size: 1024,
              distance: 'Cosine',
            },
          });
          console.log(`[Memory] Created Qdrant collection: ${this.collectionName}`);
        } catch (createErr: any) {
          console.warn('[Memory] Qdrant create failed:', createErr.message || createErr);
        }
      } else {
        console.warn('[Memory] Qdrant unreachable:', err.message || err);
      }
    }
  }

  async getConversation(conversationId: string): Promise<Message[]> {
    const rows = this.sqlite
      .prepare('SELECT role, content, tool_call_id FROM messages WHERE conversation_id = ? ORDER BY id ASC')
      .all(conversationId) as any[];

    return rows.map((row) => ({
      role: row.role,
      content: row.content,
      tool_call_id: row.tool_call_id,
    }));
  }

  async saveConversation(conversationId: string, messages: Message[]): Promise<void> {
    const upsertConversation = this.sqlite.prepare(`
      INSERT OR REPLACE INTO conversations (id, updated_at) VALUES (?, CURRENT_TIMESTAMP)
    `);
    const insertMessage = this.sqlite.prepare(`
      INSERT INTO messages (conversation_id, role, content, timestamp, tool_call_id)
      VALUES (?, ?, ?, CURRENT_TIMESTAMP, ?)
    `);

    upsertConversation.run(conversationId);

    for (const msg of messages) {
      insertMessage.run(conversationId, msg.role, JSON.stringify(msg.content), msg.tool_call_id || null);
    }
  }

  async search(query: string, limit: number = 10): Promise<MemoryItem[]> {
    try {
      // 1. Generate embedding via Ollama (nomic-embed-text)
      const embedding = await this.getEmbedding(query);

      // 2. Search Qdrant via REST
      const response = await this.axiosInstance.post(`/collections/${this.collectionName}/points/search`, {
        vector: embedding,
        limit,
        with_payload: true,
        score_threshold: 0.5,
      });

      const points = response.data.result || [];
      return points.map((hit: any) => ({
        id: hit.id,
        content: hit.payload?.content || '',
        metadata: hit.payload?.metadata || {},
      }));
    } catch (err: any) {
      console.error('[Memory] Search error (Qdrant unavailable?):', err.message || err);
      return [];
    }
  }

  async addMemory(item: MemoryItem): Promise<string> {
    const id = item.id || `${Date.now()}-${Math.random().toString(36).substring(7)}`;

    // Ensure vector is present
    const vector = item.embedding || await this.getEmbedding(item.content);

    // Try upsert to Qdrant via REST (optional)
    try {
      await this.axiosInstance.put(`/collections/${this.collectionName}/points`, {
        points: [
          {
            id,
            vector,
            payload: {
              content: item.content,
              metadata: item.metadata,
            },
          },
        ],
      });
     } catch (err: any) {
       console.warn('[Memory] Qdrant upsert failed:', err.message || err);
       // Continue without vector storage
     }

    // Also insert into SQLite observations if type is 'observation'
    if (item.metadata.type === 'observation') {
      this.sqlite.prepare(`
        INSERT INTO observations (conversation_id, type, content, confidence, related_tools, created_at)
        VALUES (?, ?, ?, ?, ?, datetime('now'))
      `).run(
        item.metadata.conversation_id || null,
        item.metadata.type,
        item.content,
        item.metadata.confidence,
        JSON.stringify(item.metadata.related_tools || [])
      );
    }

    return id;
  }

  async getRecentObservations(conversationId: string, limit: number = 50): Promise<any[]> {
    const rows = this.sqlite
      .prepare(`
        SELECT type, content, confidence, related_tools, created_at
        FROM observations
        WHERE conversation_id = ? OR conversation_id IS NULL
        ORDER BY created_at DESC
        LIMIT ?
      `)
      .all(conversationId, limit) as any[];

    return rows.map((r) => ({
      type: r.type,
      content: r.content,
      confidence: r.confidence,
      related_tools: JSON.parse(r.related_tools || '[]'),
      created_at: r.created_at,
    }));
  }

  private async getEmbedding(text: string): Promise<number[]> {
    // Use Ollama's nomic-embed-text model via HTTP API
    try {
      const ollamaHost = process.env.OLLAMA_HOST || 'http://localhost:11434';
      const response = await fetch(`${ollamaHost}/api/embeddings`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          model: 'nomic-embed-text',
          prompt: text,
        }),
      });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const data: any = await response.json();
      return data.embedding as number[];
    } catch (err: any) {
      console.error('[Memory] Embedding error:', err.message || err);
      // Return zero vector fallback (1024 dimensions)
      return new Array(1024).fill(0);
    }
  }

  async close(): Promise<void> {
    this.sqlite.close();
  }
}
