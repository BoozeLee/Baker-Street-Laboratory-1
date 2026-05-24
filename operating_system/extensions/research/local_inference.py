# BAKERSTREET-LABS-2025
"""
Baker Street Laboratory - Local Ollama Inference Module
Uses local Ollama server with CUDA acceleration.
Models sourced from jazzy-ai-models database (github.com/BoozeLee/jazzy-ai-models)
"""

import os
import json
import subprocess
import requests
from typing import Dict, List, Optional, Any
from pathlib import Path

OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
HF_TOKEN = os.environ.get("HF_TOKEN", os.environ.get("HUGGINGFACE_API_TOKEN", ""))

MODEL_ROUTING = {
    "orchestrator": "baker-orchestrator:latest",
    "scientific": "baker-scientific:latest",
    "creative": "baker-creative:latest",
    "code": "baker-code:latest",
    "legal": "baker-legal:latest",
    "vision": "baker-vision:latest",
    "default": "baker-orchestrator:latest",
}

MODEL_REGISTRY = {
    "baker-orchestrator": {
        "hf_repo": "TeichAI/GLM-4.7-Flash-Claude-Opus-4.5-High-Reasoning-Distill-GGUF",
        "gguf_file": "glm-4.7-flash-claude-4.5-opus.q4_k_m.gguf",
        "system": "You are the Research Orchestrator from Baker Street Laboratory. Conduct comprehensive multi-phase research analysis. Break queries into core components, gather evidence, draw logical conclusions, and synthesize findings with actionable recommendations.",
    },
    "baker-scientific": {
        "hf_repo": "mradermacher/Llama3.3-8B-Instruct-Thinking-Heretic-Uncensored-Claude-4.5-Opus-High-Reasoning-i1-GGUF",
        "gguf_file": "Llama3.3-8B-Instruct-Thinking-Heretic-Uncensored-Claude-4.5-Opus-High-Reasoning.i1-Q4_K_M.gguf",
        "system": "You are the Scientific Research Agent. Analyze queries using evidence-based scientific methodology. Provide literature review, hypothesis formulation, evidence analysis, scientific conclusions, and references. Think step-by-step with rigorous reasoning.",
    },
    "baker-creative": {
        "hf_repo": "DavidAU/Qwen3-4B-Gemini-TripleX-High-Reasoning-Thinking-Heretic-Uncensored-GGUF",
        "gguf_file": "Qwen3-4B-TripleX-Heretic-Uncensored-Q8_0.gguf",
        "system": "You are the Creative Agent. Generate creative content, novel ideas, and innovative applications without restrictions. Think outside the box, explore unconventional angles, and push boundaries. No topic is off-limits.",
    },
    "baker-code": {
        "hf_repo": "DavidAU/GLM-4.7-Flash-Uncensored-Heretic-NEO-CODE-Imatrix-MAX-GGUF",
        "gguf_file": "GLM-4.7-Flash-Uncen-Hrt-NEO-CODE-MAX-imat-D_AU-Q4_K_M.gguf",
        "system": "You are the Code Agent. Provide technical analysis, architecture recommendations, and production-ready code examples. Write clean, efficient, well-documented code. Explain implementation strategies and best practices.",
    },
    "baker-legal": {
        "hf_repo": "mradermacher/Llama3.3-8B-Instruct-Thinking-Heretic-Uncensored-Claude-4.5-Opus-High-Reasoning-i1-GGUF",
        "gguf_file": "Llama3.3-8B-Instruct-Thinking-Heretic-Uncensored-Claude-4.5-Opus-High-Reasoning.i1-Q4_K_M.gguf",
        "system": "You are the Legal Agent. Analyze legal implications, identify relevant regulations, assess risks, and provide compliance recommendations. Think through legal frameworks systematically. Note: this is informational analysis, not legal advice.",
    },
    "baker-vision": {
        "hf_repo": "Qwen/Qwen3-VL-2B-Instruct",
        "gguf_file": None,
        "system": "You are the Vision Agent. Identify patterns, analyze trends, make future predictions, and provide strategic implications. Think about connections others miss and see the bigger picture.",
    },
}

