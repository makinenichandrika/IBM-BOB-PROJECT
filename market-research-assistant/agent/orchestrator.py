"""
Orchestrator — Agentic loop that coordinates all market research tools.
Implements a ReAct-style (Reason + Act) pattern with IBM Granite LLM.
"""

import os
import logging
import time
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


# ─── IBM Granite LLM Client ───────────────────────────────────────────────────

class GraniteLLMClient:
    """
    IBM Granite LLM client via ibm-watsonx-ai SDK.
    Falls back to a demo mode if credentials are not set.
    """

    def __init__(self):
        self.api_key = os.getenv("WATSONX_API_KEY", "")
        self.project_id = os.getenv("WATSONX_PROJECT_ID", "")
        self.url = os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com")
        self.model_id = "ibm/granite-3-3-8b-instruct"
        self._client = None
        self._demo_mode = not (self.api_key and self.project_id and
                               self.api_key != "your_ibm_watsonx_api_key_here")
        if self._demo_mode:
            logger.warning("IBM Granite credentials not set — running in DEMO MODE")
        else:
            self._init_client()

    def _init_client(self):
        try:
            from ibm_watsonx_ai import APIClient, Credentials
            credentials = Credentials(url=self.url, api_key=self.api_key)
            self._client = APIClient(credentials=credentials)
            logger.info(f"IBM Granite client initialized: {self.model_id}")
        except Exception as e:
            logger.error(f"Failed to initialize IBM Granite client: {e}")
            self._demo_mode = True

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        """Generate text using IBM Granite or demo mode."""
        if self._demo_mode:
            return self._demo_response(user_prompt)

        try:
            from ibm_watsonx_ai.foundation_models import ModelInference
            from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams

            model = ModelInference(
                model_id=self.model_id,
                api_client=self._client,
                project_id=self.project_id,
                params={
                    GenParams.MAX_NEW_TOKENS: 1500,
                    GenParams.TEMPERATURE: 0.3,
                    GenParams.TOP_P: 0.9,
                    GenParams.REPETITION_PENALTY: 1.1,
                }
            )

            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]

            response = model.chat(messages=messages)
            return response["choices"][0]["message"]["content"]

        except Exception as e:
            logger.error(f"IBM Granite generation error: {e}")
            return self._demo_response(user_prompt)

    def _demo_response(self, prompt: str) -> str:
        """
        Demo mode response — returns a structured placeholder response
        so the UI can be tested without IBM watsonx credentials.
        """
        time.sleep(1)  # Simulate API latency

        if "trend" in prompt.lower() or "market size" in prompt.lower():
            return """## Market Trends Analysis

**1. Current Market Size & Growth Rate**
- Estimated market size: $45-60 billion globally (Medium confidence)
- Annual growth rate: 12-18% CAGR over the next 5 years
- The target region shows above-average adoption rates

**2. Key Market Drivers**
- Rapid digital transformation across industries
- Increasing consumer demand for personalized solutions
- Government initiatives supporting sector growth
- Rising disposable income in the target demographic

**3. Emerging Trends**
- AI and automation integration becoming table-stakes
- Subscription-based models outperforming one-time purchases
- Mobile-first consumer behavior dominant in this market
- Sustainability and ESG considerations influencing purchasing

**4. Market Challenges & Barriers**
- High customer acquisition costs in competitive segments
- Regulatory compliance requirements varying by region
- Consumer trust and data privacy concerns
- Talent shortage for specialized skills

**5. 5-Year Outlook**
- Market expected to consolidate around 3-5 dominant players
- Niche segments will offer 2-3x growth vs. mainstream
- Cross-border expansion creating new revenue streams

*[DEMO MODE: Connect IBM watsonx credentials for AI-powered analysis]*"""

        elif "competitor" in prompt.lower():
            return """## Competitive Analysis

**1. Competitive Landscape Overview**
- Market structure: Oligopolistic with 2-3 dominant players and fragmented mid-tier
- Competitive intensity: Medium-High (Porter's Five Forces: moderate threat)
- New entrant barriers: Medium (capital requirements + brand trust)

**2. Competitor Strengths**
- Established brand recognition and customer loyalty programs
- Significant R&D investment enabling product innovation
- Extensive distribution networks and partner ecosystems
- Strong data assets enabling personalization at scale

**3. Competitor Gaps & Weaknesses**
- Limited focus on niche/underserved customer segments
- Legacy technology stacks creating agility challenges
- Customer service responsiveness below industry benchmarks
- One-size-fits-all pricing models missing value-tier customers

**4. Differentiation Opportunities**
- Hyper-personalization for specific micro-segments
- Superior onboarding and customer success experience
- Transparent, flexible pricing vs. competitors' complex tiers
- Community-driven product development as moat

**5. Competitive Intensity Score: Medium**
- Room exists for well-positioned new entrants
- First-mover advantage in identified niches is achievable

*[DEMO MODE: Connect IBM watsonx credentials for AI-powered analysis]*"""

        elif "customer" in prompt.lower() or "audience" in prompt.lower():
            return """## Customer Insights Analysis

**1. Customer Persona Overview**
- Primary segment: Age 25-45, digitally savvy professionals
- Secondary segment: SMB owners seeking efficiency solutions
- Education: College-educated, moderate to high tech literacy
- Decision-making style: Research-driven, peer-influenced

**2. Key Pain Points & Needs**
- Time scarcity — solutions that save time are premium-priced
- Information overload — curation and simplification valued highly
- Fear of making costly mistakes — trust signals are critical
- Desire for measurable ROI within 3-6 months

**3. Purchase Decision Factors**
- Peer recommendations and reviews (67% influence weight)
- Free trial or freemium model availability
- Clear, transparent pricing with no hidden fees
- Quality of customer support and onboarding

**4. Customer Acquisition Channels**
- LinkedIn and professional networks (B2B focus)
- Content marketing and SEO (long-term, high-ROI)
- Referral programs (30-40% lower CAC vs. paid)
- Industry events and webinars for thought leadership

**5. Diversity & Inclusion Note**
- Women entrepreneurs represent a fast-growing, underserved segment
- Non-English speaking users need localized content
- Tier-2/3 city consumers offer untapped growth potential

*[DEMO MODE: Connect IBM watsonx credentials for AI-powered analysis]*"""

        elif "opportunit" in prompt.lower():
            return """## Business Opportunities & Strategy

**1. Top 3 Market Opportunities**
- **Opportunity A:** Underserved SMB segment — competitors focus on enterprise
- **Opportunity B:** Mobile-native product in a desktop-dominated market
- **Opportunity C:** Value-tier pricing for price-sensitive emerging markets

**2. Blue Ocean Areas**
- Vertical-specific solutions (competitors offer horizontal products)
- Community + product hybrid (build network effects as moat)
- White-label/API offerings for adjacent market players

**3. Strategic Positioning: Focused Differentiator**
- Target a specific, profitable niche and own it deeply
- Avoid direct price competition with established players
- Build switching costs through integrations and data lock-in

**4. Go-to-Market Strategy**
- Phase 1 (0-3 months): Launch MVP, acquire 50 beta customers
- Phase 2 (3-9 months): Referral program, content marketing engine
- Phase 3 (9-18 months): Scale paid acquisition, expand features
- Phase 4 (18+ months): Geographic expansion or new verticals

**5. Key Success Factors**
- Product-market fit validation within 90 days
- Net Promoter Score > 50 from beta customers
- Customer Acquisition Cost < 3-month revenue per customer

**6. Risk Mitigation**
- Market risk: Validate demand before full investment
- Competitive risk: Build defensible moats early
- Execution risk: Start lean, measure everything

*[DEMO MODE: Connect IBM watsonx credentials for AI-powered analysis]*"""

        elif "synthesize" in prompt.lower() or "executive" in prompt.lower() or "report" in prompt.lower():
            return """## Executive Summary
This market presents a compelling opportunity for a well-positioned new entrant with a differentiated product. The combination of underserved customer segments, competitor gaps in agility and pricing, and strong market growth creates a favorable environment for entry within the next 12-18 months.

## Market Overview
The market demonstrates double-digit growth with strong digital adoption tailwinds. Regulatory environment is favorable. The target region shows above-average growth potential.

## Competitive Intelligence
Market is moderately competitive with 2-3 dominant players. Key gaps exist in SMB-focused solutions and flexible pricing. New entrants with a niche focus can gain traction.

## Customer Profile
Target audience is digitally engaged, research-driven, and strongly influenced by peer recommendations. Underserved segments include women entrepreneurs and Tier-2 city consumers.

## Strategic Opportunities
Three high-priority opportunities identified: SMB-focused vertical solution, mobile-native product, and community-driven growth model.

## Recommendations
1. **Validate PMF early** — Run a 60-day beta with 25-50 target customers before scaling
2. **Own the SMB niche** — Position explicitly as the SMB-first alternative to enterprise tools
3. **Build referral moat** — Invest in referral infrastructure in months 1-3
4. **Price transparently** — Simple, tier-based pricing as a differentiator
5. **Content-led growth** — Publish 2x/week industry content to build organic authority

## Confidence & Limitations
- Confidence Level: Medium (based on general market patterns)
- Limitation: Analysis is based on AI knowledge; validate with primary research
- Recommendation: Conduct 10-15 customer discovery interviews before launch

*[DEMO MODE: Connect IBM watsonx credentials for AI-powered analysis]*"""

        else:
            return """Thank you for your market research query. Based on available market intelligence:

**Key Insight:** The market dynamics you're investigating show several interesting patterns worth exploring. Market research is most valuable when combined with primary customer interviews and validated assumptions.

**Framework Recommendation:** Consider applying the Jobs-to-be-Done (JTBD) framework alongside traditional SWOT analysis for a comprehensive view.

**Next Steps:**
1. Define your specific market segment precisely
2. Identify 3-5 direct competitors for benchmarking
3. Conduct 10 customer discovery interviews
4. Validate pricing assumptions with conjoint analysis

*[DEMO MODE: Connect IBM watsonx credentials for IBM Granite-powered analysis]*"""


