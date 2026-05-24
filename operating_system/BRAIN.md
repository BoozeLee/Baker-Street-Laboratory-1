# Baker Street Laboratory — Tool Reference

## Available Tools & Capabilities

### Research Tools

#### conduct_research
**Purpose**: Execute a full research pipeline on a given query.
**Parameters**:
- `query` (string, required): Research question or topic
- `output_dir` (string, optional): Output directory (default: "research/api_output")
**Returns**: Research report with methodology, findings, citations
**Execution Tier**: Tier 2 (Async, 2-10 minutes)
**Example**:
```json
{
  "tool": "conduct_research",
  "parameters": {
    "query": "effects of psilocybin on treatment-resistant depression",
    "output_dir": "research/psychedelic_studies"
  }
}
```
**Notes**: This is a long-running operation. Call `get_job_status` to monitor progress.

#### semantic_search
**Purpose**: Find semantically similar documents using vector embeddings.
**Parameters**:
- `query` (string): Search query
- `k` (int): Number of results (default: 10, max: 100)
- `threshold` (float): Similarity threshold 0-1 (default: 0.7)
- `collection` (string): Index to search (default: "research_papers")
**Returns**: List of matching documents with similarity scores + metadata
**Execution Tier**: Tier 0 (Instant, local)
**Example**:
```json
{
  "tool": "semantic_search",
  "parameters": {
    "query": "5-HT2A receptor binding affinity",
    "k": 5,
    "threshold": 0.75
  }
}
```

#### batch_analyze_images
**Purpose**: Process multiple images (charts, diagrams, scans) in parallel.
**Parameters**:
- `images` (array of strings): Array of image paths or URLs
- `analysis_type` (string): "chart" | "diagram" | "microscopy" | "general"
- `context` (string): Optional context about what to look for
**Returns**: Structured analysis of each image with descriptions + inferred insights
**Model**: Requires Vision model (LLaVA) to be operational
**Execution Tier**: Tier 1 (Fast, <30s)
**Example**:
```json
{
  "tool": "batch_analyze_images",
  "parameters": {
    "images": ["/data/figures/fmri_activation.png", "https://example.com/table.png"],
    "analysis_type": "chart",
    "context": "fMRI brain activation study"
  }
}
```

### Code & Analysis Tools

#### generate_code
**Purpose**: Generate Python/R/Julia code for data analysis, simulations, or visualizations.
**Parameters**:
- `task` (string): Description of what code should do
- `language` (string): "python" | "r" | "julia" (default: "python")
- `libraries` (array): Preferred libraries (e.g., ["pandas", "scipy", "matplotlib"])
- `context` (string): Relevant data schema or sample
- `requirements` (array): Specific statistical tests or methods needed
**Returns**: Complete, runnable code with comments + usage example
**Execution Tier**: Tier 1 (Fast)
**Model**: Coder model (DeepSeek-Coder)
**Example**:
```json
{
  "tool": "generate_code",
  "parameters": {
    "task": "Perform paired t-test on pre/post treatment scores",
    "language": "python",
    "libraries": ["scipy.stats", "pandas"],
    "context": "CSV with columns: subject_id, pre_score, post_score",
    "requirements": ["check normality", "calculate effect size"]
  }
}
```

#### review_code
**Purpose**: Review generated code for bugs, style, performance, and correctness.
**Parameters**:
- `code` (string): Code to review
- `purpose` (string): What the code should accomplish
- `data_schema` (string, optional): Expected input/output format
**Returns**: Issues found (bugs, security, style) + suggested improvements + fixed version
**Execution Tier**: Tier 1 (Fast)
**Model**: Coder model
**Example**:
```json
{
  "tool": "review_code",
  "parameters": {
    "code": "import pandas as pd\ndf = pd.read_csv('data.csv')\nprint(df.mean())",
    "purpose": "Calculate average score from experimental data"
  }
}
```

