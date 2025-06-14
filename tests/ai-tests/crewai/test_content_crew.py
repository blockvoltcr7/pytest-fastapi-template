import pytest
import asyncio
from unittest.mock import patch, MagicMock
from app.agents.content_crew.content_creation_crew import ContentCreationCrew
from app.tools.content_tools.trend_tools import ContentTrendTools
from app.api.v1.schemas.content.content_schemas import (
    ContentIdea,
    ContentCreationRequest,
    QuickTrendRequest
)

class TestContentTrendTools:
    """Test suite for ContentTrendTools"""

    def test_initialization(self):
        """Test ContentTrendTools initialization"""
        tools = ContentTrendTools()
        assert tools is not None
        # Tools might be None if API keys are not available, which is expected

    def test_search_trending_topics(self):
        """Test trending topics search"""
        tools = ContentTrendTools()
        result = tools.search_trending_topics("marketing", ["AI", "automation"])

        assert result is not None
        assert isinstance(result, str)
        assert len(result) > 0
        assert "marketing" in result.lower() or "ai" in result.lower()

    def test_analyze_competitor_content(self):
        """Test competitor content analysis"""
        tools = ContentTrendTools()
        competitors = ["example.com", "test.com"]
        result = tools.analyze_competitor_content(competitors)

        assert result is not None
        assert isinstance(result, str)
        assert len(result) > 0

    def test_search_social_trends(self):
        """Test social media trends search"""
        tools = ContentTrendTools()
        result = tools.search_social_trends("AI marketing")

        assert result is not None
        assert isinstance(result, str)
        assert len(result) > 0
        assert "AI marketing" in result or "marketing" in result.lower()

class TestContentCreationCrew:
    """Test suite for ContentCreationCrew"""

    def test_initialization(self):
        """Test ContentCreationCrew initialization"""
        crew = ContentCreationCrew()
        assert crew is not None
        assert crew.trend_researcher is not None
        assert crew.competitor_analyst is not None
        assert crew.content_strategist is not None
        assert crew.content_creator is not None
        assert crew.tools is not None

    def test_create_trend_research_task(self):
        """Test trend research task creation"""
        crew = ContentCreationCrew()
        content_idea = {
            "topic": "AI Marketing Tools",
            "industry": "marketing",
            "target_audience": "marketers"
        }

        task = crew.create_trend_research_task(content_idea)
        assert task is not None
        assert "AI Marketing Tools" in task.description
        assert task.agent == crew.trend_researcher

    def test_create_competitor_analysis_task(self):
        """Test competitor analysis task creation"""
        crew = ContentCreationCrew()
        content_idea = {
            "topic": "Content Strategy",
            "competitors": ["competitor1.com", "competitor2.com"]
        }

        task = crew.create_competitor_analysis_task(content_idea)
        assert task is not None
        assert "Content Strategy" in task.description
        assert task.agent == crew.competitor_analyst

    def test_create_strategy_task(self):
        """Test content strategy task creation"""
        crew = ContentCreationCrew()
        content_idea = {
            "topic": "Digital Marketing",
            "content_type": "blog post",
            "campaign_duration": "2 weeks"
        }

        task = crew.create_strategy_task(content_idea)
        assert task is not None
        assert "Digital Marketing" in task.description
        assert task.agent == crew.content_strategist

    def test_create_content_creation_task(self):
        """Test content creation task creation"""
        crew = ContentCreationCrew()
        content_idea = {
            "topic": "SEO Best Practices",
            "content_type": "article",
            "word_count": "1500"
        }

        task = crew.create_content_creation_task(content_idea)
        assert task is not None
        assert "SEO Best Practices" in task.description
        assert task.agent == crew.content_creator

    def test_process_content_idea_basic(self):
        """Test basic content idea processing"""
        crew = ContentCreationCrew()
        content_idea = {
            "topic": "Test Topic",
            "content_type": "blog post",
            "industry": "technology"
        }

        # This test might take a while due to actual crew processing
        result = crew.process_content_idea(content_idea)

        assert result is not None
        assert isinstance(result, dict)
        assert "original_idea" in result
        assert "optimized_content" in result
        assert "timestamp" in result
        assert "status" in result
        assert result["original_idea"]["topic"] == "Test Topic"

    def test_process_content_idea_with_error_handling(self):
        """Test content idea processing with error handling"""
        crew = ContentCreationCrew()

        # Test with invalid/minimal content idea
        content_idea = {"topic": ""}  # Empty topic should be handled gracefully

        result = crew.process_content_idea(content_idea)

        assert result is not None
        assert isinstance(result, dict)
        assert "status" in result
        # Should either succeed or fail gracefully

class TestContentCrewAPI:
    """Test suite for Content Crew API endpoints"""

    @pytest.fixture
    def sample_content_idea(self):
        """Fixture for sample content idea"""
        return ContentIdea(
            topic="AI-Powered Marketing Automation",
            content_type="blog post",
            industry="marketing",
            target_audience="marketing managers",
            competitors=["hubspot.com", "marketo.com"],
            keywords=["AI marketing", "automation", "personalization"]
        )

    @pytest.fixture
    def sample_content_request(self, sample_content_idea):
        """Fixture for sample content creation request"""
        return ContentCreationRequest(
            content_ideas=[sample_content_idea],
            google_sheet_row={"row_id": 1, "source": "test"}
        )

    def test_content_idea_schema(self, sample_content_idea):
        """Test ContentIdea schema validation"""
        assert sample_content_idea.topic == "AI-Powered Marketing Automation"
        assert sample_content_idea.content_type == "blog post"
        assert sample_content_idea.industry == "marketing"
        assert len(sample_content_idea.competitors) == 2
        assert len(sample_content_idea.keywords) == 3

    def test_content_request_schema(self, sample_content_request):
        """Test ContentCreationRequest schema validation"""
        assert len(sample_content_request.content_ideas) == 1
        assert sample_content_request.google_sheet_row["row_id"] == 1

    def test_quick_trend_request_schema(self):
        """Test QuickTrendRequest schema validation"""
        request = QuickTrendRequest(
            topic="sustainable fashion",
            industry="fashion"
        )
        assert request.topic == "sustainable fashion"
        assert request.industry == "fashion"

