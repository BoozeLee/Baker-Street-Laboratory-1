interface ToolSchema {
  description: string;
  parameters: any; // JSON Schema
  handler: (params: any) => Promise<any>;
}

export class ToolRegistry {
  private tools: Map<string, ToolSchema> = new Map();
  private available: Set<string> = new Set();

  register(name: string, schema: ToolSchema): void {
    this.tools.set(name, schema);
    this.available.add(name);
  }

  describeAll(): string {
    const lines: string[] = [];
    for (const [name, schema] of this.tools) {
      const status = this.available.has(name) ? '✅' : '❌';
      lines.push(`${status} **${name}** — ${schema.description}`);
      lines.push(`   Parameters: ${JSON.stringify(schema.parameters.properties)}`);
    }
    return lines.join('\n');
  }

  getAllSchemas(): any[] {
    return Array.from(this.tools.entries()).map(([name, schema]) => ({
      name,
      description: schema.description,
      parameters: schema.parameters,
    }));
  }

  async execute(name: string, parameters: any): Promise<any> {
    if (!this.available.has(name)) {
      throw new Error(`Tool '${name}' is not available`);
    }
    const schema = this.tools.get(name);
    if (!schema) {
      throw new Error(`Tool '${name}' not found`);
    }
    return await schema.handler(parameters);
  }

  getStatus(): Record<string, any> {
    return {
      total: this.tools.size,
      available: this.available.size,
      unavailable: this.tools.size - this.available.size,
      tools: Object.fromEntries(
        Array.from(this.tools.keys()).map((name) => [
          name,
          { available: this.available.has(name) },
        ])
      ),
    };
  }

  markAvailable(): void {
    // All tools become available when BSL adapter connects
    this.available = new Set(this.tools.keys());
  }

  setAvailable(name: string, available: boolean): void {
    if (available) {
      this.available.add(name);
    } else {
      this.available.delete(name);
    }
  }
}
