# Sample Survey Data for AI Sentiment Analysis

This directory contains sample survey data files that can be used to test the AI sentiment analysis functionality.

## Sample Data Files

### survey_responses.csv
A CSV file containing sample survey responses about AI opinions and experiences.

### Format
- `response_id`: Unique identifier for each response
- `text`: The survey response text
- `timestamp`: When the response was submitted
- `demographics`: Basic demographic information (optional)

## Usage

To analyze survey data:

```bash
python main.py --survey-data data/survey_responses.csv --keywords "AI" "artificial intelligence"
```

Or programmatically:

```python
from src.data_collection import DataCollector

collector = DataCollector()
survey_data = collector.load_survey_data('data/survey_responses.csv')
```