#### execute_code
**Purpose**: Run Python code in a sandboxed environment and return results.
**Parameters**:
- `code` (string): Valid Python code to execute
- `timeout` (int): Max execution time in seconds (default: 30, max: 300)
- `allowed_imports` (array): Allowed modules (default: ["numpy", "pandas", "scipy", "matplotlib", "json", "csv"])
**Returns**: stdout, stderr, return code, execution time
**Execution Tier**: Tier 0 (Local subprocess, sandboxed)
**Security**: Code runs in restricted environment; network access disabled; filesystem read-only except /tmp
**Example**:
```json
{
  "tool": "execute_code",
  "parameters": {
    "code": "import pandas as pd\ndf = pd.read_csv('/data/sample.csv')\nprint(df.describe())",
    "timeout": 10,
    "allowed_imports": ["pandas", "numpy"]
  }
}
```

### Data & Memory Tools

#### query_database
**Purpose**: Execute SQL queries on research database.
**Parameters**:
- `sql` (string): SQL query (SELECT only for safety)
- `format` (string): "json" | "csv" | "table" (default: "json")
**Returns**: Query results
**Security**: Only SELECT allowed; no modification queries
**Execution Tier**: Tier 0 (Instant)
**Example**:
```json
{
  "tool": "query_database",
  "parameters": {
    "sql": "SELECT title, authors, abstract FROM papers WHERE year > 2020 LIMIT 10",
    "format": "json"
  }
}
```

#### create_visualization
**Purpose**: Generate charts/plots from data.
**Parameters**:
- `data_source` (string): CSV path OR SQL query
- `chart_type` (string): "line" | "bar" | "scatter" | "histogram" | "heatmap" | "box"
- `options` (object): { title, x_label, y_label, color_scheme }
- `output_format` (string): "png" | "svg" | "pdf" (default: "png")
**Returns**: Image file path + alt-text description + data summary
**Execution Tier**: Tier 1 (Fast)
**Example**:
```json
{
  "tool": "create_visualization",
  "parameters": {
    "data_source": "SELECT response_time, accuracy FROM experiments",
    "chart_type": "scatter",
    "options": {"title": "Response Time vs Accuracy", "x_label": "RT (ms)", "y_label": "Accuracy (%)"},
    "output_format": "svg"
  }
}
```

#### ingest_document
**Purpose**: Parse and index a document (PDF, DOCX, TXT) into vector store.
**Parameters**:
- `file_path` (string): Path or URL to document
- `metadata` (object): { title, authors, date, tags }
- `chunk_size` (int): Text chunk size for embedding (default: 1000)
**Returns**: Document ID + chunk count + status
**Execution Tier**: Tier 1 (Fast)
**Example**:
```json
{
  "tool": "ingest_document",
  "parameters": {
    "file_path": "/data/papers/2024_quantum_cryptography.pdf",
    "metadata": {"title": "...", "tags": ["quantum", "cryptography"]},
    "chunk_size": 500
  }
}
```

### Audio & Media Tools

#### transcribe_audio
**Purpose**: Convert speech audio to text using Whisper model.
**Parameters**:
- `audio_path` (string): Path to audio file (WAV, MP3, AAC)
- `language` (string): Language code (default: "en")
- `diarization` (bool): Separate speakers? (default: false)
**Returns**: Transcript with timestamps + speaker labels if diarized
**Model**: Audio model (Qwen2-Audio)
**Execution Tier**: Tier 2 (Medium, 10-60s per minute of audio)
**Example**:
```json
{
  "tool": "transcribe_audio",
  "parameters": {
    "audio_path": "/data/interviews/subject1.mp3",
    "language": "en",
    "diarization": true
  }
}
```

