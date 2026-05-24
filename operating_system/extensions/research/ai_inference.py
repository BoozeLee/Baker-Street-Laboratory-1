# BAKERSTREET-LABS-2025
"""
Baker Street Laboratory - AI Inference Module
Uses Hugging Face Inference API for research analysis and synthesis.
"""

import os
import json
import requests
from typing import Dict, List, Optional, Any
from datetime import datetime


class HFInferenceClient:
    """Client for Hugging Face Inference API"""
    
    def __init__(self, token: str = None):
        self.token = token or os.environ.get("HF_TOKEN")
        self.api_url = "https://api-inference.huggingface.co/models"
        self.headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}
    
    def query(self, model: str, inputs: Dict[str, Any], parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        """Query a model via Inference API"""
        url = f"{self.api_url}/{model}"
        payload = {"inputs": inputs}
        if parameters:
            payload["parameters"] = parameters
        
        response = requests.post(url, headers=self.headers, json=payload, timeout=60)
        response.raise_for_status()
        return response.json()
    
    def text_generation(self, prompt: str, model: str = "mistralai/Mixtral-8x7B-Instruct-v0.1", 
                       max_tokens: int = 2048) -> str:
        """Generate text using a model"""
        try:
            result = self.query(model, prompt, {
                "max_new_tokens": max_tokens,
                "temperature": 0.7,
                "top_p": 0.9,
                "return_full_text": False
            })
            
            if isinstance(result, list) and len(result) > 0:
                return result[0].get("generated_text", "")
            return str(result)
        except Exception as e:
            return f"Error generating text: {e}"
    
    def analyze_research(self, query: str, research_data: Dict[str, Any], 
                        agent_type: str = "orchestrator") -> str:
        """
        Analyze research data using AI.
        Generates structured research report.
        """
        agent_prompts = {
            "orchestrator": self._orchestrator_prompt,
            "scientific": self._scientific_prompt,
            "creative": self._creative_prompt,
            "code": self._code_prompt,
            "legal": self._legal_prompt,
            "vision": self._vision_prompt
        }
        
        prompt_func = agent_prompts.get(agent_type, self._orchestrator_prompt)
        prompt = prompt_func(query, research_data)
        
        return self.text_generation(prompt, max_tokens=3000)
    
    def _orchestrator_prompt(self, query: str, data: Dict[str, Any]) -> str:
        """Multi-phase research orchestrator prompt"""
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
5. References to relevant research"""

    def _creative_prompt(self, query: str, data: Dict[str, Any]) -> str:
        return f"""You are the Creative Agent. Generate creative content and ideas based on this research.

QUERY: {query}

DATA: {json.dumps(data, indent=2)[:2000]}

Provide:
1. Creative interpretations
2. Novel ideas and concepts
3. Innovative applications
4. Artistic possibilities"""

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
4. Compliance recommendations"""

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
                   agent_type: str = "orchestrator", token: str = None) -> str:
    """Main function for AI analysis of research"""
    client = HFInferenceClient(token=token)
    return client.analyze_research(query, research_data, agent_type)
