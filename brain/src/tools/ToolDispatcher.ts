import { EventEmitter } from 'events';
import { ToolRegistry } from './ToolRegistry.js';
import { BSLToolAdapter } from './BSLToolAdapter.js';

interface ToolCall {
  name: string;
  arguments: Record<string, any>;
  id: string;
}

interface ToolResult {
  tool_call_id: string;
  name: string;
  result: any;
  error?: string;
}

export class ToolDispatcher extends EventEmitter {
  private registry: ToolRegistry;
  private bslAdapter: BSLToolAdapter | null = null;

  constructor() {
    super();
    this.registry = new ToolRegistry();
    this.initializeTools();
  }

  private initializeTools(): void {
    // Register all available tools with their schemas and handlers
    this.registry.register('conduct_research', {
      description: 'Execute a full research pipeline on a given query',
      parameters: {
        type: 'object',
        properties: {
          query: { type: 'string', description: 'Research question or topic' },
          output_dir: { type: 'string', description: 'Output directory (optional)' },
        },
        required: ['query'],
      },
      handler: async (params: any) => {
        if (!this.bslAdapter) throw new Error('BSL adapter not initialized');
        return this.bslAdapter.conductResearch(params);
      },
    });

    this.registry.register('semantic_search', {
      description: 'Find semantically similar documents using vector embeddings',
      parameters: {
        type: 'object',
        properties: {
          query: { type: 'string', description: 'Search query' },
          k: { type: 'number', description: 'Number of results (default: 10)' },
          threshold: { type: 'number', description: 'Similarity threshold 0-1 (default: 0.7)' },
        },
        required: ['query'],
      },
      handler: async (params: any) => {
        if (!this.bslAdapter) throw new Error('BSL adapter not initialized');
        return this.bslAdapter.semanticSearch(params);
      },
    });

    this.registry.register('batch_analyze_images', {
      description: 'Process multiple images in parallel',
      parameters: {
        type: 'object',
        properties: {
          images: { type: 'array', items: { type: 'string' }, description: 'Image paths or URLs' },
          analysis_type: { type: 'string', enum: ['chart', 'diagram', 'microscopy', 'general'] },
          context: { type: 'string' },
        },
        required: ['images', 'analysis_type'],
      },
      handler: async (params: any) => {
        if (!this.bslAdapter) throw new Error('BSL adapter not initialized');
        return this.bslAdapter.batchAnalyzeImages(params);
      },
    });

    this.registry.register('generate_code', {
      description: 'Generate code for data analysis or simulations',
      parameters: {
        type: 'object',
        properties: {
          task: { type: 'string', description: 'What the code should do' },
          language: { type: 'string', enum: ['python', 'r', 'julia'], default: 'python' },
          libraries: { type: 'array', items: { type: 'string' } },
          context: { type: 'string' },
        },
        required: ['task'],
      },
      handler: async (params: any) => {
        if (!this.bslAdapter) throw new Error('BSL adapter not initialized');
        return this.bslAdapter.generateCode(params);
      },
    });

    this.registry.register('review_code', {
      description: 'Review code for bugs and improvements',
      parameters: {
        type: 'object',
        properties: {
          code: { type: 'string', description: 'Code to review' },
          purpose: { type: 'string', description: 'What the code should accomplish' },
        },
        required: ['code', 'purpose'],
      },
      handler: async (params: any) => {
        if (!this.bslAdapter) throw new Error('BSL adapter not initialized');
        return this.bslAdapter.reviewCode(params);
      },
    });

    this.registry.register('execute_code', {
      description: 'Run Python code in a sandboxed environment',
      parameters: {
        type: 'object',
        properties: {
          code: { type: 'string' },
          timeout: { type: 'number', default: 30 },
          allowed_imports: { type: 'array', items: { type: 'string' } },
        },
        required: ['code'],
      },
      handler: async (params: any) => {
        if (!this.bslAdapter) throw new Error('BSL adapter not initialized');
        return this.bslAdapter.executeCode(params);
      },
    });

    this.registry.register('get_system_status', {
      description: 'Check operational status of BSL models and services',
      parameters: { type: 'object', properties: {} },
      handler: async () => {
        if (!this.bslAdapter) throw new Error('BSL adapter not initialized');
        return this.bslAdapter.getSystemStatus();
      },
    });

    this.registry.register('query_database', {
      description: 'Execute SQL queries (SELECT only)',
      parameters: {
        type: 'object',
        properties: {
          sql: { type: 'string', description: 'SELECT SQL query' },
          format: { type: 'string', enum: ['json', 'csv', 'table'], default: 'json' },
        },
        required: ['sql'],
      },
      handler: async (params: any) => {
        if (!this.bslAdapter) throw new Error('BSL adapter not initialized');
        return this.bslAdapter.queryDatabase(params);
      },
    });

    this.registry.register('create_visualization', {
      description: 'Generate charts/plots from data',
      parameters: {
        type: 'object',
        properties: {
          data_source: { type: 'string', description: 'CSV path or SQL query' },
          chart_type: { type: 'string', enum: ['line', 'bar', 'scatter', 'histogram', 'heatmap', 'box'] },
          options: { type: 'object', description: 'Chart options (title, labels, colors)' },
          output_format: { type: 'string', enum: ['png', 'svg', 'pdf'], default: 'png' },
        },
        required: ['data_source', 'chart_type'],
      },
      handler: async (params: any) => {
        if (!this.bslAdapter) throw new Error('BSL adapter not initialized');
        return this.bslAdapter.createVisualization(params);
      },
    });

    this.registry.register('ingest_document', {
      description: 'Parse and index a document into vector store',
      parameters: {
        type: 'object',
        properties: {
          file_path: { type: 'string' },
          metadata: { type: 'object', description: 'title, authors, date, tags' },
          chunk_size: { type: 'number', default: 1000 },
        },
        required: ['file_path'],
      },
      handler: async (params: any) => {
        if (!this.bslAdapter) throw new Error('BSL adapter not initialized');
        return this.bslAdapter.ingestDocument(params);
      },
    });
  }

  registerBSLTools(bslApiUrl: string): void {
    this.bslAdapter = new BSLToolAdapter(bslApiUrl);
    this.registry.markAvailable();
  }

  getToolDescriptions(): string {
    return this.registry.describeAll();
  }

  getToolSchemas(): any[] {
    return this.registry.getAllSchemas();
  }

  async execute(name: string, parameters: any): Promise<any> {
    return this.registry.execute(name, parameters);
  }

  async executeAll(calls: ToolCall[]): Promise<ToolResult[]> {
    const results = await Promise.all(
      calls.map(async (call) => {
        try {
          const result = await this.execute(call.name, call.arguments);
          return {
            tool_call_id: call.id,
            name: call.name,
            result,
          };
        } catch (err) {
          return {
            tool_call_id: call.id,
            name: call.name,
            result: null,
            error: err instanceof Error ? err.message : String(err),
          };
        }
      })
    );
    return results;
  }

  getStatus(): Record<string, any> {
    return this.registry.getStatus();
  }
}