#### analyze_video_frame
**Purpose**: Extract and analyze frames from video files.
**Parameters**:
- `video_path` (string): Path to video file
- `timestamps` (array): List of timestamps in seconds to extract
- `analysis_prompt` (string): What to look for in frames
**Returns**: For each frame: description + detected objects + relevant observations
**Model**: Vision model
**Execution Tier**: Tier 2 (Slow)
**Example**:
```json
{
  "tool": "analyze_video_frame",
  "parameters": {
    "video_path": "/data/experiments/trial1.mp4",
    "timestamps": [0, 30, 60, 90],
    "analysis_prompt": "Look for pupil dilation changes"
  }
}
```

### System & Utility Tools

#### get_system_status
**Purpose**: Check operational status of BSL models and services.
**Parameters**: None
**Returns**: Object with model statuses (operational/loading/error), GPU memory, uptime
**Execution Tier**: Tier 0 (Instant)
**Example**:
```json
{
  "tool": "get_system_status"
}
```

#### list_research_projects
**Purpose**: Show all active/completed research projects.
**Parameters**:
- `status` (string): Filter by "active" | "completed" | "failed" (optional)
- `limit` (int): Max results (default: 20)
**Returns**: List of projects with summaries, dates, statuses
**Execution Tier**: Tier 0 (Instant)

#### get_job_status
**Purpose**: Monitor status of an async job.
**Parameters**:
- `job_id` (string): Job identifier from previous response
**Returns**: { status: "pending"|"running"|"completed"|"failed", progress_pct, logs, result_url }
**Execution Tier**: Tier 0 (Instant)

## Tool Selection Decision Tree

```
User query received
  ↓
Is this a research question requiring multi-source synthesis?
  ├─ YES → conduct_research (async, monitor with get_job_status)
  │
  ├─ Is there an image/video/audio to analyze?
  │   ├─ Image → batch_analyze_images
  │   ├─ Audio → transcribe_audio
  │   └─ Video → analyze_video_frame (select frames first)
  │
  ├─ Is code needed?
  │   ├─ Write new → generate_code
  │   ├─ Review existing → review_code
  │   └─ Test/debug → execute_code (sandbox)
  │
  ├─ Want to find related documents?
  │   ├─ Similar to X → semantic_search
  │   └─ Insert new doc → ingest_document
  │
  └─ Just need factual recall?
      ├─ From memory → use built-in recall (no tool)
      └─ Recent info → conduct_research (short form)
```

## Common Pitfalls & Solutions

### Problem: "Vision model not available"
**Solution**: Check status with `get_system_status`, wait for model to load, or use `batch_analyze_images` with `analysis_type: "general"` as fallback.

### Problem: "Research taking too long"
**Solution**: Long-running research runs async. Call `get_job_status <job_id>` to monitor, or don't wait — just let it complete and check later.

### Problem: "semantic_search returns no results"
**Solution**: Increase threshold (lower similarity requirement), ensure documents ingested first via `ingest_document`.

### Problem: "Code execution timeout"
**Solution**: Reduce computation, request larger timeout (max 300s), or break into steps.

### Problem: "Memory full / database locked"
**Solution**: Vector store uses Qdrant with 128k+ capacity; if SQLite locked, ensure WAL mode enabled.

## Performance Tips

1. **Batch operations**: `semantic_search(k=20)` fetches 20 results in 1 query vs. 20x single queries
2. **Write-ahead logging**: SQLite WAL mode enabled → concurrent reads during writes
3. **Model caching**: Ollama keeps models in GPU memory; first inference per model incurs cold-start penalty
4. **Async tool calls**: Vision + Audio + LongContext models should run in parallel when possible
5. **Streaming results**: Use `conduct_research` with streaming output for large reports (split into sections)

## Security & Safety

**Command allowlist**: Only listed tools may be executed.
**Input validation**: All parameters type-checked; SQL queries parsed for modification keywords; code execution sandboxed.
**Output sanitization**: API keys, tokens automatically redacted before display.
**Audit trail**: Every tool call logged with user, timestamp, parameters, result hash.

---

**Tool schemas are dynamically loaded** from system status. If a model is offline, corresponding tools are automatically disabled.
