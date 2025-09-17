"""
Example usage script for the AI Sentiment Analysis project
"""

import sys
import os
import pandas as pd

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.data_collection import DataCollector
from src.sentiment_analysis import SentimentAnalyzer
from src.metaphor_analysis import MetaphorDetector
from src.utils import setup_logging, create_sample_config


def run_example():
    """Run a simple example analysis"""
    
    print("AI Sentiment Analysis - Example Usage")
    print("=" * 50)
    
    # Setup logging
    setup_logging()
    
    # Sample AI-related texts for demonstration
    sample_texts = [
        "AI is revolutionary technology that will transform healthcare and education for the better",
        "I'm concerned that artificial intelligence might replace human workers and cause unemployment",
        "Machine learning algorithms are powerful tools for analyzing complex data patterns",
        "The AI overlords will control humanity unless we resist their technological dominance",
        "Humans and AI should collaborate as partners to solve global challenges together",
        "AI systems are evolving rapidly in this digital ecosystem of innovation",
        "We must defend against the AI invasion that threatens traditional industries",
        "Artificial intelligence is like a brilliant brain that can process information faster than humans",
        "AI tools help doctors diagnose diseases more accurately and efficiently",
        "The mysterious black box of AI decision-making raises concerns about transparency"
    ]
    
    print(f"Analyzing {len(sample_texts)} sample texts...\n")
    
    # Initialize analyzers
    sentiment_analyzer = SentimentAnalyzer(model_type="textblob")
    metaphor_detector = MetaphorDetector()
    
    # Perform sentiment analysis
    print("1. SENTIMENT ANALYSIS")
    print("-" * 30)
    
    sentiment_results = sentiment_analyzer.analyze_batch(sample_texts)
    sentiment_summary = sentiment_analyzer.get_sentiment_summary(sentiment_results)
    
    print("Individual text results:")
    for _, row in sentiment_results.iterrows():
        sentiment_cat = sentiment_analyzer.categorize_sentiment(row['compound'])
        print(f"Text {row['text_id']}: {sentiment_cat.upper()} ({row['compound']:.3f}) - {row['text']}")
    
    print(f"\nOverall Results:")
    print(f"Average sentiment: {sentiment_summary['average_compound']:.3f}")
    print("Distribution:")
    for sentiment, count in sentiment_summary['sentiment_distribution'].items():
        percentage = (count / len(sample_texts)) * 100
        print(f"  {sentiment.capitalize()}: {count} ({percentage:.1f}%)")
    
    # Perform metaphor analysis
    print("\n2. METAPHOR ANALYSIS")
    print("-" * 30)
    
    metaphor_results = metaphor_detector.analyze_batch(sample_texts)
    metaphor_summary = metaphor_detector.get_metaphor_summary(metaphor_results)
    
    print("Metaphor categories found:")
    for category, data in metaphor_summary['metaphor_category_counts'].items():
        if data['total_occurrences'] > 0:
            print(f"  {category.replace('_', ' ').title()}: {data['total_occurrences']} occurrences")
    
    print(f"\nTexts with metaphors: {metaphor_summary['texts_with_metaphors']}/{len(sample_texts)}")
    print(f"Average metaphor density: {metaphor_summary['average_metaphor_density']:.4f}")
    
    # Show examples for specific metaphor categories
    print("\n3. METAPHOR EXAMPLES")
    print("-" * 30)
    
    for category in ['human_like', 'tool_instrument', 'threat_war', 'partnership']:
        examples = metaphor_detector.extract_metaphor_examples(metaphor_results, category, limit=2)
        if examples:
            print(f"\n{category.replace('_', ' ').title()} metaphors:")
            for example in examples:
                print(f"  • {example}")
    
    # Data collection example (with sample data)
    print("\n4. DATA COLLECTION EXAMPLE")
    print("-" * 30)
    
    data_collector = DataCollector()
    
    # Demonstrate data collection (returns sample data)
    keywords = ['artificial intelligence', 'machine learning']
    social_data = data_collector.collect_social_media_data(keywords)
    news_data = data_collector.collect_news_data(keywords)
    
    print(f"Sample social media data: {len(social_data)} posts")
    print(f"Sample news data: {len(news_data)} articles")
    
    # Create sample survey data
    sample_survey = pd.DataFrame({
        'text': [
            "AI will help solve climate change through smart energy systems",
            "I worry about AI bias affecting hiring decisions",
            "Autonomous vehicles powered by AI will make roads safer"
        ],
        'source': ['survey'] * 3,
        'respondent_id': [1, 2, 3]
    })
    
    print(f"Sample survey data: {len(sample_survey)} responses")
    
    print("\n5. COMBINED ANALYSIS")
    print("-" * 30)
    
    # Combine all sample data
    all_sample_data = []
    if not social_data.empty:
        all_sample_data.append(social_data[['text']])
    if not news_data.empty:
        all_sample_data.append(news_data[['text']])
    all_sample_data.append(sample_survey[['text']])
    
    combined_sample = pd.concat(all_sample_data, ignore_index=True)
    
    # Analyze combined data
    combined_sentiment = sentiment_analyzer.analyze_batch(combined_sample['text'].tolist())
    combined_metaphors = metaphor_detector.analyze_batch(combined_sample['text'].tolist())
    
    print(f"Combined analysis of {len(combined_sample)} texts:")
    print(f"Average sentiment: {combined_sentiment['compound'].mean():.3f}")
    print(f"Texts with metaphors: {(combined_metaphors['total_metaphors'] > 0).sum()}")
    
    print("\nExample completed successfully!")
    print("\nTo run the full application with real data:")
    print("1. Install requirements: pip install -r requirements.txt")
    print("2. Configure API keys in config/config.json")
    print("3. Run: python main.py --keywords 'AI' 'machine learning'")


if __name__ == "__main__":
    run_example()