import { connect, StringCodec } from 'nats';

const sc = StringCodec();

export class NATSClient {
  private nc: any = null;
  private js: any = null;

  constructor(private url: string) {}

  async connect(): Promise<void> {
    try {
      this.nc = await connect({ servers: this.url });
      console.log('[NATS] Connected to', this.url);

      this.js = this.nc.jetstream();
      console.log('[NATS] JetStream context acquired');
    } catch (err) {
      console.error('[NATS] Connection failed:', err);
      throw err;
    }
  }

  async publish(subject: string, data: any): Promise<void> {
    if (!this.js) throw new Error('NATS not connected');
    await this.js.publish(subject, sc.encode(JSON.stringify(data)));
  }

  async subscribe(subject: string, handler: (data: any) => Promise<void>): Promise<any> {
    if (!this.js) throw new Error('NATS not connected');
    return await this.js.subscribe(subject, {
      deliver: 'all',
    });
  }

  async disconnect(): Promise<void> {
    if (this.nc) {
      await this.nc.drain();
      console.log('[NATS] Disconnected');
    }
  }

  isConnected(): boolean {
    return this.nc !== null && !this.nc.isClosed();
  }
}