class TestContentCrewIntegration:
    """Integration tests for the complete content crew workflow"""

    def test_end_to_end_content_creation(self):
        """Test complete end-to-end content creation workflow"""
        # Create content idea
        content_idea = {
            "topic": "Future of Remote Work",
            "content_type": "blog post",
            "industry": "technology",
            "target_audience": "remote workers",
            "keywords": ["remote work", "future", "productivity"]
        }

        # Initialize crew and process
        crew = ContentCreationCrew()
        result = crew.process_content_idea(content_idea)

        # Validate result structure
        assert isinstance(result, dict)
        assert "original_idea" in result
        assert "optimized_content" in result
        assert "timestamp" in result
        assert "status" in result

        # Validate content
        assert result["original_idea"]["topic"] == "Future of Remote Work"
        assert len(result["optimized_content"]) > 0

    def test_multiple_content_ideas_processing(self):
        """Test processing multiple content ideas"""
        content_ideas = [
            {
                "topic": "AI in Healthcare",
                "industry": "healthcare",
                "content_type": "article"
            },
            {
                "topic": "Blockchain Technology",
                "industry": "technology",
                "content_type": "blog post"
            }
        ]

        crew = ContentCreationCrew()
        results = []

        for idea in content_ideas:
            result = crew.process_content_idea(idea)
            results.append(result)

        assert len(results) == 2
        assert all("status" in result for result in results)
        assert all("optimized_content" in result for result in results)

    def test_content_creation_with_competitors(self):
        """Test content creation with competitor analysis"""
        content_idea = {
            "topic": "Digital Marketing Trends 2024",
            "industry": "marketing",
            "competitors": ["hubspot.com", "contentmarketinginstitute.com"],
            "target_audience": "digital marketers"
        }

        crew = ContentCreationCrew()
        result = crew.process_content_idea(content_idea)

        assert result is not None
        assert "optimized_content" in result
        # Content should incorporate competitor insights
        assert len(result["optimized_content"]) > 100  # Ensure substantial content

    def test_trend_tools_integration(self):
        """Test integration with trend analysis tools"""
        tools = ContentTrendTools()

        # Test trend search
        trends = tools.search_trending_topics("technology", ["AI", "machine learning"])
        assert isinstance(trends, str)
        assert len(trends) > 0

        # Test social trends
        social_trends = tools.search_social_trends("artificial intelligence")
        assert isinstance(social_trends, str)
        assert len(social_trends) > 0

        # Test competitor analysis
        competitor_analysis = tools.analyze_competitor_content(["example.com"])
        assert isinstance(competitor_analysis, str)
        assert len(competitor_analysis) > 0

class TestErrorHandling:
    """Test error handling in content crew functionality"""

    def test_empty_content_idea(self):
        """Test handling of empty content ideas"""
        crew = ContentCreationCrew()
        result = crew.process_content_idea({})

        assert result is not None
        assert isinstance(result, dict)
        assert "status" in result

    def test_invalid_content_type(self):
        """Test handling of invalid content types"""
        crew = ContentCreationCrew()
        content_idea = {
            "topic": "Test Topic",
            "content_type": "invalid_type",
            "industry": "test"
        }

        result = crew.process_content_idea(content_idea)
        assert result is not None
        assert isinstance(result, dict)

    def test_missing_required_fields(self):
        """Test handling of missing required fields"""
        crew = ContentCreationCrew()

        # Missing topic
        content_idea = {
            "content_type": "blog post",
            "industry": "technology"
        }

        result = crew.process_content_idea(content_idea)
        assert result is not None
        # Should handle gracefully or include error information

    def test_network_error_simulation(self):
        """Test handling of network-related errors"""
        tools = ContentTrendTools()

        # These should not raise exceptions even if network calls fail
        result1 = tools.search_trending_topics("test", ["keyword"])
        result2 = tools.search_social_trends("test topic")
        result3 = tools.analyze_competitor_content(["invalid-url"])

        assert isinstance(result1, str)
        assert isinstance(result2, str)
        assert isinstance(result3, str)

@pytest.mark.asyncio
class TestAsyncOperations:
    """Test asynchronous operations for content crew"""

    async def test_concurrent_content_processing(self):
        """Test concurrent processing of multiple content ideas"""
        content_ideas = [
            {"topic": f"Topic {i}", "industry": "technology"}
            for i in range(3)
        ]

        crew = ContentCreationCrew()

        # Process ideas concurrently (simulated)
        tasks = []
        for idea in content_ideas:
            # In a real async scenario, this would be awaitable
            result = crew.process_content_idea(idea)
            tasks.append(result)

        assert len(tasks) == 3
        assert all(isinstance(task, dict) for task in tasks)

    async def test_background_task_simulation(self):
        """Test background task processing simulation"""
        content_idea = {
            "topic": "Background Processing Test",
            "content_type": "article",
            "industry": "technology"
        }

        crew = ContentCreationCrew()

        # Simulate background processing
        result = await asyncio.create_task(
            self._simulate_background_processing(crew, content_idea)
        )

        assert result is not None
        assert "status" in result

    async def _simulate_background_processing(self, crew, content_idea):
        """Helper method to simulate background processing"""
        # In real implementation, this would be truly async
        return crew.process_content_idea(content_idea)

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