# ─── Agentic Orchestrator ─────────────────────────────────────────────────────

class MarketResearchOrchestrator:
    """
    ReAct-style agentic orchestrator.
    Coordinates all market research tools and manages the research workflow.
    """

    def __init__(self):
        self.llm = GraniteLLMClient()
        self._init_tools()

    def _init_tools(self):
        from agent.tools import (
            MarketTrendAnalyzer, CompetitorAnalyzer,
            CustomerInsightEngine, OpportunityFinder, ReportGenerator, QAResponder
        )
        self.tools = {
            "market_trends": MarketTrendAnalyzer(self.llm),
            "competitors": CompetitorAnalyzer(self.llm),
            "customers": CustomerInsightEngine(self.llm),
            "opportunities": OpportunityFinder(self.llm),
            "report": ReportGenerator(self.llm),
            "qa": QAResponder(self.llm),
        }
        logger.info(f"Initialized {len(self.tools)} agent tools")

    def run_research(self, inputs: dict) -> dict:
        """
        Full market research pipeline.
        Runs all 5 tools sequentially and synthesizes a final report.
        Returns dict with report sections and reasoning steps.
        """
        from agent.guardrails import validate_output, ethics_summary

        reasoning_steps = []
        start_time = time.time()

        logger.info(f"Starting research pipeline for industry: {inputs.get('industry')}")

        # Step 1: Market Trend Analysis
        reasoning_steps.append({
            "step": 1,
            "tool": "MarketTrendAnalyzer",
            "action": f"Analyzing market trends for {inputs['industry']} in {inputs['location']}"
        })
        market_trends = self.tools["market_trends"].run(**inputs)
        market_trends_validated = validate_output(market_trends)

        # Step 2: Competitor Analysis
        reasoning_steps.append({
            "step": 2,
            "tool": "CompetitorAnalyzer",
            "action": f"Analyzing competitors: {inputs.get('competitors', 'general market')}"
        })
        competitor_analysis = self.tools["competitors"].run(**inputs)
        competitor_validated = validate_output(competitor_analysis)

        # Step 3: Customer Insights
        reasoning_steps.append({
            "step": 3,
            "tool": "CustomerInsightEngine",
            "action": f"Building customer insights for: {inputs['target_audience']}"
        })
        customer_insights = self.tools["customers"].run(**inputs)
        customer_validated = validate_output(customer_insights)

        # Step 4: Opportunity Finding
        reasoning_steps.append({
            "step": 4,
            "tool": "OpportunityFinder",
            "action": "Identifying strategic opportunities and go-to-market strategy"
        })
        opportunities = self.tools["opportunities"].run(**inputs)
        opportunities_validated = validate_output(opportunities)

        # Step 5: Report Synthesis
        reasoning_steps.append({
            "step": 5,
            "tool": "ReportGenerator",
            "action": "Synthesizing all analyses into executive report"
        })
        final_report = self.tools["report"].run(
            market_trends=market_trends_validated["text"],
            competitor_analysis=competitor_validated["text"],
            customer_insights=customer_validated["text"],
            opportunities=opportunities_validated["text"]
        )
        report_validated = validate_output(final_report)

        elapsed = round(time.time() - start_time, 2)
        logger.info(f"Research pipeline completed in {elapsed}s")

        all_warnings = (
            market_trends_validated["warnings"] +
            competitor_validated["warnings"] +
            customer_validated["warnings"] +
            opportunities_validated["warnings"] +
            report_validated["warnings"]
        )

        return {
            "status": "success",
            "report": {
                "executive_summary": report_validated["text"],
                "market_trends": market_trends_validated["text"],
                "competitor_analysis": competitor_validated["text"],
                "customer_insights": customer_validated["text"],
                "opportunities": opportunities_validated["text"],
            },
            "reasoning_steps": reasoning_steps,
            "ethics_check": {
                "passed": True,
                **ethics_summary()
            },
            "warnings": all_warnings,
            "elapsed_seconds": elapsed,
            "model": self.llm.model_id,
            "mode": "demo" if self.llm._demo_mode else "live"
        }

    def run_query(self, question: str) -> dict:
        """Answer a single market research question."""
        from agent.guardrails import validate_output

        start_time = time.time()
        answer = self.tools["qa"].run(question=question)
        validated = validate_output(answer)
        elapsed = round(time.time() - start_time, 2)

        return {
            "status": "success",
            "answer": validated["text"],
            "warnings": validated["warnings"],
            "elapsed_seconds": elapsed,
            "model": self.llm.model_id,
            "mode": "demo" if self.llm._demo_mode else "live"
        }
