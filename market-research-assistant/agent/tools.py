"""
Tools module — Individual agent skills/tools for market research analysis.
Each tool calls IBM Granite with a specific, structured prompt.
"""

import logging
from agent.prompts import (
    MARKET_TREND_PROMPT,
    COMPETITOR_ANALYSIS_PROMPT,
    CUSTOMER_INSIGHT_PROMPT,
    OPPORTUNITY_PROMPT,
    REPORT_SYNTHESIS_PROMPT,
    QA_PROMPT,
    SYSTEM_PROMPT,
)

logger = logging.getLogger(__name__)


class AgentTool:
    """Base class for agent tools."""

    def __init__(self, name: str, description: str, llm_client):
        self.name = name
        self.description = description
        self.llm = llm_client

    def run(self, **kwargs) -> str:
        raise NotImplementedError


class MarketTrendAnalyzer(AgentTool):
    """Analyzes market size, growth, drivers, and trends."""

    def __init__(self, llm_client):
        super().__init__(
            name="MarketTrendAnalyzer",
            description="Analyzes current market trends, size, growth, and 5-year outlook",
            llm_client=llm_client,
        )

    def run(self, industry: str, product: str, location: str, **kwargs) -> str:
        logger.info(f"[Tool: MarketTrendAnalyzer] industry={industry}, location={location}")
        prompt = MARKET_TREND_PROMPT.format(
            industry=industry, product=product, location=location
        )
        return self.llm.generate(SYSTEM_PROMPT, prompt)


class CompetitorAnalyzer(AgentTool):
    """Balanced competitor analysis using Porter's Five Forces."""

    def __init__(self, llm_client):
        super().__init__(
            name="CompetitorAnalyzer",
            description="Conducts balanced competitor analysis and identifies differentiation gaps",
            llm_client=llm_client,
        )

    def run(self, industry: str, product: str, competitors: str, location: str, **kwargs) -> str:
        logger.info(f"[Tool: CompetitorAnalyzer] competitors={competitors}")
        prompt = COMPETITOR_ANALYSIS_PROMPT.format(
            industry=industry, product=product,
            competitors=competitors or "Not specified",
            location=location
        )
        return self.llm.generate(SYSTEM_PROMPT, prompt)


class CustomerInsightEngine(AgentTool):
    """Builds customer personas and identifies pain points."""

    def __init__(self, llm_client):
        super().__init__(
            name="CustomerInsightEngine",
            description="Analyzes customer preferences, personas, pain points, and acquisition channels",
            llm_client=llm_client,
        )

    def run(self, industry: str, product: str, target_audience: str, location: str, **kwargs) -> str:
        logger.info(f"[Tool: CustomerInsightEngine] audience={target_audience}")
        prompt = CUSTOMER_INSIGHT_PROMPT.format(
            industry=industry, product=product,
            target_audience=target_audience, location=location
        )
        return self.llm.generate(SYSTEM_PROMPT, prompt)


class OpportunityFinder(AgentTool):
    """Identifies business opportunities and strategic recommendations."""

    def __init__(self, llm_client):
        super().__init__(
            name="OpportunityFinder",
            description="Identifies blue ocean opportunities, go-to-market strategies, and risk mitigation",
            llm_client=llm_client,
        )

    def run(self, industry: str, product: str, target_audience: str,
            location: str, competitors: str, **kwargs) -> str:
        logger.info("[Tool: OpportunityFinder]")
        prompt = OPPORTUNITY_PROMPT.format(
            industry=industry, product=product,
            target_audience=target_audience, location=location,
            competitors=competitors or "Not specified"
        )
        return self.llm.generate(SYSTEM_PROMPT, prompt)


class ReportGenerator(AgentTool):
    """Synthesizes all analyses into a final executive report."""

    def __init__(self, llm_client):
        super().__init__(
            name="ReportGenerator",
            description="Synthesizes all analyses into a structured executive market research report",
            llm_client=llm_client,
        )

    def run(self, market_trends: str, competitor_analysis: str,
            customer_insights: str, opportunities: str, **kwargs) -> str:
        logger.info("[Tool: ReportGenerator] Synthesizing final report")
        prompt = REPORT_SYNTHESIS_PROMPT.format(
            market_trends=market_trends,
            competitor_analysis=competitor_analysis,
            customer_insights=customer_insights,
            opportunities=opportunities
        )
        return self.llm.generate(SYSTEM_PROMPT, prompt)


class QAResponder(AgentTool):
    """Answers individual market research questions."""

    def __init__(self, llm_client):
        super().__init__(
            name="QAResponder",
            description="Answers specific market research questions",
            llm_client=llm_client,
        )

    def run(self, question: str, **kwargs) -> str:
        logger.info(f"[Tool: QAResponder] question={question[:60]}...")
        prompt = QA_PROMPT.format(question=question)
        return self.llm.generate(SYSTEM_PROMPT, prompt)
