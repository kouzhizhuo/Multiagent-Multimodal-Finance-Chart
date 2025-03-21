# Multiagent-Multimodal-Finance-Chart
# Financial Chart Analysis Framework

A powerful multi-agent framework for analyzing financial charts using advanced AI techniques. This framework combines computer vision, natural language processing, and financial analysis to provide intelligent insights about financial charts.

## Features

- **Chart Analysis**: Advanced chart pattern recognition and analysis
- **Question Answering**: Natural language Q&A about chart features and patterns
- **Multi-modal Processing**: Combines visual and numerical data analysis
- **Extensible Architecture**: Easy to add new analysis capabilities
- **Real-time Data**: Integration with yfinance for real-time stock data

## Project Structure

```
financial_chart_agents/
├── agents/
│   ├── __init__.py
│   ├── base_agent.py
│   └── chart_qa_agent.py
├── utils/
│   └── __init__.py
├── config/
│   └── __init__.py
├── tests/
│   └── __init__.py
├── requirements.txt
├── chart_qa_example.py
└── README.md
```

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd financial_chart_agents
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Dependencies

- numpy>=1.21.0
- pandas>=1.3.0
- matplotlib>=3.4.0
- seaborn>=0.11.0
- opencv-python>=4.5.0
- torch>=1.9.0
- transformers>=4.11.0
- pillow>=8.3.0
- python-dotenv>=0.19.0
- langchain>=0.0.150
- openai>=0.27.0
- pydantic>=1.8.0
- fastapi>=0.68.0
- uvicorn>=0.15.0
- python-multipart>=0.0.5
- ta>=0.10.0
- yfinance>=0.1.63

## Usage

### Basic Example

```python
from agents.chart_qa_agent import ChartQAAgent
import asyncio

async def analyze_chart(image_path, question):
    agent = ChartQAAgent()
    result = await agent.process({
        'chart_image': image_path,
        'question': question
    })
    return result

# Run analysis
asyncio.run(analyze_chart('path_to_chart.png', 'What is the trend?'))
```

### Running the Example Script

```bash
python chart_qa_example.py
```

This will:
1. Download real-time stock data for AAPL
2. Generate a price chart
3. Analyze the chart using the ChartQAAgent
4. Answer predefined questions about the chart

## Features in Detail

### ChartQAAgent

The main agent responsible for chart analysis and question answering:

- **Chart Processing**:
  - Image preprocessing
  - Chart element detection
  - Pattern recognition
  - Numerical data extraction

- **Analysis Capabilities**:
  - Trend analysis
  - Support/resistance level detection
  - Pattern identification
  - Price movement analysis
  - Technical indicator calculation

- **Question Answering**:
  - Natural language understanding
  - Context-aware responses
  - Confidence scoring
  - Detailed explanations

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Future Enhancements

- [ ] Implement advanced pattern recognition
- [ ] Add more technical indicators
- [ ] Enhance natural language understanding
- [ ] Add support for more chart types
- [ ] Improve confidence scoring
- [ ] Add batch processing capabilities

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- YFinance for real-time stock data
- Hugging Face Transformers for NLP capabilities
- OpenCV for image processing
- Matplotlib for chart generation

## Contact

For questions and support, please open an issue in the repository.
