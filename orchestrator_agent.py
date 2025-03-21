from typing import Dict, Any, List
from .base_agent import BaseAgent, AgentResponse
from .chart_analysis_agent import ChartAnalysisAgent
from .technical_analysis_agent import TechnicalAnalysisAgent
from .sentiment_analysis_agent import SentimentAnalysisAgent
from .report_generation_agent import ReportGenerationAgent

class OrchestratorAgent(BaseAgent):
    """Agent responsible for orchestrating the analysis workflow"""
    
    def __init__(self):
        super().__init__(
            name="OrchestratorAgent",
            description="Coordinates the analysis workflow between all agents"
        )
        # Initialize all agents
        self.chart_agent = ChartAnalysisAgent()
        self.technical_agent = TechnicalAnalysisAgent()
        self.sentiment_agent = SentimentAnalysisAgent()
        self.report_agent = ReportGenerationAgent()
        
    async def process(self, input_data: Dict[str, Any]) -> AgentResponse:
        try:
            # Extract input data
            chart_data = input_data.get('chart_data')
            price_data = input_data.get('price_data')
            text_data = input_data.get('text_data')
            
            if not all([chart_data, price_data, text_data]):
                return AgentResponse(
                    success=False,
                    data={},
                    error="Missing required input data"
                )
            
            # Run parallel analysis
            analysis_results = await self._run_parallel_analysis(
                chart_data,
                price_data,
                text_data
            )
            
            # Generate final report
            final_report = await self._generate_final_report(analysis_results)
            
            return AgentResponse(
                success=True,
                data=final_report
            )
            
        except Exception as e:
            return AgentResponse(
                success=False,
                data={},
                error=str(e)
            )
    
    async def _run_parallel_analysis(
        self,
        chart_data: Any,
        price_data: Any,
        text_data: Any
    ) -> Dict[str, Any]:
        """Run analysis in parallel using all agents"""
        # Run chart analysis
        chart_response = await self.chart_agent.process({
            'image': chart_data
        })
        
        # Run technical analysis
        technical_response = await self.technical_agent.process({
            'price_data': price_data
        })
        
        # Run sentiment analysis
        sentiment_response = await self.sentiment_agent.process({
            'text_data': text_data
        })
        
        # Combine results
        return {
            'chart_analysis': chart_response.data if chart_response.success else {},
            'technical_analysis': technical_response.data if technical_response.success else {},
            'sentiment_analysis': sentiment_response.data if sentiment_response.success else {}
        }
    
    async def _generate_final_report(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate final report using the report generation agent"""
        report_response = await self.report_agent.process(analysis_results)
        
        if not report_response.success:
            return {
                'error': report_response.error,
                'partial_results': analysis_results
            }
        
        return report_response.data
    
    def _validate_input_data(
        self,
        chart_data: Any,
        price_data: Any,
        text_data: Any
    ) -> bool:
        """Validate input data before processing"""
        # TODO: Implement input validation
        return True
    
    def _handle_agent_error(
        self,
        agent_name: str,
        error: str
    ) -> Dict[str, Any]:
        """Handle errors from individual agents"""
        return {
            'agent': agent_name,
            'error': error,
            'status': 'failed'
        }
    
    def _update_agent_contexts(self, analysis_results: Dict[str, Any]) -> None:
        """Update context for all agents based on analysis results"""
        # Update chart agent context
        self.chart_agent.update_context({
            'technical_indicators': analysis_results.get('technical_analysis', {}).get('indicators', {}),
            'sentiment_context': analysis_results.get('sentiment_analysis', {}).get('overall_sentiment', {})
        })
        
        # Update technical agent context
        self.technical_agent.update_context({
            'chart_patterns': analysis_results.get('chart_analysis', {}).get('patterns', []),
            'sentiment_context': analysis_results.get('sentiment_analysis', {}).get('overall_sentiment', {})
        })
        
        # Update sentiment agent context
        self.sentiment_agent.update_context({
            'technical_context': analysis_results.get('technical_analysis', {}).get('summary', {}),
            'chart_context': analysis_results.get('chart_analysis', {}).get('patterns', [])
        })
        
        # Update report agent context
        self.report_agent.update_context(analysis_results) 