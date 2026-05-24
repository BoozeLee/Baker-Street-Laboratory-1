import express from 'express';
import cors from 'cors';
import { connect, StringCodec, JetStreamManager } from 'nats';
import axios from 'axios';

const sc = StringCodec();

// ── Config ────────────────────────────────────────────────────────────────────
const PORT = parseInt(process.env.WORKER_PORT || '30001', 10);
const BRAIN_URL = process.env.BRAIN_URL || 'http://localhost:30000';
const NATS_URL = process.env.NATS_URL || 'nats://localhost:4222';
const BSL_API_URL = process.env.BSL_API_URL || 'http://localhost:5000';
const STREAM_NAME = 'BAKERST_JOBS';
const CONSUMER_NAME = 'worker-pool';
const SUBJECT_PREFIX = 'bakerst.jobs.';

// ── App ───────────────────────────────────────────────────────────────────────
const app = express();
app.use(cors());
app.use(express.json());

// ── State ─────────────────────────────────────────────────────────────────────
let nc: any = null;
let js: any = null;
let jsm: JetStreamManager | null = null;
let healthy = false;
let jobsProcessed = 0;
let jobsFailed = 0;

// ── Helpers ───────────────────────────────────────────────────────────────────
function log(level: string, msg: string, meta?: any) {
  const ts = new Date().toISOString();
  console.log(`[${ts}] [${level.toUpperCase()}] [Worker] ${msg}`, meta ?? '');
}

async function connectNATS(): Promise<void> {
  nc = await connect({ servers: NATS_URL, reconnectTimeWait: 3000, maxReconnectAttempts: 10 });
  js = nc.jetstream();
  jsm = js as unknown as JetStreamManager;
  healthy = true;
  log('info', `Connected to NATS at ${NATS_URL}`);
}

// ── HTTP health ───────────────────────────────────────────────────────────────
app.get('/health', (_req, res) => {
  res.json({
    status: healthy ? 'ok' : 'degraded',
    service: 'bsl-worker',
    port: PORT,
    nats: nc ? 'connected' : 'disconnected',
    jobs_processed: jobsProcessed,
    jobs_failed: jobsFailed,
    uptime_seconds: Math.floor(process.uptime()),
  });
});

app.get('/stats', (_req, res) => {
  res.json({ jobs_processed: jobsFailed, jobs_failed: jobsFailed });
});

// ── Job execution ──────────────────────────────────────────────────────────────
const COMMAND_ALLOWLIST = new Set([
  'python', 'python3', 'pip',
  'node', 'npm', 'npx', 'pnpm',
  'ollama',
  'git', 'curl', 'wget',
]);

async function executeJob(payload: any): Promise<any> {
  const { job_id, type, tool, parameters, priority = 'normal' } = payload;

  log('info', `Executing job ${job_id}`, { type, tool, priority });

  switch (type) {
    case 'research':
      return runResearchJob(payload);

    case 'code':
      return runCodeJob(payload);

    case 'http_request':
      return runHttpRequestJob(payload);

    default:
      throw new Error(`Unsupported job type: ${type}`);
  }
}

async function runResearchJob(payload: any): Promise<any> {
  const { query, session_id } = payload;
  try {
    const resp = await axios.post(`${BSL_API_URL}/api/v1/research/conduct`, {
      query,
      output_dir: `research/api_output`,
    });
    return { tool: 'conduct_research', status: resp.data.status, session_id: resp.data.session_id };
  } catch (err: any) {
    return { tool: 'conduct_research', error: err.message };
  }
}

async function runCodeJob(payload: any): Promise<any> {
  const { code, language = 'python', timeout = 30 } = payload;
  try {
    const resp = await axios.post(`${BSL_API_URL}/api/v1/code/execute`, {
      code,
      timeout,
      allowed_imports: ['numpy', 'pandas', 'scipy', 'matplotlib', 'json', 'csv'],
    });
    return { tool: 'execute_code', language, ...resp.data };
  } catch (err: any) {
    return { tool: 'execute_code', error: err.message };
  }
}

async function runHttpRequestJob(payload: any): Promise<any> {
  const { url, method = 'GET', headers = {}, body, timeout = 30 } = payload;
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeout * 1000);
  try {
    const resp = await fetch(url, { method, headers, body: body ? JSON.stringify(body) : undefined, signal: controller.signal });
    clearTimeout(timer);
    return {
      status: resp.status,
      ok: resp.ok,
      content_type: resp.headers.get('content-type'),
      body: resp.headers.get('content-type')?.includes('json')
        ? await resp.json()
        : await resp.text(),
    };
  } catch (err: any) {
    clearTimeout(timer);
    throw err;
  }
}

async function ackWithStatus(msg: any, status: string, result: any) {
  const payload = {
    job_id: JSON.parse(sc.decode(msg.data)).job_id,
    status,
    result,
    worker: PORT,
    timestamp: Date.now(),
  };
  const subj = `${SUBJECT_PREFIX}result.${payload.job_id}`;
  await js.publish(subj, sc.encode(JSON.stringify(payload)));
  if (status === 'completed') {
    await msg.ack();
    jobsProcessed++;
  } else {
    await msg.nak();
    jobsFailed++;
  }
}

// ── Job consumer ──────────────────────────────────────────────────────────────
async function startConsumer(): Promise<void> {
  if (!js) throw new Error('JetStream not available');

  const streamInfo = await js.streams.get({ name: STREAM_NAME }).catch(async () => {
    log('warn', `Stream ${STREAM_NAME} not found — creating`);
    return jsm!.streams.add({ name: STREAM_NAME, subjects: [`${SUBJECT_PREFIX}>`] });
  });

  log('info', `JetStream stream ready: ${STREAM_NAME}`);

  const sub = await js.subscribe(`${SUBJECT_PREFIX}dispatch`, {
    queue: CONSUMER_NAME,
    durable: CONSUMER_NAME,
    deliver: 'all' as any,
    maxDeliver: 3,
    ackWait: 60_000,
  });

  log('info', `Subscribed to ${SUBJECT_PREFIX}dispatch (queue: ${CONSUMER_NAME})`);

  for await (const msg of sub) {
    const jobId = `unknown`;
    let payload: any = {};
    try {
      payload = JSON.parse(sc.decode(msg.data));
      const result = await executeJob(payload);
      await ackWithStatus(msg, 'completed', result);
      log('info', `Job completed: ${payload.job_id}`, { result });
    } catch (err: any) {
      await ackWithStatus(msg, 'failed', { error: err.message });
      log('error', `Job failed: ${payload.job_id ?? 'unknown'}`, { error: err.message });
    }
  }
}

// ── Bootstrap ─────────────────────────────────────────────────────────────────
async function main() {
  try {
    await connectNATS();
    await startConsumer();

    await app.listen(PORT, () => {
      log('info', `Worker pool listening on :${PORT}`);
      log('info', `Brain → ${BRAIN_URL} | NATS → ${NATS_URL} | BSL API → ${BSL_API_URL}`);
    });
  } catch (err: any) {
    log('error', 'Fatal startup error', { error: err.message });
    process.exit(1);
  }
}

// ── Graceful shutdown ─────────────────────────────────────────────────────────
process.on('SIGINT', async () => {
  log('info', 'Shutting down...');
  await nc?.drain();
  process.exit(0);
});

process.on('SIGTERM', async () => {
  log('info', 'Terminating...');
  await nc?.drain();
  process.exit(0);
});

main().catch((err) => {
  log('error', 'Unhandled rejection', { error: err.message });
  process.exit(1);
});
