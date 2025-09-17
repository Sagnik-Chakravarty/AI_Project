#!/usr/bin/env python3
"""
AI Sentiment Analysis Main Application

This script demonstrates the complete workflow for analyzing public sentiment
on AI opinions and metaphor usage from online data sources and survey data.
"""

import argparse
import sys
import os
import pandas as pd
from datetime import datetime

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.data_collection import DataCollector
from src.sentiment_analysis import SentimentAnalyzer
from src.metaphor_analysis import MetaphorDetector
from src.utils import (
    setup_logging, load_config, save_results, create_sample_config,
    plot_sentiment_distribution, plot_metaphor_analysis, generate_report,
    validate_data, clean_text
)


def main():
    """Main application function"""
    parser = argparse.ArgumentParser(description='AI Sentiment and Metaphor Analysis')
    parser.add_argument('--config', default='config/config.json', 
                       help='Path to configuration file')
    parser.add_argument('--keywords', nargs='+', 
                       default=['artificial intelligence', 'AI', 'machine learning'],
                       help='Keywords to search for')
    parser.add_argument('--survey-data', help='Path to survey data file')
    parser.add_argument('--output-dir', default='results', 
                       help='Output directory for results')
    parser.add_argument('--sentiment-model', default='textblob',
                       choices=['textblob', 'vader', 'transformers'],
                       help='Sentiment analysis model to use')
    parser.add_argument('--days-back', type=int, default=7,
                       help='Days back to collect social media data')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Verbose logging')
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(level='DEBUG' if args.verbose else 'INFO')
    
    print("=" * 60)
    print("AI SENTIMENT AND METAPHOR ANALYSIS")
    print("=" * 60)
    print(f"Starting analysis at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Keywords: {', '.join(args.keywords)}")
    print(f"Sentiment Model: {args.sentiment_model}")
    print()
    
    # Load configuration
    config = load_config(args.config)
    if not config:
        print("No configuration found. Creating sample configuration...")
        create_sample_config()
        print("Please edit config/config.json with your API keys and run again.")
        return
    
    # Initialize components
    data_collector = DataCollector(args.config)
    sentiment_analyzer = SentimentAnalyzer(model_type=args.sentiment_model)
    metaphor_detector = MetaphorDetector()
    
    # Collect data
    print("1. COLLECTING DATA")
    print("-" * 30)
    
    all_data = []
    
    # Collect social media data
    print("Collecting social media data...")
    social_data = data_collector.collect_social_media_data(
        keywords=args.keywords,
        days_back=args.days_back
    )
    if not social_data.empty:
        social_data['source'] = 'social_media'
        all_data.append(social_data)
        print(f"Collected {len(social_data)} social media posts")
    
    # Collect news data
    print("Collecting news data...")
    news_data = data_collector.collect_news_data(keywords=args.keywords)
    if not news_data.empty:
        news_data['source'] = 'news'
        all_data.append(news_data)
        print(f"Collected {len(news_data)} news articles")
    
    # Load survey data if provided
    if args.survey_data:
        print(f"Loading survey data from {args.survey_data}...")
        try:
            survey_data = data_collector.load_survey_data(args.survey_data)
            if not survey_data.empty:
                survey_data['source'] = 'survey'
                all_data.append(survey_data)
                print(f"Loaded {len(survey_data)} survey responses")
        except Exception as e:
            print(f"Error loading survey data: {e}")
    
    # Combine all data
    if not all_data:
        print("No data collected. Please check your configuration and try again.")
        return
    
    combined_data = pd.concat(all_data, ignore_index=True)
    print(f"Total texts to analyze: {len(combined_data)}")
    print()
    
    # Clean text data
    print("Cleaning text data...")
    if 'text' in combined_data.columns:
        combined_data['text'] = combined_data['text'].apply(clean_text)
        combined_data = combined_data[combined_data['text'] != '']
        print(f"Texts after cleaning: {len(combined_data)}")
    
    # Analyze sentiment
    print("2. SENTIMENT ANALYSIS")
    print("-" * 30)
    
    texts = combined_data['text'].tolist()
    sentiment_results = sentiment_analyzer.analyze_batch(texts)
    sentiment_summary = sentiment_analyzer.get_sentiment_summary(sentiment_results)
    
    print(f"Analyzed sentiment for {len(sentiment_results)} texts")
    print(f"Average sentiment score: {sentiment_summary.get('average_compound', 0):.3f}")
    
    # Print sentiment distribution
    sentiment_dist = sentiment_summary.get('sentiment_distribution', {})
    for sentiment, count in sentiment_dist.items():
        percentage = (count / len(sentiment_results)) * 100
        print(f"  {sentiment.capitalize()}: {count} ({percentage:.1f}%)")
    print()
    
    # Analyze metaphors
    print("3. METAPHOR ANALYSIS")
    print("-" * 30)
    
    metaphor_results = metaphor_detector.analyze_batch(texts)
    metaphor_summary = metaphor_detector.get_metaphor_summary(metaphor_results)
    
    print(f"Analyzed metaphors for {len(metaphor_results)} texts")
    print(f"Texts with metaphors: {metaphor_summary.get('texts_with_metaphors', 0)}")
    print(f"Average metaphor density: {metaphor_summary.get('average_metaphor_density', 0):.4f}")
    
    # Print top metaphor categories
    top_categories = metaphor_summary.get('most_common_categories', [])[:5]
    print("Top metaphor categories:")
    for category, count in top_categories:
        print(f"  {category.replace('_', ' ').title()}: {count}")
    print()
    
    # Generate visualizations
    print("4. GENERATING VISUALIZATIONS")
    print("-" * 30)
    
    try:
        plot_sentiment_distribution(sentiment_results, 
                                  f"{args.output_dir}/sentiment_distribution.png")
        plot_metaphor_analysis(metaphor_results, 
                              f"{args.output_dir}/metaphor_analysis.png")
        print("Visualizations saved successfully")
    except Exception as e:
        print(f"Error generating visualizations: {e}")
    print()
    
    # Save results
    print("5. SAVING RESULTS")
    print("-" * 30)
    
    # Save detailed results
    sentiment_results.to_csv(f"{args.output_dir}/sentiment_analysis.csv", index=False)
    metaphor_results.to_csv(f"{args.output_dir}/metaphor_analysis.csv", index=False)
    combined_data.to_csv(f"{args.output_dir}/collected_data.csv", index=False)
    
    # Save summary results
    save_results(sentiment_summary, 'sentiment_summary.json', args.output_dir)
    save_results(metaphor_summary, 'metaphor_summary.json', args.output_dir)
    
    # Generate HTML report
    generate_report(sentiment_summary, metaphor_summary, 
                   f"{args.output_dir}/analysis_report.html")
    
    print(f"Results saved to {args.output_dir}/")
    print()
    
    # Final summary
    print("6. ANALYSIS COMPLETE")
    print("-" * 30)
    print("Summary of findings:")
    print(f"• Analyzed {len(combined_data)} texts from {len(set(combined_data['source']))} sources")
    print(f"• Overall sentiment: {sentiment_summary.get('average_compound', 0):.3f}")
    print(f"• Most common sentiment: {max(sentiment_dist.items(), key=lambda x: x[1])[0] if sentiment_dist else 'N/A'}")
    print(f"• Metaphor usage: {metaphor_summary.get('texts_with_metaphors', 0)} texts contain metaphors")
    
    if top_categories:
        print(f"• Most common metaphor: {top_categories[0][0].replace('_', ' ').title()}")
    
    print(f"\nDetailed results and visualizations saved to: {args.output_dir}/")
    print("Analysis completed successfully!")


if __name__ == "__main__":
    main()