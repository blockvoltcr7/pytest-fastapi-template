from crewai import Agent, Crew, Task, Process
from crewai_tools import SerperDevTool, WebsiteSearchTool, ScrapeWebsiteTool
from app.tools.content_tools.trend_tools import ContentTrendTools
from typing import List, Dict, Optional
from datetime import datetime
import json
import os

class ContentCreationCrew:
    """Content Creation Crew for trend-based content optimization"""

    def __init__(self):
        # Check for required environment variables
        if not os.getenv("OPENAI_API_KEY"):
            print("Warning: OPENAI_API_KEY not found. CrewAI may require this for embeddings.")

        self.tools = ContentTrendTools()
        self._setup_agents()

    def _setup_agents(self):
        """Initialize all agents for the content creation workflow"""

        # Trend Researcher Agent
        self.trend_researcher = Agent(
            role="Trend Research Specialist",
            goal="Identify and analyze current trends in the industry to ensure content relevance",
            backstory="""You are an expert trend analyst with years of experience in
            identifying viral content patterns and emerging topics. You excel at spotting
            opportunities for content that can ride the wave of current trends.""",
            tools=[],  # Tools will be added when needed
            verbose=True,
            allow_delegation=False
        )

        # Competitor Analyst Agent
        self.competitor_analyst = Agent(
            role="Competitor Content Analyst",
            goal="Analyze competitor content strategies to identify gaps and opportunities",
            backstory="""You are a strategic content analyst who specializes in
            competitive intelligence. You can identify what works in competitor content
            and find unique angles that haven't been explored.""",
            tools=[],  # Tools will be added when needed
            verbose=True,
            allow_delegation=False
        )

        # Content Strategist Agent
        self.content_strategist = Agent(
            role="Content Strategy Expert",
            goal="Develop strategic content plans that combine trend insights with brand messaging",
            backstory="""You are a seasoned content strategist who excels at creating
            data-driven content strategies. You can seamlessly blend trending topics
            with brand values to create compelling content plans. You work with the insights
            provided by the trend researcher and competitor analyst to create comprehensive strategies.""",
            verbose=True,
            allow_delegation=False  # Changed to False to prevent delegation errors
        )

        # Content Creator Agent
        self.content_creator = Agent(
            role="Creative Content Writer",
            goal="Create engaging, trend-optimized content that resonates with the target audience",
            backstory="""You are a creative content writer with a knack for crafting
            viral-worthy content. You understand how to incorporate trends naturally
            while maintaining authenticity and brand voice.""",
            verbose=True,
            allow_delegation=False
        )

    def create_trend_research_task(self, content_idea: Dict) -> Task:
        """Create a task for trend research"""
        topic = content_idea.get('topic', 'general topic')
        return Task(
            description=f"""
            Research current trends related to: {topic}
            Industry: {content_idea.get('industry', 'general')}
            Target audience: {content_idea.get('target_audience', 'general')}

            Focus on:
            1. Identify top 5 trending topics or angles related to this content idea
            2. Find viral content examples in this space
            3. Analyze what makes these trends successful
            4. Identify trending hashtags and keywords
            5. Look for emerging conversations and pain points

            Use the available trend analysis tools to gather this information.
            If tools are not available, provide insights based on general knowledge and best practices.

            Provide a comprehensive trend analysis report.
            """,
            expected_output="""A detailed trend analysis report containing:
            - Top 5 trending angles with evidence
            - Viral content examples with engagement metrics
            - Key success factors analysis
            - List of 10+ trending hashtags and keywords
            - Emerging opportunities and content gaps""",
            agent=self.trend_researcher
        )

    def create_competitor_analysis_task(self, content_idea: Dict) -> Task:
        """Create a task for competitor analysis"""
        topic = content_idea.get('topic', 'general topic')
        competitors = content_idea.get('competitors', [])
        return Task(
            description=f"""
            Analyze competitor content strategies for: {topic}
            Competitors to analyze: {competitors if competitors else 'Find top 3 competitors in this space'}

            Research:
            1. What content angles are competitors using?
            2. Which content pieces are getting the most engagement?
            3. What gaps exist in their content coverage?
            4. What unique value propositions are they offering?
            5. How frequently are they publishing on this topic?

            If competitor URLs are provided, analyze their content strategy.
            If no specific competitors are provided, research general competitive landscape.

            Provide insights on how to differentiate our content.
            """,
            expected_output="""A competitor analysis report including:
            - Summary of each competitor's content strategy
            - High-performing content examples
            - Identified content gaps and opportunities
            - Differentiation strategies
            - Recommended unique angles""",
            agent=self.competitor_analyst
        )

    def create_strategy_task(self, content_idea: Dict) -> Task:
        """Create a task for content strategy development"""
        topic = content_idea.get('topic', 'general topic')
        return Task(
            description=f"""
            You will receive insights from trend research and competitor analysis to develop a strategic
            content plan for: {topic}

            Campaign duration: {content_idea.get('campaign_duration', '1 week')}
            Publishing date: {content_idea.get('publish_date', 'TBD')}
            Content type: {content_idea.get('content_type', 'blog post')}

            Use the provided context from previous tasks to create a strategy that:
            1. Leverages identified trends while maintaining brand authenticity
            2. Fills content gaps found in competitor analysis
            3. Provides unique value to the target audience
            4. Includes specific content angles and headlines
            5. Suggests optimal timing and distribution channels

            Work with the available information from the trend research and competitor analysis.
            Do not delegate - use the context provided to create your strategy.
            """,
            expected_output="""A comprehensive content strategy including:
            - 3-5 unique content angles with headlines
            - Content calendar with optimal publishing times
            - Distribution channel recommendations
            - Key messages and talking points
            - Expected outcomes and KPIs""",
            agent=self.content_strategist
        )

    def create_content_creation_task(self, content_idea: Dict) -> Task:
        """Create a task for final content creation"""
        topic = content_idea.get('topic', 'general topic')
        return Task(
            description=f"""
            Using all the insights from trend research, competitor analysis, and content strategy,
            create the final optimized content for: {topic}

            Content type: {content_idea.get('content_type', 'blog post')}
            Word count: {content_idea.get('word_count', '800-1000')}
            Target audience: {content_idea.get('target_audience', 'general')}

            Requirements:
            1. Incorporate trending elements naturally based on the trend research
            2. Address identified content gaps from competitor analysis
            3. Use trending keywords and hashtags appropriately
            4. Create an attention-grabbing headline
            5. Include a compelling hook that relates to current trends
            6. Maintain brand voice while being trendy
            7. Include clear CTAs
            8. Structure content for maximum engagement

            The content should feel fresh, relevant, and timely.
            Use the context from all previous tasks to inform your content creation.
            Do not delegate - create the content using all available insights.
            """,
            expected_output="""Final content deliverables:
            - Main headline (optimized for trends)
            - 3 alternative headlines
            - Full content piece with proper formatting
            - List of hashtags to use
            - Meta description
            - Key takeaways or summary points
            - Suggested visuals or media
            - Call-to-action recommendations""",
            agent=self.content_creator
        )

    def process_content_idea(self, content_idea: Dict) -> Dict:
        """Process a single content idea through the crew"""

        # Create tasks
        trend_task = self.create_trend_research_task(content_idea)
        competitor_task = self.create_competitor_analysis_task(content_idea)
        strategy_task = self.create_strategy_task(content_idea)
        content_task = self.create_content_creation_task(content_idea)

        # Set up task dependencies
        strategy_task.context = [trend_task, competitor_task]
        content_task.context = [trend_task, competitor_task, strategy_task]

        # Create and run crew
        crew = Crew(
            agents=[
                self.trend_researcher,
                self.competitor_analyst,
                self.content_strategist,
                self.content_creator
            ],
            tasks=[
                trend_task,
                competitor_task,
                strategy_task,
                content_task
            ],
            process=Process.sequential,
            verbose=True,
            memory=False  # Disable memory to avoid OpenAI embedding dependency
        )

        try:
            # Execute the crew
            result = crew.kickoff()

            return {
                'original_idea': content_idea,
                'optimized_content': str(result) if result else "Content creation completed successfully",
                'timestamp': datetime.now().isoformat(),
                'status': 'success'
            }
        except Exception as e:
            return {
                'original_idea': content_idea,
                'optimized_content': f"Error during content creation: {str(e)}",
                'timestamp': datetime.now().isoformat(),
                'status': 'error',
                'error': str(e)
            }
