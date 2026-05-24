#!/usr/bin/env python3
"""
Baker Street Laboratory - Baker Street Analyzer Implementation
Advanced multi-model AI analyzer with GPT-4o, Claude-3.5-Sonnet, and Gemini Pro integration
"""

import os
import json
import datetime
from typing import Dict, List, Any, Optional
import requests
import asyncio
import aiohttp

class BakerStreetAnalyzer:
    """
    Advanced Baker Street Analyzer with multi-model integration
    """
    
    def __init__(self):
        self.name = "Baker Street Analyzer"
        self.version = "2.0.0"
        self.description = "Advanced multi-model AI analyzer with enterprise-grade capabilities"
        
        # API configurations
        self.api_configs = {
            "openai": {
                "api_key": os.getenv("OPENAI_API_KEY", ""),
                "base_url": "https://api.openai.com/v1",
                "models": ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo"]
            },
            "anthropic": {
                "api_key": os.getenv("ANTHROPIC_API_KEY", ""),
                "base_url": "https://api.anthropic.com/v1",
                "models": ["claude-3-5-sonnet-20241022", "claude-3-haiku-20240307", "claude-3-opus-20240229"]
            },
            "google": {
                "api_key": os.getenv("GOOGLE_AI_API_KEY", ""),
                "base_url": "https://generativelanguage.googleapis.com/v1beta",
                "models": ["gemini-pro", "gemini-pro-vision", "gemini-ultra"]
            }
        }
        
        # Analysis capabilities
        self.capabilities = {
            "reasoning": {
                "description": "Advanced logical reasoning and problem-solving",
                "models": ["gpt-4o", "claude-3-5-sonnet-20241022", "gemini-pro"],
                "use_cases": ["Complex problem analysis", "Strategic planning", "Decision support"]
            },
            "analysis": {
                "description": "Deep data analysis and pattern recognition",
                "models": ["gpt-4o", "claude-3-5-sonnet-20241022", "gemini-pro"],
                "use_cases": ["Data interpretation", "Trend analysis", "Insight generation"]
            },
            "research": {
                "description": "Comprehensive research and information synthesis",
                "models": ["claude-3-5-sonnet-20241022", "gpt-4o", "gemini-pro"],
                "use_cases": ["Market research", "Competitive analysis", "Technical research"]
            },
            "creative": {
                "description": "Creative problem-solving and innovation",
                "models": ["gpt-4o", "claude-3-5-sonnet-20241022", "gemini-pro"],
                "use_cases": ["Innovation strategies", "Creative solutions", "Brainstorming"]
            }
        }
        
        # Baker Street methodology
        self.methodology = {
            "observation": "Careful observation of all available data and evidence",
            "deduction": "Logical deduction from observed facts",
            "hypothesis": "Formation of testable hypotheses",
            "verification": "Systematic verification of hypotheses",
            "conclusion": "Drawing evidence-based conclusions"
        }

    async def analyze_with_model(self, query: str, capability: str, model: str) -> Dict[str, Any]:
        """Analyze query with specific model and capability"""
        try:
            if model.startswith("gpt-"):
                return await self._analyze_with_openai(query, capability, model)
            elif model.startswith("claude-"):
                return await self._analyze_with_anthropic(query, capability, model)
            elif model.startswith("gemini-"):
                return await self._analyze_with_google(query, capability, model)
            else:
                return {"error": f"Unknown model: {model}"}
        except Exception as e:
            return {"error": f"Analysis failed: {str(e)}"}

    async def _analyze_with_openai(self, query: str, capability: str, model: str) -> Dict[str, Any]:
        """Analyze with OpenAI models"""
        if not self.api_configs["openai"]["api_key"]:
            return {"error": "OpenAI API key not configured"}
        
        headers = {
            "Authorization": f"Bearer {self.api_configs['openai']['api_key']}",
            "Content-Type": "application/json"
        }
        
        system_prompt = self._get_system_prompt(capability)
        
        data = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ],
            "max_tokens": 4000,
            "temperature": 0.7
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.api_configs['openai']['base_url']}/chat/completions",
                headers=headers,
                json=data
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    return {
                        "model": model,
                        "capability": capability,
                        "response": result["choices"][0]["message"]["content"],
                        "usage": result.get("usage", {}),
                        "timestamp": datetime.datetime.now().isoformat()
                    }
                else:
                    return {"error": f"OpenAI API error: {response.status}"}

    async def _analyze_with_anthropic(self, query: str, capability: str, model: str) -> Dict[str, Any]:
        """Analyze with Anthropic models"""
        if not self.api_configs["anthropic"]["api_key"]:
            return {"error": "Anthropic API key not configured"}
        
        headers = {
            "x-api-key": self.api_configs["anthropic"]["api_key"],
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        }
        
        system_prompt = self._get_system_prompt(capability)
        
        data = {
            "model": model,
            "max_tokens": 4000,
            "system": system_prompt,
            "messages": [
                {"role": "user", "content": query}
            ]
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.api_configs['anthropic']['base_url']}/messages",
                headers=headers,
                json=data
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    return {
                        "model": model,
                        "capability": capability,
                        "response": result["content"][0]["text"],
                        "usage": result.get("usage", {}),
                        "timestamp": datetime.datetime.now().isoformat()
                    }
                else:
                    return {"error": f"Anthropic API error: {response.status}"}

    async def _analyze_with_google(self, query: str, capability: str, model: str) -> Dict[str, Any]:
        """Analyze with Google models"""
        if not self.api_configs["google"]["api_key"]:
            return {"error": "Google AI API key not configured"}
        
        system_prompt = self._get_system_prompt(capability)
        
        data = {
            "contents": [
                {
                    "parts": [
                        {"text": f"{system_prompt}\n\n{query}"}
                    ]
                }
            ],
            "generationConfig": {
                "maxOutputTokens": 4000,
                "temperature": 0.7
            }
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.api_configs['google']['base_url']}/models/{model}:generateContent?key={self.api_configs['google']['api_key']}",
                json=data
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    return {
                        "model": model,
                        "capability": capability,
                        "response": result["candidates"][0]["content"]["parts"][0]["text"],
                        "usage": result.get("usageMetadata", {}),
                        "timestamp": datetime.datetime.now().isoformat()
                    }
                else:
                    return {"error": f"Google AI API error: {response.status}"}

    def _get_system_prompt(self, capability: str) -> str:
        """Get system prompt for specific capability"""
        base_prompt = f"""
You are the Baker Street Analyzer, an advanced AI system based on Sherlock Holmes methodology.

Baker Street Methodology:
1. Observation: Careful observation of all available data and evidence
2. Deduction: Logical deduction from observed facts
3. Hypothesis: Formation of testable hypotheses
4. Verification: Systematic verification of hypotheses
5. Conclusion: Drawing evidence-based conclusions

Current Capability: {capability}
Description: {self.capabilities[capability]['description']}

Instructions:
- Apply the Baker Street methodology to all analysis
- Provide detailed, evidence-based reasoning
- Be thorough and systematic in your approach
- Draw clear, actionable conclusions
- Maintain the highest standards of analytical rigor
"""
        return base_prompt

    async def multi_model_analysis(self, query: str, capability: str) -> Dict[str, Any]:
        """Perform analysis with multiple models and synthesize results"""
        models = self.capabilities[capability]["models"]
        results = []
        
        # Run analysis with all models in parallel
        tasks = [self.analyze_with_model(query, capability, model) for model in models]
        model_results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        for i, result in enumerate(model_results):
            if isinstance(result, Exception):
                results.append({
                    "model": models[i],
                    "error": str(result)
                })
            else:
                results.append(result)
        
        # Synthesize results
        synthesis = self._synthesize_results(results, query, capability)
        
        return {
            "query": query,
            "capability": capability,
            "individual_results": results,
            "synthesis": synthesis,
            "timestamp": datetime.datetime.now().isoformat()
        }

    def _synthesize_results(self, results: List[Dict[str, Any]], query: str, capability: str) -> Dict[str, Any]:
        """Synthesize results from multiple models"""
        successful_results = [r for r in results if "error" not in r]
        
        if not successful_results:
            return {"error": "All model analyses failed"}
        
        # Extract key insights from each result
        insights = []
        for result in successful_results:
            insights.append({
                "model": result["model"],
                "insight": result["response"][:500] + "..." if len(result["response"]) > 500 else result["response"]
            })
        
        # Generate synthesis
        synthesis = {
            "summary": f"Multi-model analysis completed for {capability} capability",
            "models_used": len(successful_results),
            "total_models": len(results),
            "insights": insights,
            "recommendation": "Consider all model perspectives for comprehensive analysis",
            "confidence": "High" if len(successful_results) >= 2 else "Medium"
        }
        
        return synthesis

    def get_analysis_capabilities(self) -> Dict[str, Any]:
        """Get available analysis capabilities"""
        return {
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "capabilities": self.capabilities,
            "methodology": self.methodology,
            "api_status": {
                "openai": "configured" if self.api_configs["openai"]["api_key"] else "not_configured",
                "anthropic": "configured" if self.api_configs["anthropic"]["api_key"] else "not_configured",
                "google": "configured" if self.api_configs["google"]["api_key"] else "not_configured"
            }
        }

