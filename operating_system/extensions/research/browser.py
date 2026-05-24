# BAKERSTREET-LABS-2025
"""
Baker Street Laboratory - Human-Level Browser Automation
Uses Playwright for headless browsing with human-like behavior.
"""

import asyncio
import time
import random
import re
from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass, field

try:
    from playwright.async_api import async_playwright, Browser, BrowserContext, Page
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False


@dataclass
class WebPage:
    """Represents a scraped web page"""
    url: str
    title: str
    content: str
    text_content: str
    links: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


class HumanBehaviorSimulator:
    """Simulates human browsing behavior to avoid detection"""
    
    @staticmethod
    async def human_delay(min_ms: float = 500, max_ms: float = 2000):
        """Random delay mimicking human reading time"""
        delay = random.uniform(min_ms, max_ms) / 1000
        await asyncio.sleep(delay)
    
    @staticmethod
    async def human_scroll(page: Page, max_scrolls: int = 5):
        """Simulate human scrolling behavior"""
        for _ in range(random.randint(1, max_scrolls)):
            scroll_amount = random.randint(200, 800)
            await page.mouse.wheel(0, scroll_amount)
            await HumanBehaviorSimulator.human_delay(300, 1000)
    
    @staticmethod
    async def human_mouse_movement(page: Page):
        """Simulate natural mouse movements"""
        viewport = page.viewport_size
        if viewport:
            for _ in range(random.randint(2, 5)):
                x = random.randint(100, viewport.get('width', 1280) - 100)
                y = random.randint(100, viewport.get('height', 720) - 100)
                await page.mouse.move(x, y, steps=random.randint(10, 30))
                await HumanBehaviorSimulator.human_delay(100, 500)


