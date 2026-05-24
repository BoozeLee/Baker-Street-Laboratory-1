// Global unhandled rejection handler
process.on('unhandledRejection', (reason: any) => {
  console.error('Unhandled Rejection:', reason);
});

process.on('uncaughtException', (err: any) => {
  console.error('Uncaught Exception:', err);
});

import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import dotenv from 'dotenv';
import { Brain } from './agent/Brain.js';

dotenv.config();

const APP_PORT = parseInt(process.env.BRAIN_PORT || '30000', 10);
const app = express();

// Middleware
app.use(helmet());
app.use(cors({ origin: process.env.ALLOWED_ORIGINS?.split(',') || '*' }));
app.use(express.json());

// Initialize Brain
const brain = new Brain({
  bslApiUrl: process.env.BSL_API_URL || 'http://localhost:5000',
  natsUrl: process.env.NATS_URL || 'nats://localhost:4222',
  qdrantUrl: process.env.QDRANT_URL || 'http://localhost:6333',
  sqlitePath: process.env.SQLITE_PATH || './data/bakerst.db',
  configPath: process.env.CONFIG_PATH || '../operating_system',
});

// Start server after Brain initialization
(async () => {
  try {
    await brain.initialize();
    console.log('🧠 Brain agent initialized');

    // Health check
    app.get('/health', (req, res) => {
      res.json({
        status: 'ok',
        service: 'brain',
        timestamp: new Date().toISOString(),
        uptime: process.uptime(),
      });
    });

    // Streaming chat endpoint
    app.post('/api/v1/chat/stream', async (req, res) => {
      const { message, conversation_id } = req.body;

      if (!message || typeof message !== 'string') {
        res.status(400).json({ error: 'Message is required' });
        return;
      }

      const conversationId = conversation_id || generateId();

      // Set up SSE
      res.setHeader('Content-Type', 'text/event-stream');
      res.setHeader('Cache-Control', 'no-cache');
      res.setHeader('Connection', 'keep-alive');
      res.setHeader('X-Conversation-ID', conversationId);

      try {
        await brain.chatStream({
          message,
          conversationId,
          onText: (chunk) => {
            res.write(`data: ${JSON.stringify({ type: 'text', content: chunk })}\n\n`);
          },
          onToolUse: (tool) => {
            res.write(`data: ${JSON.stringify({ type: 'tool_use', tool })}\n\n`);
          },
          onDone: () => {
            res.write(`data: ${JSON.stringify({ type: 'done', conversation_id: conversationId })}\n\n`);
            res.end();
          },
          onError: (err) => {
            res.write(`data: ${JSON.stringify({ type: 'error', error: err.message })}\n\n`);
            res.end();
          },
        });
      } catch (err: any) {
        console.error('Chat error:', err);
        res.write(`data: ${JSON.stringify({ type: 'error', error: err.message })}\n\n`);
        res.end();
      }
    });

    // Non-streaming chat (for API compatibility)
    app.post('/api/v1/chat', async (req, res) => {
      const { message, conversation_id } = req.body;

      try {
        const result = await brain.chat({
          message,
          conversationId: conversation_id || generateId(),
        });
        res.json(result);
      } catch (err: any) {
        console.error('Chat error:', err);
        res.status(500).json({ error: err.message });
      }
    });

    // Tool status
    app.get('/api/v1/tools/status', (req, res) => {
      res.json(brain.getToolStatus());
    });

    // Tool execution (for direct calls)
    app.post('/api/v1/tools/execute', async (req, res) => {
      const { name, parameters } = req.body;

      try {
        const result = await brain.executeTool(name, parameters);
        res.json({ result });
      } catch (err: any) {
        console.error('Tool execution error:', err);
        res.status(500).json({ error: err.message });
      }
    });

    // Memory search
    app.get('/api/v1/memory/search', async (req, res) => {
      const { q, limit = 10 } = req.query;

      try {
        const results = await brain.searchMemory(q as string, parseInt(limit as string, 10));
        res.json({ results });
      } catch (err: any) {
        console.error('Memory search error:', err);
        res.status(500).json({ error: err.message });
      }
    });

    // Conversation history
    app.get('/api/v1/conversations/:id', async (req, res) => {
      try {
        const history = await brain.getConversation(req.params.id);
        res.json({ conversation_id: req.params.id, messages: history });
      } catch (err: any) {
        res.status(500).json({ error: err.message });
      }
    });

    app.listen(APP_PORT, () => {
      console.log(`🧠 Brain agent started on port ${APP_PORT}`);
      console.log(`   Health: http://localhost:${APP_PORT}/health`);
      console.log(`   Chat: http://localhost:${APP_PORT}/api/v1/chat`);
    });
  } catch (err: any) {
    console.error('Failed to initialize Brain:', err);
    process.exit(1);
  }
})();

function generateId(): string {
  return Date.now().toString(36) + Math.random().toString(36).substring(2);
}
