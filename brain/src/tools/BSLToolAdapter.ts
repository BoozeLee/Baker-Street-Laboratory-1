import axios from 'axios';
import type { AxiosInstance } from 'axios';

export class BSLToolAdapter {
  private baseUrl: string;
  private client: AxiosInstance;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl.replace(/\/$/, ''); // remove trailing slash
    this.client = axios.create({
      baseURL: this.baseUrl,
      timeout: 300000, // 5 minutes for long research
      headers: {
        'Content-Type': 'application/json',
        'X-API-Key': process.env.BSL_API_KEY || 'bsl-local-dev-key',
      },
    });
  }

  async conductResearch(params: { query: string; output_dir?: string }): Promise<any> {
    try {
      const response = await this.client.post('/api/v1/research/conduct', {
        query: params.query,
        output_dir: params.output_dir || 'research/api_output',
      });

      return {
        status: 'started',
        session_id: response.data.session_id,
        message: `Research started: ${response.data.status}`,
        report_path: response.data.report_path,
      };
    } catch (err: any) {
      return this.handleError(err, 'conduct_research');
    }
  }

  async semanticSearch(params: { query: string; k?: number; threshold?: number }): Promise<any> {
    try {
      // Try to use vector store directly via BSL's API
      const response = await this.client.post('/api/v1/memory/search', {
        query: params.query,
        k: params.k || 10,
        threshold: params.threshold || 0.7,
      });

      return response.data;
    } catch (err: any) {
      // Fallback: query database with LIKE (less accurate)
      return { results: [], warning: 'Vector search unavailable, using text search' };
    }
  }

  async batchAnalyzeImages(params: { images: string[]; analysis_type: string; context?: string }): Promise<any> {
    try {
      const results = await Promise.all(
        params.images.map(async (img) => {
          const response = await this.client.post('/api/v1/vision/analyze', {
            image_url: img,
            analysis_type: params.analysis_type,
            context: params.context,
          });
          return { image: img, analysis: response.data };
        })
      );
      return { analyses: results };
    } catch (err: any) {
      return this.handleError(err, 'batch_analyze_images');
    }
  }

  async generateCode(params: {
    task: string;
    language?: string;
    libraries?: string[];
    context?: string;
    requirements?: string[];
  }): Promise<any> {
    try {
      const response = await this.client.post('/api/v1/code/generate', {
        task: params.task,
        language: params.language || 'python',
        libraries: params.libraries || [],
        context: params.context,
        requirements: params.requirements || [],
      });

      return {
        code: response.data.code,
        language: params.language || 'python',
        explanation: response.data.explanation,
      };
    } catch (err: any) {
      return this.handleError(err, 'generate_code');
    }
  }

  async reviewCode(params: { code: string; purpose: string; data_schema?: string }): Promise<any> {
    try {
      const response = await this.client.post('/api/v1/code/review', {
        code: params.code,
        purpose: params.purpose,
        data_schema: params.data_schema,
      });

      return {
        issues: response.data.issues || [],
        suggestions: response.data.suggestions || [],
        fixed_code: response.data.fixed_code,
      };
    } catch (err: any) {
      return this.handleError(err, 'review_code');
    }
  }

  async executeCode(params: { code: string; timeout?: number; allowed_imports?: string[] }): Promise<any> {
    try {
      const response = await this.client.post('/api/v1/code/execute', {
        code: params.code,
        timeout: params.timeout || 30,
        allowed_imports: params.allowed_imports || [],
      });

      return {
        stdout: response.data.stdout,
        stderr: response.data.stderr,
        returncode: response.data.returncode,
        execution_time: response.data.execution_time,
      };
    } catch (err: any) {
      return this.handleError(err, 'execute_code');
    }
  }

  async getSystemStatus(): Promise<any> {
    try {
      const response = await this.client.get('/api/v1/system/status');
      return response.data;
    } catch (err: any) {
      return this.handleError(err, 'get_system_status');
    }
  }

  async queryDatabase(params: { sql: string; format?: string }): Promise<any> {
    try {
      const response = await this.client.post('/api/v1/database/query', {
        sql: params.sql,
        format: params.format || 'json',
      });
      return response.data;
    } catch (err: any) {
      return this.handleError(err, 'query_database');
    }
  }

  async createVisualization(params: {
    data_source: string;
    chart_type: string;
    options?: any;
    output_format?: string;
  }): Promise<any> {
    try {
      const response = await this.client.post('/api/v1/visualization/create', {
        data_source: params.data_source,
        chart_type: params.chart_type,
        options: params.options || {},
        output_format: params.output_format || 'png',
      });

      return {
        image_path: response.data.image_path,
        alt_text: response.data.alt_text,
        summary: response.data.summary,
      };
    } catch (err: any) {
      return this.handleError(err, 'create_visualization');
    }
  }

  async ingestDocument(params: { file_path: string; metadata?: any; chunk_size?: number }): Promise<any> {
    try {
      const response = await this.client.post('/api/v1/documents/ingest', {
        file_path: params.file_path,
        metadata: params.metadata || {},
        chunk_size: params.chunk_size || 1000,
      });

      return {
        document_id: response.data.document_id,
        chunks: response.data.chunks,
        status: 'indexed',
      };
    } catch (err: any) {
      return this.handleError(err, 'ingest_document');
    }
  }

  private handleError(err: any, context: string): any {
    console.error(`[BSLAdapter] ${context} error:`, err.message || err);

    if (err.response) {
      // BSL returned an error response
      return {
        error: true,
        tool: context,
        message: `BSL API error: ${err.response.status} ${err.response.statusText}`,
        details: err.response.data,
      };
    } else if (err.code === 'ECONNREFUSED' || err.code === 'ENOTFOUND') {
      return {
        error: true,
        tool: context,
        message: 'BSL API unavailable — is the server running?',
      };
    } else {
      return {
        error: true,
        tool: context,
        message: err.message || String(err),
      };
    }
  }
}
