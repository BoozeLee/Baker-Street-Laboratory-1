import express from 'express';
import cors from 'cors';
import axios from 'axios';

const app = express();
const PORT = parseInt(process.env.GATEWAY_PORT || '8080', 10);
const BRAIN_URL = process.env.BRAIN_URL || 'http://localhost:30000';

app.use(cors());
app.use(express.json());

// ── Health ──────────────────────────────────────────────────────────────────
app.get('/health', (req, res) => {
  res.json({ status: 'ok', service: 'gateway', brain: BRAIN_URL, port: PORT });
});

// ── Root ─────────────────────────────────────────────────────────────────────
app.get('/', (req, res) => {
  res.json({
    service: 'Baker Street Laboratory — Gateway',
    version: '2.1.0',
    endpoints: {
      health: '/health',
      chat: 'POST /api/v1/chat',
      tools: 'GET /api/v1/tools/status',
      memory: 'GET /api/v1/memory/search?q=...',
      models: 'GET /api/v1/models/status',
    },
  });
});

// ── Helpers ──────────────────────────────────────────────────────────────────
const brainClient = axios.create({
  baseURL: BRAIN_URL,
  timeout: 300_000,
  headers: { 'Content-Type': 'application/json' },
});

async function proxyToBrain(path: string): Promise<any> {
  try {
    const r = await brainClient.get(path);
    return r.data;
  } catch (err: any) {
    return { error: true, message: err.message };
  }
}

// ── Route → Brain proxy ───────────────────────────────────────────────────────
app.get('/api/v1/tools/status', async (req, res) => {
  const data = await proxyToBrain('/api/v1/tools/status');
  res.json(data);
});

app.get('/api/v1/memory/search', async (req, res) => {
  const q = (req.query.q as string) || '';
  const limit = parseInt((req.query.limit as string) || '10', 10);
  const data = await proxyToBrain(`/api/v1/memory/search?q=${encodeURIComponent(q)}&limit=${limit}`);
  res.json(data);
});

app.get('/api/v1/models/status', async (req, res) => {
  const data = await proxyToBrain('/api/v1/tools/status');
  res.json(data);
});

// ── Chat (non-streaming) ──────────────────────────────────────────────────────
app.post('/api/v1/chat', async (req, res) => {
  try {
    const response = await brainClient.post('/api/v1/chat', req.body);
    res.json(response.data);
  } catch (err: any) {
    res.status(err.response?.status || 500).json({
      error: true,
      message: err.response?.data?.error || err.message,
    });
  }
});

// ── Chat (SSE stream proxy) ───────────────────────────────────────────────────
app.post('/api/v1/chat/stream', async (req, res) => {
  res.setHeader('Content-Type', 'text/event-stream');
  res.setHeader('Cache-Control', 'no-cache');
  res.setHeader('Connection', 'keep-alive');

  try {
    const response = await brainClient.post('/api/v1/chat/stream', req.body, {
      responseType: 'stream',
    });

    response.data.on('data', (chunk: Buffer) => {
      res.write(chunk);
    });

    response.data.on('end', () => res.end());
    response.data.on('error', (err: Error) => {
      res.write(`data: ${JSON.stringify({ type: 'error', error: err.message })}\n\n`);
      res.end();
    });
  } catch (err: any) {
    res.write(`data: ${JSON.stringify({ type: 'error', error: err.message })}\n\n`);
    res.end();
  }
});

// ── Conversation history ──────────────────────────────────────────────────────
app.get('/api/v1/conversations/:id', async (req, res) => {
  const data = await proxyToBrain(`/api/v1/conversations/${req.params.id}`);
  res.json(data);
});

// ── Research status (pass-through) ────────────────────────────────────────────
app.get('/api/v1/research/status/:sessionId', async (req, res) => {
  // Proxy to BSL API directly for session tracking
  try {
    const r = await axios.get(
      `${process.env.BSL_API_URL || 'http://localhost:5000'}/api/v1/research/status/${req.params.sessionId}`,
    );
    res.json(r.data);
  } catch (err: any) {
    res.status(500).json({ error: true, message: err.message });
  }
});

// ── Static redirect: / → docs ─────────────────────────────────────────────────
app.get('/docs', async (req, res) => {
  res.redirect((process.env.BRAIN_URL || 'http://localhost:30000') + '/health');
});

// ── Start ─────────────────────────────────────────────────────────────────────
app.listen(PORT, () => {
  console.log(`🚪 Gateway listening on :${PORT}`);
  console.log(`   Brain → ${BRAIN_URL}`);
});
