# AI Sentiment Analysis Project

A comprehensive tool for analyzing public sentiment on artificial intelligence opinions and the use of metaphors in AI-related discourse from online data sources and survey data.

## 🎯 Project Overview

This project provides a complete pipeline for:
- **Data Collection**: Gathering AI-related content from social media, news sources, and surveys
- **Sentiment Analysis**: Analyzing public opinion and attitudes toward AI
- **Metaphor Detection**: Identifying and categorizing metaphorical language used to describe AI
- **Visualization & Reporting**: Creating insights through charts and comprehensive reports

## 🚀 Features

### Data Collection
- Social media data collection (Twitter, Reddit)
- News article gathering from various sources
- Survey data integration (CSV, JSON, Excel)
- Configurable keywords and time ranges

### Sentiment Analysis
- Multiple sentiment analysis models (TextBlob, VADER, Transformers)
- AI-specific sentiment adjustments
- Batch processing capabilities
- Detailed sentiment categorization

### Metaphor Analysis
- Detection of AI metaphor categories:
  - Human-like metaphors (AI "thinks", "learns")
  - Tool/instrument metaphors (AI as utility)
  - Partnership metaphors (human-AI collaboration)
  - Threat/war metaphors (AI as danger)
  - Biological metaphors (AI "evolution")
  - Master/slave metaphors (AI dominance)
  - Magic/supernatural metaphors (AI as mysterious)

### Visualization & Reporting
- Sentiment distribution charts
- Metaphor usage analysis
- Interactive HTML reports
- Export capabilities for further analysis

## 📦 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Sagnik-Chakravarty/AI_Project.git
   cd AI_Project
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Download NLTK data (if using VADER):**
   ```python
   import nltk
   nltk.download('vader_lexicon')
   ```

4. **Set up configuration:**
   ```bash
   python main.py  # This will create a sample config file
   # Edit config/config.json with your API keys
   ```

## 🏃 Quick Start

### Run Example Analysis
```bash
python example.py
```

### Basic Usage
```bash
python main.py --keywords "artificial intelligence" "machine learning" "AI ethics"
```

### Advanced Usage
```bash
python main.py \
  --keywords "AI" "artificial intelligence" "machine learning" \
  --sentiment-model transformers \
  --days-back 14 \
  --survey-data data/survey_responses.csv \
  --output-dir results/analysis_2024 \
  --verbose
```

## 📁 Project Structure

```
AI_Project/
├── src/
│   ├── data_collection/     # Data gathering modules
│   │   ├── __init__.py
│   │   └── collector.py
│   ├── sentiment_analysis/  # Sentiment analysis tools
│   │   ├── __init__.py
│   │   └── analyzer.py
│   ├── metaphor_analysis/   # Metaphor detection tools
│   │   ├── __init__.py
│   │   └── detector.py
│   └── utils/              # Utility functions
│       ├── __init__.py
│       └── helpers.py
├── config/                 # Configuration files
├── data/                   # Data storage
├── results/               # Analysis outputs
├── tests/                 # Test files
├── main.py               # Main application
├── example.py            # Example usage
├── requirements.txt      # Dependencies
└── README.md            # This file
```

## ⚙️ Configuration

Create `config/config.json` with your API credentials:

```json
{
  "api_keys": {
    "twitter_bearer_token": "your_token_here",
    "reddit_client_id": "your_client_id",
    "reddit_client_secret": "your_secret",
    "news_api_key": "your_news_api_key"
  },
  "data_collection": {
    "default_keywords": ["artificial intelligence", "AI", "machine learning"],
    "days_back": 7,
    "max_results": 1000
  },
  "analysis": {
    "sentiment_model": "textblob",
    "enable_metaphor_analysis": true
  }
}
```

## 📊 Usage Examples

### Analyze Social Media Sentiment
```python
from src.data_collection import DataCollector
from src.sentiment_analysis import SentimentAnalyzer

collector = DataCollector()
analyzer = SentimentAnalyzer()

# Collect data
data = collector.collect_social_media_data(['AI ethics', 'machine learning'])

# Analyze sentiment
results = analyzer.analyze_batch(data['text'].tolist())
summary = analyzer.get_sentiment_summary(results)

print(f"Average sentiment: {summary['average_compound']}")
```

### Detect AI Metaphors
```python
from src.metaphor_analysis import MetaphorDetector

detector = MetaphorDetector()

text = "AI is like a powerful brain that can learn and think faster than humans"
metaphors = detector.detect_metaphors(text)

print("Detected metaphors:", metaphors)
```

### Survey Data Integration
```python
# Load survey data
survey_data = collector.load_survey_data('data/ai_survey.csv')

# Analyze sentiment and metaphors
sentiment_results = analyzer.analyze_batch(survey_data['response'].tolist())
metaphor_results = detector.analyze_batch(survey_data['response'].tolist())
```

## 📈 Output Examples

### Sentiment Analysis Results
```
Sentiment Distribution:
  Positive: 45 (45.0%)
  Neutral: 35 (35.0%)
  Negative: 20 (20.0%)

Average Sentiment Score: 0.123
```

### Metaphor Analysis Results
```
Metaphor Categories:
  Human-like: 23 occurrences
  Tool/Instrument: 18 occurrences
  Partnership: 12 occurrences
  Threat/War: 8 occurrences
```

## 🔧 API Reference

### DataCollector
- `collect_social_media_data(keywords, platforms, days_back)`
- `collect_news_data(keywords, sources)`
- `load_survey_data(file_path)`

### SentimentAnalyzer
- `analyze_text(text)` - Analyze single text
- `analyze_batch(texts)` - Analyze multiple texts
- `get_sentiment_summary(results)` - Generate summary statistics

### MetaphorDetector
- `detect_metaphors(text)` - Detect metaphors in text
- `analyze_batch(texts)` - Analyze multiple texts
- `get_metaphor_summary(results)` - Generate summary statistics

## 🧪 Testing

```bash
# Run basic functionality test
python example.py

# Run with sample data
python main.py --keywords "test AI" --verbose
```

## 📝 Research Applications

This tool can be used for:
- **Academic Research**: Studying public perception of AI
- **Policy Analysis**: Understanding societal attitudes toward AI regulation
- **Communication Strategy**: Analyzing effective AI messaging
- **Trend Analysis**: Tracking changes in AI discourse over time
- **Cross-platform Comparison**: Comparing sentiment across different sources

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is available under the MIT License.

## 🙏 Acknowledgments

- Built for analyzing public sentiment and metaphor usage in AI discourse
- Supports multiple data sources and analysis methods
- Designed for researchers, policymakers, and communication professionals

## 📞 Support

For questions, issues, or contributions, please:
1. Check the documentation above
2. Review existing issues
3. Create a new issue with detailed information

---

**Happy Analyzing! 🤖📊**