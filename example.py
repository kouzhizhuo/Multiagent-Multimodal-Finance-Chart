import asyncio
import yfinance as yf
from PIL import Image
import io
import matplotlib.pyplot as plt
from agents.orchestrator_agent import OrchestratorAgent
import pandas as pd

async def analyze_stock(symbol: str, period: str = "1y"):
    """
    Analyze a stock using the multi-agent framework
    
    Args:
        symbol (str): Stock symbol (e.g., "AAPL" for Apple)
        period (str): Time period for analysis (e.g., "1y", "6mo", "1mo")
    """
    # Initialize the orchestrator agent
    orchestrator = OrchestratorAgent()
    
    # Get historical price data
    stock = yf.Ticker(symbol)
    hist = stock.history(period=period)
    
    # Create a price chart
    plt.figure(figsize=(12, 6))
    plt.plot(hist.index, hist['Close'])
    plt.title(f"{symbol} Stock Price")
    plt.xlabel("Date")
    plt.ylabel("Price")
    
    # Convert plot to image
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    chart_image = Image.open(buf)
    
    # Get news articles
    news = stock.news
    news_texts = []
    for article in news[:5]:
        if isinstance(article, dict):
            title = article.get('title', '')
            summary = article.get('summary', '')
            news_texts.append(f"{title} {summary}")
    
    # Prepare input data
    input_data = {
        'chart_data': chart_image,
        'price_data': hist.to_dict('records'),
        'text_data': news_texts if news_texts else [f"Analysis for {symbol} stock"]
    }
    
    # Run analysis
    result = await orchestrator.process(input_data)
    
    if result.success:
        print(f"\nAnalysis Results for {symbol}:")
        print("-----------------")
        
        # Print summary
        summary = result.data.get('summary', {})
        print("\nOverall Trend:", summary.get('overall_trend'))
        print("Confidence Score:", summary.get('confidence_score'))
        
        # Print technical analysis
        technical = result.data.get('technical_analysis', {})
        print("\nTechnical Indicators:")
        for indicator, value in technical.get('indicators', {}).items():
            if isinstance(value, (pd.Series, pd.DataFrame)):
                print(f"- {indicator}: {value.iloc[-1]:.2f}")
            else:
                print(f"- {indicator}: {value}")
        
        # Print sentiment analysis
        sentiment = result.data.get('sentiment_analysis', {})
        print("\nMarket Sentiment:")
        print(f"Overall Sentiment: {sentiment.get('overall_sentiment', {})}")
        print(f"Market Impact: {sentiment.get('market_impact', {}).get('impact_level')}")
        
        # Print recommendations
        recommendations = result.data.get('recommendations', [])
        print("\nRecommendations:")
        for rec in recommendations:
            print(f"- {rec}")
        
        # Print risk assessment
        risk_assessment = result.data.get('risk_assessment', {})
        print("\nRisk Assessment:")
        print(f"Overall Risk Level: {risk_assessment.get('overall_risk_level')}")
        
    else:
        print("Error:", result.error)

async def main():
    # Example: Analyze multiple stocks
    stocks = ["AAPL", "GOOGL", "MSFT"]
    for symbol in stocks:
        print(f"\nAnalyzing {symbol}...")
        await analyze_stock(symbol)

if __name__ == "__main__":
    asyncio.run(main()) 