class ResearchBrowser:
    """
    Headless browser for AI research with human-like behavior.
    Uses Playwright for robust web automation.
    """
    
    def __init__(self, headless: bool = True, user_agent: str = None):
        self.headless = headless
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self.visited_urls: List[str] = []
        self.research_data: List[WebPage] = []
        
        # Human-like user agent
        self.user_agent = user_agent or (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    
    async def start(self):
        """Initialize the browser"""
        if not PLAYWRIGHT_AVAILABLE:
            raise RuntimeError("Playwright not installed. Run: pip install playwright && playwright install chromium")
        
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(
            headless=self.headless,
            args=[
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-gpu',
                '--single-process'
            ]
        )
        
        self.context = await self.browser.new_context(
            user_agent=self.user_agent,
            viewport={'width': 1280, 'height': 720},
            locale='en-US',
            timezone_id='Europe/Brussels'
        )
        
        # Block unnecessary resources for faster loading
        await self.context.route("**/*.{png,jpg,jpeg,gif,svg,woff,woff2}", lambda route: route.abort())
        
        self.page = await self.context.new_page()
    
    async def stop(self):
        """Close the browser"""
        if self.browser:
            await self.browser.close()
    
    async def navigate(self, url: str, wait_until: str = 'networkidle') -> Optional[WebPage]:
        """Navigate to a URL with human-like behavior"""
        if not self.page:
            await self.start()
        
        try:
            # Human-like delay before navigation
            await HumanBehaviorSimulator.human_delay(1000, 3000)
            
            response = await self.page.goto(url, wait_until=wait_until, timeout=30000)
            
            if response and response.status != 200:
                return None
            
            # Human-like scrolling
            await HumanBehaviorSimulator.human_scroll(self.page)
            
            # Extract page content
            page_data = await self._extract_page_content(url)
            
            if page_data:
                self.visited_urls.append(url)
                self.research_data.append(page_data)
            
            return page_data
            
        except Exception as e:
            print(f"Navigation error for {url}: {e}")
            return None
    
    async def search_google(self, query: str, num_results: int = 5) -> List[Dict[str, str]]:
        """Perform a Google search and extract results"""
        search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}&num={num_results}"
        
        page = await self.navigate(search_url)
        if not page:
            return []
        
        # Extract search results
        results = await self.page.evaluate("""
            () => {
                const results = [];
                const links = document.querySelectorAll('a[href^="/url?q="]');
                links.forEach(link => {
                    const url = link.href.replace('/url?q=', '').split('&')[0];
                    const title = link.querySelector('h3')?.textContent || link.textContent;
                    if (url && title && !url.includes('google.com')) {
                        results.push({title: title.trim(), url: decodeURIComponent(url)});
                    }
                });
                return results.slice(0, 10);
            }
        """)
        
        return results[:num_results]
    
    async def search_duckduckgo(self, query: str, num_results: int = 5) -> List[Dict[str, str]]:
        """Perform a DuckDuckGo search (more scraping-friendly)"""
        search_url = f"https://html.duckduckgo.com/html/?q={query.replace(' ', '+')}"
        
        page = await self.navigate(search_url)
        if not page:
            return []
        
        results = await self.page.evaluate("""
            () => {
                const results = [];
                const links = document.querySelectorAll('.result__a');
                links.forEach(link => {
                    results.push({
                        title: link.textContent?.trim() || '',
                        url: link.href
                    });
                });
                return results.slice(0, 10);
            }
        """)
        
        return results[:num_results]
    
    async def deep_research(self, query: str, max_pages: int = 5, max_depth: int = 2) -> List[WebPage]:
        """
        Conduct deep research by following links from search results.
        Mimics a human researcher exploring multiple sources.
        """
        # Start with search
        search_results = await self.search_duckduckgo(query, num_results=max_pages)
        
        if not search_results:
            search_results = await self.search_google(query, num_results=max_pages)
        
        # Visit each result
        for result in search_results:
            if len(self.research_data) >= max_pages:
                break
            
            await self.navigate(result['url'])
            await HumanBehaviorSimulator.human_delay(2000, 5000)
        
        return self.research_data
    
    async def _extract_page_content(self, url: str) -> Optional[WebPage]:
        """Extract meaningful content from a page"""
        try:
            # Get title
            title = await self.page.title()
            
            # Get text content (cleaned)
            text_content = await self.page.evaluate("""
                () => {
                    // Remove scripts, styles, nav, footer
                    const elements = document.querySelectorAll('script, style, nav, footer, header, aside, iframe');
                    elements.forEach(el => el.remove());
                    return document.body?.innerText || '';
                }
            """)
            
            # Get all links
            links = await self.page.evaluate("""
                () => {
                    const links = [];
                    document.querySelectorAll('a[href^="http"]').forEach(a => {
                        links.push(a.href);
                    });
                    return links.slice(0, 50);
                }
            """)
            
            # Clean text content
            cleaned_text = re.sub(r'\n\s*\n', '\n\n', text_content.strip())
            cleaned_text = cleaned_text[:10000]  # Limit content size
            
            return WebPage(
                url=url,
                title=title,
                content=text_content,
                text_content=cleaned_text,
                links=links,
                metadata={
                    'url': url,
                    'content_length': len(cleaned_text),
                    'link_count': len(links)
                }
            )
            
        except Exception as e:
            print(f"Error extracting content from {url}: {e}")
            return None
    
    async def take_screenshot(self, url: str, path: str = None) -> Optional[str]:
        """Take a screenshot of a page"""
        await self.navigate(url)
        if not path:
            path = f"screenshot_{int(time.time())}.png"
        await self.page.screenshot(path=path, full_page=True)
        return path


async def research_query(query: str, max_pages: int = 3) -> Dict[str, Any]:
    """
    Main research function - conducts web research on a query.
    Returns structured research findings.
    """
    browser = ResearchBrowser(headless=True)
    
    try:
        await browser.start()
        
        # Search and collect
        pages = await browser.deep_research(query, max_pages=max_pages)
        
        # Compile research summary
        research_summary = {
            'query': query,
            'timestamp': datetime.now().isoformat(),
            'pages_visited': len(pages),
            'sources': [],
            'key_findings': []
        }
        
        for page in pages:
            research_summary['sources'].append({
                'title': page.title,
                'url': page.url,
                'content_preview': page.text_content[:500] + '...' if len(page.text_content) > 500 else page.text_content
            })
        
        return research_summary
        
    finally:
        await browser.stop()
