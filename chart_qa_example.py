import asyncio
from PIL import Image
import matplotlib.pyplot as plt
import yfinance as yf
import io
from agents.chart_qa_agent import ChartQAAgent

async def analyze_chart_and_qa(symbol: str, period: str = "1y"):
    """
    Analyze a financial chart and answer questions about it
    
    Args:
        symbol (str): Stock symbol (e.g., "AAPL" for Apple)
        period (str): Time period for analysis (e.g., "1y", "6mo", "1mo")
    """
    # Initialize the Chart QA Agent
    chart_qa_agent = ChartQAAgent()
    
    # Get historical price data
    stock = yf.Ticker(symbol)
    hist = stock.history(period=period)
    
    # Create a price chart
    plt.figure(figsize=(12, 6))
    plt.plot(hist.index, hist['Close'])
    plt.title(f"{symbol} Stock Price")
    plt.xlabel("Date")
    plt.ylabel("Price")
    
    # Convert plot to PIL Image
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    chart_image = Image.open(buf)
    
    # Close the plot to free memory
    plt.close()
    
    # Questions to ask about the chart
    questions = [
        "What is the overall trend of this stock price?",
        "What is the highest price point shown in the chart?",
        "Are there any significant price movements or patterns?",
        "What is the current price compared to the start of the period?",
        "Can you identify any support or resistance levels?"
    ]
    
    print(f"\nAnalyzing {symbol} chart and answering questions...")
    print("----------------------------------------")
    
    # Process each question
    for question in questions:
        print(f"\nQuestion: {question}")
        
        # Prepare input data
        input_data = {
            'chart_image': chart_image,
            'question': question
        }
        
        # Get answer
        result = await chart_qa_agent.process(input_data)
        
        if result.success:
            print(f"Answer: {result.data['answer']}")
            print(f"Confidence: {result.data['confidence']:.2f}")
            print("\nChart Description:", result.data['chart_description'])
        else:
            print(f"Error: {result.error}")

async def main():
    # Example: Analyze a single stock with detailed analysis
    symbol = "AAPL"
    print(f"\nStarting detailed analysis for {symbol}...")
    await analyze_chart_and_qa(symbol)

if __name__ == "__main__":
    asyncio.run(main()) 