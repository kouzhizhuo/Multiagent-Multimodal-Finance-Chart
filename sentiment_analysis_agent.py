from typing import Dict, Any, List
from transformers import pipeline
from .base_agent import BaseAgent, AgentResponse

class SentimentAnalysisAgent(BaseAgent):
    """Agent responsible for analyzing market sentiment from text data"""
    
    def __init__(self):
        super().__init__(
            name="SentimentAnalysisAgent",
            description="Analyzes market sentiment from news and social media"
        )
        # Initialize sentiment analysis pipeline
        self.sentiment_analyzer = pipeline(
            "sentiment-analysis",
            model="ProsusAI/finbert"  # Financial sentiment analysis model
        )
        
    async def process(self, input_data: Dict[str, Any]) -> AgentResponse:
        try:
            # Extract text data
            text_data = input_data.get('text_data')
            if not text_data:
                return AgentResponse(
                    success=False,
                    data={},
                    error="No text data provided"
                )
            
            # Perform sentiment analysis
            analysis_results = await self._analyze_sentiment(text_data)
            
            return AgentResponse(
                success=True,
                data=analysis_results
            )
            
        except Exception as e:
            return AgentResponse(
                success=False,
                data={},
                error=str(e)
            )
    
    async def _analyze_sentiment(self, text_data: Any) -> Dict[str, Any]:
        """Analyze sentiment from text data"""
        results = {
            'overall_sentiment': self._get_overall_sentiment(text_data),
            'sentiment_breakdown': self._get_sentiment_breakdown(text_data),
            'key_topics': self._extract_key_topics(text_data),
            'market_impact': self._assess_market_impact(text_data)
        }
        return results
    
    def _get_overall_sentiment(self, text_data: Any) -> Dict[str, Any]:
        """Calculate overall sentiment score"""
        if isinstance(text_data, str):
            texts = [text_data]
        elif isinstance(text_data, list):
            texts = text_data
        else:
            raise ValueError("Text data must be string or list of strings")
        
        # Analyze sentiment for each text
        sentiments = self.sentiment_analyzer(texts)
        
        # Calculate average sentiment
        sentiment_scores = {
            'positive': 0,
            'negative': 0,
            'neutral': 0
        }
        
        for sentiment in sentiments:
            label = sentiment['label'].lower()
            score = sentiment['score']
            sentiment_scores[label] += score
        
        # Normalize scores
        total = len(sentiments)
        for key in sentiment_scores:
            sentiment_scores[key] /= total
        
        return sentiment_scores
    
    def _get_sentiment_breakdown(self, text_data: Any) -> List[Dict[str, Any]]:
        """Get detailed sentiment breakdown for each text"""
        if isinstance(text_data, str):
            texts = [text_data]
        elif isinstance(text_data, list):
            texts = text_data
        else:
            raise ValueError("Text data must be string or list of strings")
        
        return self.sentiment_analyzer(texts)
    
    def _extract_key_topics(self, text_data: Any) -> List[Dict[str, Any]]:
        """Extract key topics from the text"""
        # TODO: Implement topic extraction
        return []
    
    def _assess_market_impact(self, text_data: Any) -> Dict[str, Any]:
        """Assess potential market impact of the sentiment"""
        sentiment_scores = self._get_overall_sentiment(text_data)
        
        # Calculate market impact score (-1 to 1)
        impact_score = (
            sentiment_scores['positive'] -
            sentiment_scores['negative']
        )
        
        # Determine impact level
        if impact_score > 0.5:
            impact_level = "strongly_positive"
        elif impact_score > 0.2:
            impact_level = "moderately_positive"
        elif impact_score > -0.2:
            impact_level = "neutral"
        elif impact_score > -0.5:
            impact_level = "moderately_negative"
        else:
            impact_level = "strongly_negative"
        
        return {
            'impact_score': impact_score,
            'impact_level': impact_level,
            'confidence': max(sentiment_scores.values())
        } 