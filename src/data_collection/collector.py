"""
Data Collection Module

This module handles collecting data from various online sources including
social media platforms, news sites, forums, and survey data.
"""

import os
import json
import pandas as pd
import requests
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataCollector:
    """Main class for collecting data from various sources"""
    
    def __init__(self, config_path: str = "config/api_keys.json"):
        """
        Initialize the data collector with API credentials
        
        Args:
            config_path: Path to configuration file with API keys
        """
        self.config = self._load_config(config_path)
        self.collected_data = []
    
    def _load_config(self, config_path: str) -> Dict:
        """Load API configuration from file"""
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return json.load(f)
        else:
            logger.warning(f"Config file {config_path} not found. Using empty config.")
            return {}
    
    def collect_social_media_data(self, 
                                 keywords: List[str], 
                                 platforms: List[str] = ['twitter', 'reddit'],
                                 days_back: int = 7) -> pd.DataFrame:
        """
        Collect data from social media platforms
        
        Args:
            keywords: List of keywords to search for
            platforms: List of platforms to collect from
            days_back: Number of days back to collect data
            
        Returns:
            DataFrame with collected social media data
        """
        data = []
        
        for platform in platforms:
            if platform == 'twitter':
                data.extend(self._collect_twitter_data(keywords, days_back))
            elif platform == 'reddit':
                data.extend(self._collect_reddit_data(keywords, days_back))
        
        return pd.DataFrame(data)
    
    def _collect_twitter_data(self, keywords: List[str], days_back: int) -> List[Dict]:
        """Collect data from Twitter (placeholder implementation)"""
        # This would implement actual Twitter API calls
        logger.info(f"Collecting Twitter data for keywords: {keywords}")
        
        # Placeholder data structure
        sample_data = []
        for keyword in keywords:
            sample_data.append({
                'platform': 'twitter',
                'keyword': keyword,
                'text': f"Sample tweet about {keyword} and AI technology",
                'timestamp': datetime.now(),
                'author': 'sample_user',
                'engagement': {'likes': 10, 'retweets': 5, 'replies': 2}
            })
        
        return sample_data
    
    def _collect_reddit_data(self, keywords: List[str], days_back: int) -> List[Dict]:
        """Collect data from Reddit (placeholder implementation)"""
        # This would implement actual Reddit API calls
        logger.info(f"Collecting Reddit data for keywords: {keywords}")
        
        # Placeholder data structure
        sample_data = []
        for keyword in keywords:
            sample_data.append({
                'platform': 'reddit',
                'keyword': keyword,
                'text': f"Reddit post discussing {keyword} and artificial intelligence",
                'timestamp': datetime.now(),
                'author': 'reddit_user',
                'engagement': {'upvotes': 25, 'comments': 8}
            })
        
        return sample_data
    
    def collect_news_data(self, keywords: List[str], sources: List[str] = None) -> pd.DataFrame:
        """
        Collect data from news sources
        
        Args:
            keywords: Keywords to search for
            sources: List of news sources to search
            
        Returns:
            DataFrame with news articles
        """
        logger.info(f"Collecting news data for keywords: {keywords}")
        
        # Placeholder implementation
        data = []
        for keyword in keywords:
            data.append({
                'source': 'news_site',
                'keyword': keyword,
                'title': f"News article about {keyword} in AI",
                'text': f"This is a news article discussing the implications of {keyword} in artificial intelligence...",
                'timestamp': datetime.now(),
                'url': f"https://example.com/article-{keyword}"
            })
        
        return pd.DataFrame(data)
    
    def load_survey_data(self, file_path: str) -> pd.DataFrame:
        """
        Load survey data from file
        
        Args:
            file_path: Path to survey data file (CSV, JSON, Excel)
            
        Returns:
            DataFrame with survey responses
        """
        logger.info(f"Loading survey data from {file_path}")
        
        if not os.path.exists(file_path):
            logger.error(f"Survey file {file_path} not found")
            return pd.DataFrame()
        
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if file_ext == '.csv':
            return pd.read_csv(file_path)
        elif file_ext == '.json':
            return pd.read_json(file_path)
        elif file_ext in ['.xlsx', '.xls']:
            return pd.read_excel(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_ext}")
    
    def save_data(self, data: pd.DataFrame, filename: str) -> None:
        """Save collected data to file"""
        if not os.path.exists('data'):
            os.makedirs('data')
        
        filepath = os.path.join('data', filename)
        data.to_csv(filepath, index=False)
        logger.info(f"Data saved to {filepath}")


if __name__ == "__main__":
    # Example usage
    collector = DataCollector()
    
    # Collect data with AI-related keywords
    ai_keywords = ['artificial intelligence', 'machine learning', 'AI ethics', 'AI metaphor']
    social_data = collector.collect_social_media_data(ai_keywords)
    news_data = collector.collect_news_data(ai_keywords)
    
    # Save collected data
    collector.save_data(social_data, 'social_media_data.csv')
    collector.save_data(news_data, 'news_data.csv')
    
    print(f"Collected {len(social_data)} social media posts and {len(news_data)} news articles")