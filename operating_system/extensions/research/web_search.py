# BAKERSTREET-LABS-2025
"""
Baker Street Laboratory - Web Search & Content Extraction
Uses DuckDuckGo, BeautifulSoup, and trafilatura for web research.
"""

import re
import json
import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass, field
from urllib.parse import quote, urlparse

import requests
from bs4 import BeautifulSoup


@dataclass
class SearchResult:
    """Represents a search result"""
    title: str
    url: str
    snippet: str
    source: str


@dataclass
class ExtractedContent:
    """Represents extracted web content"""
    url: str
    title: str
    text: str
    summary: str
    metadata: Dict[str, Any] = field(default_factory=dict)


class DuckDuckGoSearcher:
    """Search using DuckDuckGo (no API key required)"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        })
    
    def search(self, query: str, max_results: int = 10) -> List[SearchResult]:
        """Search DuckDuckGo HTML"""
        try:
            url = f"https://html.duckduckgo.com/html/?q={quote(query)}"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            results = []
            
            for result in soup.select('.result'):
                title_elem = result.select_one('.result__a')
                snippet_elem = result.select_one('.result__snippet')
                
                if title_elem and snippet_elem:
                    title = title_elem.get_text(strip=True)
                    url = title_elem.get('href', '')
                    snippet = snippet_elem.get_text(strip=True)
                    
                    if url:
                        results.append(SearchResult(
                            title=title,
                            url=url,
                            snippet=snippet,
                            source="DuckDuckGo"
                        ))
                
                if len(results) >= max_results:
                    break
            
            return results
        except Exception as e:
            print(f"DuckDuckGo search error: {e}")
            return []


class ContentExtractor:
    """Extract meaningful content from web pages"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        })
    
    def extract(self, url: str) -> Optional[ExtractedContent]:
        """Extract content from a URL using multiple methods"""
        try:
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Get title
            title = soup.title.string if soup.title else ""
            
            # Remove unwanted elements
            for element in soup(['script', 'style', 'nav', 'footer', 'header', 'aside', 'iframe', 'noscript']):
                element.decompose()
            
            # Get main content
            main_content = soup.find('main') or soup.find('article') or soup.find('body')
            if main_content:
                text = main_content.get_text(separator='\n', strip=True)
            else:
                text = soup.get_text(separator='\n', strip=True)
            
            # Clean text
            text = self._clean_text(text)
            
            # Generate summary
            summary = self._generate_summary(text)
            
            return ExtractedContent(
                url=url,
                title=title,
                text=text[:5000],
                summary=summary,
                metadata={
                    "content_length": len(text),
                    "domain": urlparse(url).netloc
                }
            )
        except Exception as e:
            print(f"Content extraction error for {url}: {e}")
            return None
    
    def _clean_text(self, text: str) -> str:
        """Clean extracted text"""
        # Remove multiple newlines
        text = re.sub(r'\n\s*\n', '\n\n', text)
        # Remove URLs
        text = re.sub(r'http\S+', '', text)
        # Remove extra whitespace
        text = re.sub(r' +', ' ', text)
        return text.strip()
    
    def _generate_summary(self, text: str, max_sentences: int = 5) -> str:
        """Generate a simple extractive summary"""
        sentences = re.split(r'(?<=[.!?]) +', text.replace('\n', ' '))
        return ' '.join(sentences[:max_sentences])


class WebResearcher:
    """
    Complete web research tool combining search and content extraction.
    """
    
    def __init__(self):
        self.searcher = DuckDuckGoSearcher()
        self.extractor = ContentExtractor()
    
    def research(self, query: str, max_sources: int = 5, extract_content: bool = True) -> Dict[str, Any]:
        """
        Conduct web research on a query.
        Returns search results and optionally extracted content.
        """
        # Search
        search_results = self.searcher.search(query, max_results=max_sources)
        
        results = {
            "query": query,
            "timestamp": datetime.now().isoformat(),
            "search_results": [
                {
                    "title": r.title,
                    "url": r.url,
                    "snippet": r.snippet,
                    "source": r.source
                }
                for r in search_results
            ],
            "extracted_content": []
        }
        
        # Extract content from top results
        if extract_content:
            for result in search_results[:3]:
                content = self.extractor.extract(result.url)
                if content:
                    results["extracted_content"].append({
                        "url": content.url,
                        "title": content.title,
                        "summary": content.summary,
                        "text_preview": content.text[:500] + "..." if len(content.text) > 500 else content.text
                    })
        
        return results
    
    def compare_sources(self, query: str, urls: List[str]) -> Dict[str, Any]:
        """Compare content from multiple sources"""
        comparison = {
            "query": query,
            "sources": []
        }
        
        for url in urls:
            content = self.extractor.extract(url)
            if content:
                comparison["sources"].append({
                    "url": url,
                    "title": content.title,
                    "summary": content.summary,
                    "domain": content.metadata.get("domain", "")
                })
        
        return comparison


def web_research(query: str, max_sources: int = 5) -> Dict[str, Any]:
    """Main function for web research"""
    researcher = WebResearcher()
    return researcher.research(query, max_sources=max_sources)
