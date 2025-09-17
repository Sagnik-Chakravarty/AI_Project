"""
Sentiment Analysis Module

This module provides tools for analyzing sentiment in text data related to AI opinions.
It includes various sentiment analysis approaches and specialized handling for AI-related content.
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Tuple, Optional
import logging
from datetime import datetime

# NLP and ML imports (would be actual imports in real implementation)
try:
    from textblob import TextBlob
    from transformers import pipeline
    import nltk
    from nltk.sentiment import SentimentIntensityAnalyzer
except ImportError:
    logging.warning("Some NLP libraries not available. Install requirements.txt")

logger = logging.getLogger(__name__)


class SentimentAnalyzer:
    """Main class for sentiment analysis of AI-related content"""
    
    def __init__(self, model_type: str = "textblob"):
        """
        Initialize sentiment analyzer
        
        Args:
            model_type: Type of sentiment model to use ('textblob', 'vader', 'transformers')
        """
        self.model_type = model_type
        self.analyzer = self._initialize_analyzer()
        
        # AI-specific sentiment keywords
        self.ai_positive_keywords = [
            'innovative', 'breakthrough', 'efficient', 'helpful', 'revolutionary',
            'promising', 'beneficial', 'advancement', 'progress', 'improvement'
        ]
        
        self.ai_negative_keywords = [
            'dangerous', 'threatening', 'replace', 'job loss', 'scary', 'risky',
            'uncontrolled', 'bias', 'discrimination', 'surveillance', 'manipulative'
        ]
        
        self.ai_neutral_keywords = [
            'algorithm', 'data', 'processing', 'computation', 'analysis',
            'model', 'system', 'technology', 'automated', 'digital'
        ]
    
    def _initialize_analyzer(self):
        """Initialize the sentiment analysis model"""
        if self.model_type == "textblob":
            return None  # TextBlob doesn't need initialization
        elif self.model_type == "vader":
            try:
                nltk.download('vader_lexicon', quiet=True)
                return SentimentIntensityAnalyzer()
            except:
                logger.warning("VADER not available, falling back to TextBlob")
                self.model_type = "textblob"
                return None
        elif self.model_type == "transformers":
            try:
                return pipeline("sentiment-analysis", 
                              model="cardiffnlp/twitter-roberta-base-sentiment-latest")
            except:
                logger.warning("Transformers not available, falling back to TextBlob")
                self.model_type = "textblob"
                return None
        else:
            raise ValueError(f"Unsupported model type: {self.model_type}")
    
    def analyze_text(self, text: str) -> Dict[str, float]:
        """
        Analyze sentiment of a single text
        
        Args:
            text: Input text to analyze
            
        Returns:
            Dictionary with sentiment scores
        """
        if not text or not isinstance(text, str):
            return {'compound': 0.0, 'positive': 0.0, 'negative': 0.0, 'neutral': 0.0}
        
        if self.model_type == "textblob":
            return self._analyze_textblob(text)
        elif self.model_type == "vader":
            return self._analyze_vader(text)
        elif self.model_type == "transformers":
            return self._analyze_transformers(text)
    
    def _analyze_textblob(self, text: str) -> Dict[str, float]:
        """Analyze sentiment using TextBlob"""
        try:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity  # -1 to 1
            subjectivity = blob.sentiment.subjectivity  # 0 to 1
            
            # Convert to standard format
            positive = max(0, polarity)
            negative = abs(min(0, polarity))
            neutral = 1 - abs(polarity)
            
            return {
                'compound': polarity,
                'positive': positive,
                'negative': negative,
                'neutral': neutral,
                'subjectivity': subjectivity
            }
        except Exception as e:
            logger.error(f"TextBlob analysis failed: {e}")
            return {'compound': 0.0, 'positive': 0.0, 'negative': 0.0, 'neutral': 1.0}
    
    def _analyze_vader(self, text: str) -> Dict[str, float]:
        """Analyze sentiment using VADER"""
        try:
            scores = self.analyzer.polarity_scores(text)
            return scores
        except Exception as e:
            logger.error(f"VADER analysis failed: {e}")
            return {'compound': 0.0, 'positive': 0.0, 'negative': 0.0, 'neutral': 1.0}
    
    def _analyze_transformers(self, text: str) -> Dict[str, float]:
        """Analyze sentiment using Transformers"""
        try:
            result = self.analyzer(text)
            label = result[0]['label']
            score = result[0]['score']
            
            # Convert to standard format
            if label == 'POSITIVE':
                return {'compound': score, 'positive': score, 'negative': 0.0, 'neutral': 1-score}
            elif label == 'NEGATIVE':
                return {'compound': -score, 'positive': 0.0, 'negative': score, 'neutral': 1-score}
            else:  # NEUTRAL
                return {'compound': 0.0, 'positive': 0.0, 'negative': 0.0, 'neutral': score}
        except Exception as e:
            logger.error(f"Transformers analysis failed: {e}")
            return {'compound': 0.0, 'positive': 0.0, 'negative': 0.0, 'neutral': 1.0}
    
    def analyze_ai_specific_sentiment(self, text: str) -> Dict[str, float]:
        """
        Analyze AI-specific sentiment considering domain-specific keywords
        
        Args:
            text: Input text to analyze
            
        Returns:
            Enhanced sentiment scores with AI-specific adjustments
        """
        base_sentiment = self.analyze_text(text)
        text_lower = text.lower()
        
        # Count AI-specific keywords
        positive_count = sum(1 for word in self.ai_positive_keywords if word in text_lower)
        negative_count = sum(1 for word in self.ai_negative_keywords if word in text_lower)
        
        # Adjust sentiment based on AI-specific keywords
        ai_adjustment = (positive_count - negative_count) * 0.1
        
        # Apply adjustment
        adjusted_compound = np.clip(base_sentiment['compound'] + ai_adjustment, -1, 1)
        
        return {
            **base_sentiment,
            'compound': adjusted_compound,
            'ai_positive_keywords': positive_count,
            'ai_negative_keywords': negative_count,
            'ai_adjustment': ai_adjustment
        }
    
    def analyze_batch(self, texts: List[str]) -> pd.DataFrame:
        """
        Analyze sentiment for a batch of texts
        
        Args:
            texts: List of texts to analyze
            
        Returns:
            DataFrame with sentiment analysis results
        """
        results = []
        
        for i, text in enumerate(texts):
            sentiment = self.analyze_ai_specific_sentiment(text)
            sentiment['text_id'] = i
            sentiment['text'] = text[:100] + "..." if len(text) > 100 else text
            sentiment['analysis_timestamp'] = datetime.now()
            results.append(sentiment)
        
        return pd.DataFrame(results)
    
    def categorize_sentiment(self, compound_score: float) -> str:
        """
        Categorize sentiment based on compound score
        
        Args:
            compound_score: Compound sentiment score (-1 to 1)
            
        Returns:
            Sentiment category ('positive', 'negative', 'neutral')
        """
        if compound_score >= 0.05:
            return 'positive'
        elif compound_score <= -0.05:
            return 'negative'
        else:
            return 'neutral'
    
    def get_sentiment_summary(self, df: pd.DataFrame) -> Dict:
        """
        Get summary statistics for sentiment analysis results
        
        Args:
            df: DataFrame with sentiment analysis results
            
        Returns:
            Dictionary with summary statistics
        """
        if df.empty:
            return {}
        
        # Add sentiment categories
        df['sentiment_category'] = df['compound'].apply(self.categorize_sentiment)
        
        summary = {
            'total_texts': len(df),
            'average_compound': df['compound'].mean(),
            'sentiment_distribution': df['sentiment_category'].value_counts().to_dict(),
            'most_positive': df.loc[df['compound'].idxmax()]['text'] if len(df) > 0 else "",
            'most_negative': df.loc[df['compound'].idxmin()]['text'] if len(df) > 0 else "",
            'ai_keyword_stats': {
                'avg_positive_keywords': df['ai_positive_keywords'].mean(),
                'avg_negative_keywords': df['ai_negative_keywords'].mean()
            }
        }
        
        return summary


if __name__ == "__main__":
    # Example usage
    analyzer = SentimentAnalyzer()
    
    # Sample AI-related texts
    sample_texts = [
        "AI is revolutionary and will bring amazing benefits to humanity",
        "I'm worried that AI might replace human jobs and cause unemployment",
        "Machine learning algorithms are processing data efficiently",
        "Artificial intelligence is dangerous and threatens our privacy"
    ]
    
    # Analyze sentiment
    results = analyzer.analyze_batch(sample_texts)
    summary = analyzer.get_sentiment_summary(results)
    
    print("Sentiment Analysis Results:")
    print(results[['text', 'compound', 'sentiment_category']].to_string())
    print("\nSummary:", summary)