def main():
    """Main function to demonstrate Baker Street Analyzer"""
    print("🕵️‍♂️ Baker Street Laboratory - Baker Street Analyzer")
    print("=" * 60)
    
    # Initialize analyzer
    analyzer = BakerStreetAnalyzer()
    
    # Display analyzer information
    capabilities = analyzer.get_analysis_capabilities()
    print(f"\n🕵️‍♂️ Analyzer: {capabilities['name']}")
    print(f"Version: {capabilities['version']}")
    print(f"Description: {capabilities['description']}")
    
    # Display capabilities
    print(f"\n🎯 Analysis Capabilities:")
    for cap_id, cap_info in capabilities["capabilities"].items():
        print(f"  • {cap_id.title()}: {cap_info['description']}")
        print(f"    Models: {', '.join(cap_info['models'])}")
    
    # Display methodology
    print(f"\n🔍 Baker Street Methodology:")
    for step, description in capabilities["methodology"].items():
        print(f"  {step.title()}: {description}")
    
    # Display API status
    print(f"\n🔌 API Status:")
    for provider, status in capabilities["api_status"].items():
        status_emoji = "✅" if status == "configured" else "❌"
        print(f"  {status_emoji} {provider.title()}: {status}")
    
    print(f"\n🕵️‍♂️ The game is afoot! Baker Street Analyzer ready for advanced analysis!")
    
    return analyzer

if __name__ == "__main__":
    main()
