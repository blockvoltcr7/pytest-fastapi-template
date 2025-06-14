from crewai_tools import SerperDevTool, WebsiteSearchTool, ScrapeWebsiteTool
from typing import List, Dict
import os

class ContentTrendTools:
    """Tools for content trend analysis and competitor monitoring"""

    def __init__(self):
        # Initialize tools - these will work even without API keys for basic functionality
        try:
            self.search_tool = SerperDevTool()
        except:
            self.search_tool = None

        try:
            self.website_search_tool = WebsiteSearchTool()
        except:
            self.website_search_tool = None

        try:
            self.scrape_tool = ScrapeWebsiteTool()
        except:
            self.scrape_tool = None

    def search_trending_topics(self, industry: str, keywords: List[str]) -> str:
        """Search for trending topics in a specific industry"""
        query = f"trending {industry} topics 2024 {' '.join(keywords)}"

        if self.search_tool:
            try:
                return self.search_tool.run(query)
            except Exception as e:
                return f"Mock trend data for {industry}: Current trending topics include AI automation, sustainability practices, and digital transformation. Keywords: {', '.join(keywords)}"
        else:
            return f"Mock trend data for {industry}: Current trending topics include AI automation, sustainability practices, and digital transformation. Keywords: {', '.join(keywords)}"

    def analyze_competitor_content(self, competitor_urls: List[str]) -> str:
        """Analyze competitor content strategies"""
        results = []
        for url in competitor_urls:
            try:
                if self.scrape_tool:
                    content = self.scrape_tool.run(url)
                    results.append({
                        'url': url,
                        'content': content[:500]  # First 500 chars
                    })
                else:
                    results.append({
                        'url': url,
                        'content': f"Mock analysis for {url}: Strong content strategy focusing on educational content, regular posting schedule, high engagement rates."
                    })
            except Exception as e:
                results.append({
                    'url': url,
                    'error': f"Mock error analysis for {url}: {str(e)}"
                })
        return str(results)

    def search_social_trends(self, topic: str) -> str:
        """Search for social media trends related to a topic"""
        query = f"{topic} trending on social media viral content"

        if self.search_tool:
            try:
                return self.search_tool.run(query)
            except Exception as e:
                return f"Mock social trends for {topic}: High engagement on video content, trending hashtags include #{topic.replace(' ', '')}, peak posting times are 9-11 AM and 7-9 PM"
        else:
            return f"Mock social trends for {topic}: High engagement on video content, trending hashtags include #{topic.replace(' ', '')}, peak posting times are 9-11 AM and 7-9 PM"
