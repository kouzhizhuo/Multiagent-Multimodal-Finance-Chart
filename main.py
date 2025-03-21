import asyncio
import yfinance as yf
from PIL import Image
import io
import matplotlib.pyplot as plt
from agents.orchestrator_agent import OrchestratorAgent

async def main():
    # Initialize the orchestrator agent
    orchestrator = OrchestratorAgent()
    
    # Example: Analyze AAPL stock
    symbol = "AAPL"
    
    # Get historical price data
    stock = yf.Ticker(symbol)
    hist = stock.history(period="1y")
    
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
    
    # Get news articles (example)
    news = stock.news
    news_texts = [article['title'] + " " + article['summary'] for article in news[:5]]
    
    # Prepare input data
    input_data = {
        'chart_data': chart_image,
        'price_data': hist.to_dict('records'),
        'text_data': news_texts
    }
    
    # Run analysis
    result = await orchestrator.process(input_data)
    
    if result.success:
        print("\nAnalysis Results:")
        print("-----------------")
        
        # Print summary
        summary = result.data.get('summary', {})
        print("\nOverall Trend:", summary.get('overall_trend'))
        print("Confidence Score:", summary.get('confidence_score'))
        
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

if __name__ == "__main__":
    asyncio.run(main()) 