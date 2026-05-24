# BAKERSTREET-LABS-2025
"""
Baker Street Laboratory - Research Orchestrator
Coordinates multi-agent research workflow combining web search, HF Hub, and AI analysis.
"""

import asyncio
import json
from typing import Dict, List, Optional, Any
from datetime import datetime

from research.web_search import WebResearcher, web_research
from research.hf_hub import HFHubResearcher, research_hf_hub
from research.local_inference import OllamaClient, analyze_with_ai


class ResearchOrchestrator:
    """
    Coordinates the full research workflow:
    1. Web search and content extraction
    2. Hugging Face Hub research
    3. AI analysis and synthesis
    """
    
    def __init__(self, ollama_url: str = None):
        self.ollama_client = OllamaClient(base_url=ollama_url)
        self.web_researcher = WebResearcher()
        self.hf_researcher = HFHubResearcher()
    
    def conduct_research(self, query: str, agent_type: str = "orchestrator", 
                        max_sources: int = 5) -> Dict[str, Any]:
        """
        Conduct comprehensive research using all available tools.
        
        Args:
            query: The research query
            agent_type: Type of agent to use for analysis
            max_sources: Maximum number of sources to research
            
        Returns:
            Complete research report
        """
        results = {
            "query": query,
            "agent_type": agent_type,
            "timestamp": datetime.now().isoformat(),
            "phases": {}
        }
        
        # Phase 1: Web Research
        print(f"Phase 1: Web research for '{query}'...")
        web_results = self.web_researcher.research(query, max_sources=max_sources)
        results["phases"]["web_research"] = web_results
        
        # Phase 2: HF Hub Research
        print(f"Phase 2: Hugging Face Hub research...")
        hf_results = self.hf_researcher.comprehensive_research(query, limit=3)
        results["phases"]["hf_hub_research"] = hf_results
        
        # Phase 3: AI Analysis
        print(f"Phase 3: AI analysis with {agent_type} agent...")
        combined_data = {
            "web_results": web_results.get("search_results", [])[:3],
            "hf_results": {
                "models": hf_results.get("models", [])[:2],
                "datasets": hf_results.get("datasets", [])[:2]
            }
        }
        
        ai_analysis = analyze_with_ai(query, combined_data, agent_type, self.ollama_client)
        results["phases"]["ai_analysis"] = ai_analysis
        
        # Phase 4: Synthesis
        results["synthesis"] = self._synthesize_results(results)
        
        # Flatten for display compatibility
        results["web_results"] = web_results
        results["hf_results"] = hf_results
        results["ai_analysis"] = ai_analysis
        results["mode"] = "full"
        results["agent"] = agent_type
        
        return results
    
    def quick_research(self, query: str, agent_type: str = "orchestrator") -> Dict[str, Any]:
        """Quick research using only web search and AI analysis"""
        results = {
            "query": query,
            "agent_type": agent_type,
            "agent": agent_type,
            "mode": "quick",
            "timestamp": datetime.now().isoformat()
        }
        
        # Web search only
        web_results = web_research(query, max_sources=3)
        results["web_results"] = web_results
        
        # AI analysis
        ai_analysis = analyze_with_ai(query, web_results, agent_type, self.ollama_client)
        results["ai_analysis"] = ai_analysis
        
        return results
    
    def hf_hub_only_research(self, query: str) -> Dict[str, Any]:
        """Research using only Hugging Face Hub"""
        results = research_hf_hub(query, limit=5)
        results["mode"] = "hf_only"
        return results
    
    def _synthesize_results(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Create a synthesis of all research phases"""
        web_phase = results.get("phases", {}).get("web_research", {})
        hf_phase = results.get("phases", {}).get("hf_hub_research", {})
        ai_phase = results.get("phases", {}).get("ai_analysis", "")
        
        return {
            "total_web_sources": len(web_phase.get("search_results", [])),
            "total_hf_resources": hf_phase.get("total_results", 0),
            "key_findings": ai_phase[:1000] if ai_phase else "No AI analysis available",
            "sources": {
                "web": [r.get("url", "") for r in web_phase.get("search_results", [])[:5]],
                "hf_models": [m.get("url", "") for m in hf_phase.get("models", [])[:3]],
                "hf_datasets": [d.get("url", "") for d in hf_phase.get("datasets", [])[:3]]
            }
        }


def run_research(query: str, agent_type: str = "orchestrator",
                ollama_url: str = None, mode: str = "full") -> Dict[str, Any]:
    """
    Main entry point for research.

    Args:
        query: Research query
        agent_type: Agent type (orchestrator, scientific, creative, code, legal, vision)
        ollama_url: Ollama server URL (default: http://localhost:11434)
        mode: Research mode - "full", "quick", or "hf_only"
    """
    orchestrator = ResearchOrchestrator(ollama_url=ollama_url)
    
    if mode == "full":
        return orchestrator.conduct_research(query, agent_type)
    elif mode == "quick":
        return orchestrator.quick_research(query, agent_type)
    elif mode == "hf_only":
        return orchestrator.hf_hub_only_research(query)
    else:
        return {"error": f"Unknown mode: {mode}"}
