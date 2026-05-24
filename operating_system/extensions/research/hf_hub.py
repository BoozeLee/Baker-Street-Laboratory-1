# BAKERSTREET-LABS-2025
"""
Baker Street Laboratory - Hugging Face Hub Research Module
Uses HF Hub API to search models, datasets, papers, and spaces for research.
"""

import os
import json
import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass, field

from huggingface_hub import HfApi, ModelInfo, DatasetInfo, SpaceInfo
from huggingface_hub.utils import HfHubHTTPError


@dataclass
class HFResearchResult:
    """Represents a research result from Hugging Face Hub"""
    type: str  # model, dataset, space, paper
    id: str
    name: str
    description: str
    url: str
    tags: List[str] = field(default_factory=list)
    downloads: int = 0
    likes: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)


class HFHubResearcher:
    """
    Research assistant using Hugging Face Hub.
    Searches for relevant models, datasets, papers, and spaces.
    """
    
    def __init__(self, token: str = None):
        self.api = HfApi(token=token or os.environ.get("HF_TOKEN"))
        self.token = token or os.environ.get("HF_TOKEN")
    
    def search_models(self, query: str, limit: int = 10, sort: str = "downloads") -> List[HFResearchResult]:
        """Search for relevant models on HF Hub"""
        try:
            models = self.api.list_models(
                search=query,
                sort=sort,
                direction=-1,
                limit=limit
            )
            
            results = []
            for model in models:
                results.append(HFResearchResult(
                    type="model",
                    id=model.id,
                    name=model.id.split("/")[-1],
                    description=model.description or model.card_data.get("model-index", "") if hasattr(model, 'card_data') and model.card_data else "",
                    url=f"https://huggingface.co/{model.id}",
                    tags=model.tags or [],
                    downloads=getattr(model, 'downloads', 0) or 0,
                    likes=getattr(model, 'likes', 0) or 0,
                    metadata={
                        "pipeline_tag": getattr(model, 'pipeline_tag', None),
                        "library": getattr(model, 'library_name', None),
                        "author": model.id.split("/")[0] if "/" in model.id else None
                    }
                ))
            return results
        except Exception as e:
            print(f"Error searching models: {e}")
            return []
    
    def search_datasets(self, query: str, limit: int = 10) -> List[HFResearchResult]:
        """Search for relevant datasets on HF Hub"""
        try:
            datasets = self.api.list_datasets(
                search=query,
                sort="downloads",
                direction=-1,
                limit=limit
            )
            
            results = []
            for dataset in datasets:
                results.append(HFResearchResult(
                    type="dataset",
                    id=dataset.id,
                    name=dataset.id.split("/")[-1],
                    description=dataset.description or "",
                    url=f"https://huggingface.co/datasets/{dataset.id}",
                    tags=dataset.tags or [],
                    downloads=getattr(dataset, 'downloads', 0) or 0,
                    likes=getattr(dataset, 'likes', 0) or 0,
                    metadata={
                        "size": getattr(dataset, 'dataset_info', {}).get('download_size', None),
                        "author": dataset.id.split("/")[0] if "/" in dataset.id else None
                    }
                ))
            return results
        except Exception as e:
            print(f"Error searching datasets: {e}")
            return []
    
    def search_spaces(self, query: str, limit: int = 10) -> List[HFResearchResult]:
        """Search for relevant Spaces on HF Hub"""
        try:
            spaces = self.api.list_spaces(
                search=query,
                sort="likes",
                direction=-1,
                limit=limit
            )
            
            results = []
            for space in spaces:
                results.append(HFResearchResult(
                    type="space",
                    id=space.id,
                    name=space.id.split("/")[-1],
                    description=space.description or "",
                    url=f"https://huggingface.co/spaces/{space.id}",
                    tags=space.tags or [],
                    likes=getattr(space, 'likes', 0) or 0,
                    metadata={
                        "sdk": getattr(space, 'sdk', None),
                        "author": space.id.split("/")[0] if "/" in space.id else None
                    }
                ))
            return results
        except Exception as e:
            print(f"Error searching spaces: {e}")
            return []
    
    def search_papers(self, query: str, limit: int = 10) -> List[HFResearchResult]:
        """Search for papers via HF Hub (models tagged with papers)"""
        try:
            models = self.api.list_models(
                search=query,
                filter="paper",
                sort="likes",
                direction=-1,
                limit=limit
            )
            
            results = []
            for model in models:
                results.append(HFResearchResult(
                    type="paper",
                    id=model.id,
                    name=model.id.split("/")[-1],
                    description=model.description or "",
                    url=f"https://huggingface.co/{model.id}",
                    tags=model.tags or [],
                    likes=getattr(model, 'likes', 0) or 0,
                    metadata={
                        "pipeline_tag": getattr(model, 'pipeline_tag', None),
                        "author": model.id.split("/")[0] if "/" in model.id else None
                    }
                ))
            return results
        except Exception as e:
            print(f"Error searching papers: {e}")
            return []
    
    def get_model_info(self, model_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a specific model"""
        try:
            model = self.api.model_info(model_id)
            return {
                "id": model.id,
                "name": model.id.split("/")[-1],
                "description": model.description or "",
                "url": f"https://huggingface.co/{model.id}",
                "tags": model.tags or [],
                "downloads": getattr(model, 'downloads', 0) or 0,
                "likes": getattr(model, 'likes', 0) or 0,
                "pipeline_tag": getattr(model, 'pipeline_tag', None),
                "config": getattr(model, 'config', {}),
                "siblings": [s.rfilename for s in model.siblings] if model.siblings else []
            }
        except Exception as e:
            print(f"Error getting model info: {e}")
            return None
    
    def comprehensive_research(self, query: str, limit: int = 5) -> Dict[str, Any]:
        """
        Conduct comprehensive research across HF Hub.
        Returns models, datasets, spaces, and papers related to the query.
        """
        results = {
            "query": query,
            "timestamp": datetime.now().isoformat(),
            "models": self.search_models(query, limit=limit),
            "datasets": self.search_datasets(query, limit=limit),
            "spaces": self.search_spaces(query, limit=limit),
            "papers": self.search_papers(query, limit=limit)
        }
        
        # Convert to serializable format
        serializable = {
            "query": results["query"],
            "timestamp": results["timestamp"],
            "total_results": len(results["models"]) + len(results["datasets"]) + len(results["spaces"]) + len(results["papers"]),
            "models": [self._result_to_dict(r) for r in results["models"]],
            "datasets": [self._result_to_dict(r) for r in results["datasets"]],
            "spaces": [self._result_to_dict(r) for r in results["spaces"]],
            "papers": [self._result_to_dict(r) for r in results["papers"]]
        }
        
        return serializable
    
    def _result_to_dict(self, result: HFResearchResult) -> Dict[str, Any]:
        """Convert HFResearchResult to dictionary"""
        return {
            "type": result.type,
            "id": result.id,
            "name": result.name,
            "description": result.description[:200] if result.description else "",
            "url": result.url,
            "tags": result.tags[:5],
            "downloads": result.downloads,
            "likes": result.likes,
            "metadata": result.metadata
        }


def research_hf_hub(query: str, token: str = None, limit: int = 5) -> Dict[str, Any]:
    """
    Main function for HF Hub research.
    Returns comprehensive research results.
    """
    researcher = HFHubResearcher(token=token)
    return researcher.comprehensive_research(query, limit=limit)
