"""
Basic tests for the AI Sentiment Analysis project
"""

import unittest
import sys
import os
import pandas as pd

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.data_collection import DataCollector
from src.sentiment_analysis import SentimentAnalyzer
from src.metaphor_analysis import MetaphorDetector


class TestAISentimentAnalysis(unittest.TestCase):
    """Test cases for the AI sentiment analysis components"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.sample_texts = [
            "AI is revolutionary and will benefit humanity",
            "I'm worried about AI replacing human jobs",
            "Machine learning algorithms process data efficiently",
            "AI overlords will control humanity"
        ]
        
        self.data_collector = DataCollector()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.metaphor_detector = MetaphorDetector()
    
    def test_data_collector_initialization(self):
        """Test data collector initialization"""
        self.assertIsInstance(self.data_collector, DataCollector)
        self.assertIsInstance(self.data_collector.collected_data, list)
    
    def test_social_media_data_collection(self):
        """Test social media data collection"""
        keywords = ['AI', 'artificial intelligence']
        data = self.data_collector.collect_social_media_data(keywords)
        
        self.assertIsInstance(data, pd.DataFrame)
        self.assertGreater(len(data), 0)
        self.assertIn('text', data.columns)
        self.assertIn('platform', data.columns)
    
    def test_news_data_collection(self):
        """Test news data collection"""
        keywords = ['AI', 'machine learning']
        data = self.data_collector.collect_news_data(keywords)
        
        self.assertIsInstance(data, pd.DataFrame)
        self.assertGreater(len(data), 0)
        self.assertIn('text', data.columns)
    
    def test_sentiment_analysis_single_text(self):
        """Test sentiment analysis for single text"""
        text = "AI is amazing and will help humanity"
        result = self.sentiment_analyzer.analyze_text(text)
        
        self.assertIsInstance(result, dict)
        self.assertIn('compound', result)
        self.assertIn('positive', result)
        self.assertIn('negative', result)
        self.assertIn('neutral', result)
        
        # Check score ranges
        self.assertGreaterEqual(result['compound'], -1)
        self.assertLessEqual(result['compound'], 1)
    
    def test_sentiment_analysis_batch(self):
        """Test sentiment analysis for multiple texts"""
        results = self.sentiment_analyzer.analyze_batch(self.sample_texts)
        
        self.assertIsInstance(results, pd.DataFrame)
        self.assertEqual(len(results), len(self.sample_texts))
        self.assertIn('compound', results.columns)
        self.assertIn('text_id', results.columns)
    
    def test_sentiment_categorization(self):
        """Test sentiment categorization"""
        self.assertEqual(self.sentiment_analyzer.categorize_sentiment(0.3), 'positive')
        self.assertEqual(self.sentiment_analyzer.categorize_sentiment(-0.3), 'negative')
        self.assertEqual(self.sentiment_analyzer.categorize_sentiment(0.01), 'neutral')
    
    def test_metaphor_detection(self):
        """Test metaphor detection"""
        text = "AI is like a brain that thinks and learns like humans"
        result = self.metaphor_detector.detect_metaphors(text)
        
        self.assertIsInstance(result, dict)
        self.assertIn('human_like', result)
        self.assertGreater(result['human_like']['count'], 0)
    
    def test_metaphor_batch_analysis(self):
        """Test metaphor analysis for multiple texts"""
        results = self.metaphor_detector.analyze_batch(self.sample_texts)
        
        self.assertIsInstance(results, pd.DataFrame)
        self.assertEqual(len(results), len(self.sample_texts))
        self.assertIn('total_metaphors', results.columns)
        self.assertIn('metaphor_density', results.columns)
    
    def test_metaphor_categories(self):
        """Test different metaphor categories"""
        test_cases = [
            ("AI thinks and learns", 'human_like'),
            ("AI is a powerful tool", 'tool_instrument'),
            ("AI overlords will control us", 'master_slave'),
            ("humans and AI partnership", 'partnership'),
            ("AI evolution in ecosystem", 'biological'),
            ("war against AI threat", 'threat_war'),
            ("AI magic and mysterious powers", 'magic_supernatural')
        ]
        
        for text, expected_category in test_cases:
            result = self.metaphor_detector.detect_metaphors(text)
            self.assertGreater(result[expected_category]['count'], 0, 
                             f"Failed to detect {expected_category} in '{text}'")
    
    def test_empty_text_handling(self):
        """Test handling of empty or invalid text inputs"""
        # Test empty string
        sentiment_result = self.sentiment_analyzer.analyze_text("")
        self.assertEqual(sentiment_result['compound'], 0.0)
        
        metaphor_result = self.metaphor_detector.detect_metaphors("")
        self.assertEqual(metaphor_result['human_like']['count'], 0)
        
        # Test None input
        sentiment_result = self.sentiment_analyzer.analyze_text(None)
        self.assertEqual(sentiment_result['compound'], 0.0)
        
        metaphor_result = self.metaphor_detector.detect_metaphors(None)
        self.assertEqual(metaphor_result['human_like']['count'], 0)
    
    def test_ai_specific_sentiment_adjustment(self):
        """Test AI-specific sentiment adjustments"""
        positive_text = "AI is innovative and beneficial for progress"
        negative_text = "AI is dangerous and threatening to jobs"
        
        positive_result = self.sentiment_analyzer.analyze_ai_specific_sentiment(positive_text)
        negative_result = self.sentiment_analyzer.analyze_ai_specific_sentiment(negative_text)
        
        self.assertIn('ai_positive_keywords', positive_result)
        self.assertIn('ai_negative_keywords', negative_result)
        self.assertGreater(positive_result['ai_positive_keywords'], 0)
        self.assertGreater(negative_result['ai_negative_keywords'], 0)


class TestUtilityFunctions(unittest.TestCase):
    """Test utility functions"""
    
    def test_text_cleaning(self):
        """Test text cleaning functionality"""
        from src.utils import clean_text
        
        # Test normal text
        clean = clean_text("  This is  a   test   ")
        self.assertEqual(clean, "This is a test")
        
        # Test short text
        clean = clean_text("Hi")
        self.assertEqual(clean, "")
        
        # Test non-string input
        clean = clean_text(None)
        self.assertEqual(clean, "")
    
    def test_data_validation(self):
        """Test data validation"""
        from src.utils import validate_data
        
        df = pd.DataFrame({
            'text': ['sample text'],
            'compound': [0.5]
        })
        
        # Should pass validation
        self.assertTrue(validate_data(df, ['text', 'compound']))
        
        # Should fail validation
        self.assertFalse(validate_data(df, ['text', 'missing_column']))


if __name__ == '__main__':
    unittest.main()