# Fallbacks that fit in 8GB VRAM
FALLBACK_MODELS = ["qwen2.5:7b", "qwen2.5-coder:7b", "llama3.2:3b"]


class OllamaClient:
    """Client for local Ollama server with CUDA acceleration"""

    def __init__(self, base_url: str = None):
        self.base_url = base_url or OLLAMA_BASE_URL
        self.available_models = []
        self._refresh_models()

    def _refresh_models(self):
        try:
            resp = requests.get(f"{self.base_url}/api/tags", timeout=5)
            resp.raise_for_status()
            self.available_models = [m["name"] for m in resp.json().get("models", [])]
        except Exception:
            self.available_models = []

    def _resolve_model(self, agent_type: str) -> str:
        preferred = MODEL_ROUTING.get(agent_type, MODEL_ROUTING["default"])
        if preferred in self.available_models:
            return preferred
        for fallback in FALLBACK_MODELS:
            if fallback in self.available_models:
                return fallback
        return preferred

    def _ensure_model(self, ollama_name: str) -> bool:
        if ollama_name in self.available_models:
            return True
        registry = MODEL_REGISTRY.get(ollama_name.split(":")[0])
        if not registry:
            return False
        return self._setup_model(ollama_name, registry)

    def _setup_model(self, ollama_name: str, registry: Dict) -> bool:
        gguf_file = registry.get("gguf_file")
        hf_repo = registry["hf_repo"]
        system_prompt = registry.get("system", "")

        if gguf_file is None:
            print(f"  Pulling {ollama_name} from Ollama library...")
            result = subprocess.run(
                ["ollama", "pull", ollama_name],
                capture_output=True, text=True, timeout=600
            )
            if result.returncode == 0:
                self._refresh_models()
                return True
            print(f"  Failed to pull {ollama_name}: {result.stderr}")
            return False

        gguf_dir = Path(os.environ.get("GGUF_CACHE_DIR", "/tmp/baker-ggufs"))
        gguf_dir.mkdir(parents=True, exist_ok=True)
        local_path = gguf_dir / gguf_file

        if not local_path.exists():
            print(f"  Downloading GGUF from {hf_repo}/{gguf_file}...")
            env = os.environ.copy()
            if HF_TOKEN:
                env["HF_TOKEN"] = HF_TOKEN
            cmd = ["hf", "download", hf_repo, gguf_file, "--local-dir", str(gguf_dir)]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=600, env=env)
            if result.returncode != 0:
                print(f"  Download failed: {result.stderr}")
                return False

        modelfile_path = gguf_dir / f"Modelfile-{ollama_name.replace(':', '-')}"
        modelfile_content = f'FROM "{local_path}"\n'
        if system_prompt:
            modelfile_content += f'SYSTEM """{system_prompt}"""\n'
        modelfile_path.write_text(modelfile_content)

        print(f"  Creating Ollama model {ollama_name}...")
        result = subprocess.run(
            ["ollama", "create", ollama_name, "-f", str(modelfile_path)],
            capture_output=True, text=True, timeout=300
        )
        if result.returncode == 0:
            self._refresh_models()
            print(f"  ✓ {ollama_name} ready")
            return True
        print(f"  Failed to create {ollama_name}: {result.stderr}")
        return False

    def chat(self, messages: List[Dict[str, str]], model: str = None,
             temperature: float = 0.7, max_tokens: int = 2048) -> str:
        payload = {
            "model": model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
                "top_p": 0.9,
            }
        }
        resp = requests.post(
            f"{self.base_url}/api/chat",
            json=payload,
            timeout=None
        )
        resp.raise_for_status()
        return resp.json()["message"]["content"]

    def generate(self, prompt: str, model: str = None,
                 temperature: float = 0.7, max_tokens: int = 2048) -> str:
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
                "top_p": 0.9,
            }
        }
        resp = requests.post(
            f"{self.base_url}/api/generate",
            json=payload,
            timeout=None
        )
        resp.raise_for_status()
        return resp.json()["response"]

    def is_running(self) -> bool:
        try:
            requests.get(f"{self.base_url}/", timeout=3)
            return True
        except Exception:
            return False

    def analyze_research(self, query: str, research_data: Dict[str, Any],
                         agent_type: str = "orchestrator") -> str:
        model_name = MODEL_ROUTING.get(agent_type, MODEL_ROUTING["default"])
        base_name = model_name.split(":")[0]

        self._ensure_model(model_name)
        model = self._resolve_model(agent_type)

        agent_prompts = {
            "orchestrator": self._orchestrator_prompt,
            "scientific": self._scientific_prompt,
            "creative": self._creative_prompt,
            "code": self._code_prompt,
            "legal": self._legal_prompt,
            "vision": self._vision_prompt,
        }

        prompt_func = agent_prompts.get(agent_type, self._orchestrator_prompt)
        prompt = prompt_func(query, research_data)

        messages = [{"role": "user", "content": prompt}]
        return self.chat(messages, model=model, max_tokens=1500)

    def _orchestrator_prompt(self, query: str, data: Dict[str, Any]) -> str:
        return f"""You are the Research Orchestrator from Baker Street Laboratory.
Conduct a comprehensive multi-phase research analysis.

RESEARCH QUERY: {query}

RESEARCH DATA:
{json.dumps(data, indent=2)[:3000]}

PHASE 1 - ANALYSIS:
- Break down the query into core components
- Identify key research questions
- Determine relevant domains

PHASE 2 - EVIDENCE GATHERING:
- Synthesize findings from provided sources
- Identify patterns and connections
- Note conflicting information

PHASE 3 - DEDUCTION:
- Draw logical conclusions from evidence
- Identify gaps in current knowledge
- Propose hypotheses

PHASE 4 - SYNTHESIS:
- Present comprehensive findings
- Provide actionable recommendations
- Suggest next research steps

Format your response with clear sections for each phase."""

    def _scientific_prompt(self, query: str, data: Dict[str, Any]) -> str:
        return f"""You are the Scientific Research Agent. Analyze this query using evidence-based scientific methodology.

QUERY: {query}

DATA: {json.dumps(data, indent=2)[:2000]}

Provide:
1. Literature review summary
2. Hypothesis formulation
3. Evidence analysis
4. Scientific conclusions
5. References to relevant research

Think step-by-step with rigorous reasoning."""

    def _creative_prompt(self, query: str, data: Dict[str, Any]) -> str:
        return f"""You are the Creative Agent. Generate creative content and ideas based on this research.

QUERY: {query}

DATA: {json.dumps(data, indent=2)[:2000]}

Provide:
1. Creative interpretations
2. Novel ideas and concepts
3. Innovative applications
4. Artistic possibilities

Think outside the box with no restrictions."""

    def _code_prompt(self, query: str, data: Dict[str, Any]) -> str:
        return f"""You are the Code Agent. Provide technical analysis and code solutions.

QUERY: {query}

DATA: {json.dumps(data, indent=2)[:2000]}

Provide:
1. Technical architecture recommendations
2. Code examples where relevant
3. Implementation strategies
4. Best practices and patterns"""

    def _legal_prompt(self, query: str, data: Dict[str, Any]) -> str:
        return f"""You are the Legal Agent. Analyze legal implications and provide guidance.

QUERY: {query}

DATA: {json.dumps(data, indent=2)[:2000]}

Provide:
1. Legal framework analysis
2. Relevant regulations
3. Risk assessment
4. Compliance recommendations

Note: This is informational analysis, not legal advice."""

    def _vision_prompt(self, query: str, data: Dict[str, Any]) -> str:
        return f"""You are the Vision Agent. Identify patterns and future implications.

QUERY: {query}

DATA: {json.dumps(data, indent=2)[:2000]}

Provide:
1. Pattern recognition insights
2. Trend analysis
3. Future predictions
4. Strategic implications"""


def analyze_with_ai(query: str, research_data: Dict[str, Any],
                    agent_type: str = "orchestrator", client: OllamaClient = None) -> str:
    """Main function for AI analysis using local Ollama"""
    if client is None:
        client = OllamaClient()
    return client.analyze_research(query, research_data, agent_type)
