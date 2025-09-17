"""
AI Sentiment Analysis Project

This package provides tools for analyzing public sentiment on AI opinions
and uses of metaphor from online data sources and survey data.
"""

__version__ = "0.1.0"
__author__ = "AI Sentiment Analysis Team"

from .sentiment_analysis import SentimentAnalyzer
from .metaphor_analysis import MetaphorDetector
from .data_collection import DataCollector

__all__ = ['SentimentAnalyzer', 'MetaphorDetector', 'DataCollector']