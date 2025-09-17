"""
Metaphor Analysis Module

This module provides tools for detecting and analyzing metaphors used in AI-related discourse.
It identifies common metaphorical patterns and their implications for public understanding of AI.
"""

import pandas as pd
import numpy as np
import re
from typing import List, Dict, Tuple, Optional
import logging
from collections import Counter
from datetime import datetime

logger = logging.getLogger(__name__)


class MetaphorDetector:
    """Main class for detecting and analyzing metaphors in AI-related text"""
    
    def __init__(self):
        """Initialize the metaphor detector with predefined patterns"""
        
        # Common AI metaphors categorized by theme
        self.metaphor_patterns = {
            'human_like': {
                'patterns': [
                    r'\b(AI|artificial intelligence|machine|robot|algorithm)\s+(learns?|thinks?|knows?|understands?|decides?|believes?)\b',
                    r'\b(AI|artificial intelligence|machine|robot)\s+(brain|mind|intelligence|consciousness)\b',
                    r'\b(smart|intelligent|clever)\s+(AI|machine|robot|algorithm)\b',
                    r'\b(AI|machine|robot)\s+(behavior|personality|character|emotions?)\b'
                ],
                'keywords': ['learn', 'think', 'know', 'understand', 'decide', 'believe', 'brain', 'mind', 'smart', 'intelligent', 'behavior', 'personality']
            },
            
            'tool_instrument': {
                'patterns': [
                    r'\bAI\s+(tool|instrument|device|utility|application)\b',
                    r'\b(use|using|utilize|employ|leverage)\s+AI\b',
                    r'\bAI\s+(helps?|assists?|aids?|supports?)\b',
                    r'\b(hammer|screwdriver|calculator|computer)\s+of\s+the\s+future\b'
                ],
                'keywords': ['tool', 'instrument', 'device', 'utility', 'application', 'use', 'employ', 'leverage', 'helps', 'assists']
            },
            
            'master_slave': {
                'patterns': [
                    r'\bAI\s+(masters?|controls?|dominates?|rules?|governs?)\b',
                    r'\b(humans?|people|we)\s+(serve|obey|submit to)\s+AI\b',
                    r'\bAI\s+(overlords?|masters?|rulers?)\b',
                    r'\b(enslaved?|controlled|dominated)\s+by\s+AI\b'
                ],
                'keywords': ['master', 'control', 'dominate', 'rule', 'govern', 'serve', 'obey', 'submit', 'overlord', 'enslaved']
            },
            
            'partnership': {
                'patterns': [
                    r'\b(human|AI)\s+(partnership|collaboration|cooperation|teamwork)\b',
                    r'\b(work|working)\s+(with|alongside)\s+AI\b',
                    r'\bAI\s+(partner|colleague|ally|companion)\b',
                    r'\b(human|AI)\s+collaboration\b'
                ],
                'keywords': ['partnership', 'collaboration', 'cooperation', 'teamwork', 'work with', 'alongside', 'partner', 'colleague', 'ally']
            },
            
            'biological': {
                'patterns': [
                    r'\bAI\s+(evolution|evolves?|evolving|evolved)\b',
                    r'\b(neural|brain|organic|biological)\s+AI\b',
                    r'\bAI\s+(ecosystem|environment|habitat)\b',
                    r'\b(artificial|digital)\s+(DNA|genes?|genome)\b',
                    r'\bAI\s+(species|organism|life form)\b'
                ],
                'keywords': ['evolution', 'evolve', 'neural', 'brain', 'organic', 'biological', 'ecosystem', 'DNA', 'genes', 'species', 'organism']
            },
            
            'threat_war': {
                'patterns': [
                    r'\bAI\s+(threat|danger|enemy|opponent|adversary)\b',
                    r'\b(war|battle|fight|combat|struggle)\s+(against|with)\s+AI\b',
                    r'\bAI\s+(invasion|attack|assault|conquest)\b',
                    r'\b(defend|defense|protect|resistance)\s+(against|from)\s+AI\b'
                ],
                'keywords': ['threat', 'danger', 'enemy', 'opponent', 'war', 'battle', 'fight', 'invasion', 'attack', 'defend', 'resistance']
            },
            
            'magic_supernatural': {
                'patterns': [
                    r'\bAI\s+(magic|magical|mystical|supernatural)\b',
                    r'\b(artificial|digital|silicon)\s+(wizard|sorcerer|oracle|prophet)\b',
                    r'\bAI\s+(powers?|abilities|capabilities)\b',
                    r'\b(black box|mysterious|inexplicable)\s+AI\b'
                ],
                'keywords': ['magic', 'magical', 'mystical', 'supernatural', 'wizard', 'sorcerer', 'oracle', 'powers', 'mysterious']
            }
        }
        
        # Compile regex patterns for efficiency
        self.compiled_patterns = {}
        for category, data in self.metaphor_patterns.items():
            self.compiled_patterns[category] = [
                re.compile(pattern, re.IGNORECASE) for pattern in data['patterns']
            ]
    
    def detect_metaphors(self, text: str) -> Dict[str, any]:
        """
        Detect metaphors in a given text
        
        Args:
            text: Input text to analyze
            
        Returns:
            Dictionary with detected metaphors by category
        """
        if not text or not isinstance(text, str):
            return {category: {'count': 0, 'matches': []} for category in self.metaphor_patterns.keys()}
        
        results = {}
        text_lower = text.lower()
        
        for category, patterns in self.compiled_patterns.items():
            matches = []
            
            # Check regex patterns
            for pattern in patterns:
                found_matches = pattern.findall(text)
                matches.extend(found_matches)
            
            # Check keyword presence
            keywords = self.metaphor_patterns[category]['keywords']
            keyword_matches = [kw for kw in keywords if kw in text_lower]
            
            results[category] = {
                'count': len(matches) + len(keyword_matches),
                'pattern_matches': matches,
                'keyword_matches': keyword_matches,
                'total_matches': len(set(matches + keyword_matches))
            }
        
        return results
    
    def analyze_metaphor_sentiment(self, text: str, metaphor_results: Dict) -> Dict:
        """
        Analyze the sentiment associated with different metaphor categories
        
        Args:
            text: Original text
            metaphor_results: Results from detect_metaphors
            
        Returns:
            Dictionary with sentiment analysis for each metaphor category
        """
        # Simple sentiment indicators for metaphor analysis
        positive_indicators = ['beneficial', 'helpful', 'useful', 'good', 'great', 'amazing', 'wonderful', 'positive']
        negative_indicators = ['dangerous', 'harmful', 'bad', 'terrible', 'awful', 'negative', 'scary', 'threatening']
        
        text_lower = text.lower()
        metaphor_sentiment = {}
        
        for category, data in metaphor_results.items():
            if data['count'] > 0:
                # Count positive/negative indicators near metaphors
                positive_count = sum(1 for word in positive_indicators if word in text_lower)
                negative_count = sum(1 for word in negative_indicators if word in text_lower)
                
                # Determine overall sentiment for this metaphor category
                if positive_count > negative_count:
                    sentiment = 'positive'
                elif negative_count > positive_count:
                    sentiment = 'negative'
                else:
                    sentiment = 'neutral'
                
                metaphor_sentiment[category] = {
                    'sentiment': sentiment,
                    'positive_indicators': positive_count,
                    'negative_indicators': negative_count,
                    'metaphor_count': data['count']
                }
        
        return metaphor_sentiment
    
    def analyze_batch(self, texts: List[str]) -> pd.DataFrame:
        """
        Analyze metaphors for a batch of texts
        
        Args:
            texts: List of texts to analyze
            
        Returns:
            DataFrame with metaphor analysis results
        """
        results = []
        
        for i, text in enumerate(texts):
            metaphor_results = self.detect_metaphors(text)
            metaphor_sentiment = self.analyze_metaphor_sentiment(text, metaphor_results)
            
            # Flatten results for DataFrame
            row = {
                'text_id': i,
                'text': text[:100] + "..." if len(text) > 100 else text,
                'analysis_timestamp': datetime.now()
            }
            
            # Add metaphor counts
            for category, data in metaphor_results.items():
                row[f'{category}_count'] = data['count']
                row[f'{category}_matches'] = str(data.get('pattern_matches', []))
            
            # Add sentiment data
            for category, sentiment_data in metaphor_sentiment.items():
                row[f'{category}_sentiment'] = sentiment_data['sentiment']
            
            # Calculate overall metaphor density
            total_metaphors = sum(data['count'] for data in metaphor_results.values())
            row['total_metaphors'] = total_metaphors
            row['metaphor_density'] = total_metaphors / len(text.split()) if text.split() else 0
            
            results.append(row)
        
        return pd.DataFrame(results)
    
    def get_metaphor_summary(self, df: pd.DataFrame) -> Dict:
        """
        Get summary statistics for metaphor analysis results
        
        Args:
            df: DataFrame with metaphor analysis results
            
        Returns:
            Dictionary with summary statistics
        """
        if df.empty:
            return {}
        
        summary = {
            'total_texts': len(df),
            'texts_with_metaphors': len(df[df['total_metaphors'] > 0]),
            'average_metaphor_density': df['metaphor_density'].mean(),
            'metaphor_category_counts': {}
        }
        
        # Count metaphors by category
        for category in self.metaphor_patterns.keys():
            count_col = f'{category}_count'
            if count_col in df.columns:
                summary['metaphor_category_counts'][category] = {
                    'total_occurrences': df[count_col].sum(),
                    'texts_with_category': len(df[df[count_col] > 0]),
                    'average_per_text': df[count_col].mean()
                }
        
        # Find most common metaphor categories
        category_totals = {cat: data['total_occurrences'] 
                          for cat, data in summary['metaphor_category_counts'].items()}
        summary['most_common_categories'] = sorted(category_totals.items(), 
                                                 key=lambda x: x[1], reverse=True)
        
        return summary
    
    def extract_metaphor_examples(self, df: pd.DataFrame, category: str, limit: int = 5) -> List[str]:
        """
        Extract example texts that contain specific metaphor categories
        
        Args:
            df: DataFrame with metaphor analysis results
            category: Metaphor category to extract examples for
            limit: Maximum number of examples to return
            
        Returns:
            List of example texts
        """
        count_col = f'{category}_count'
        if count_col not in df.columns:
            return []
        
        # Get texts with this metaphor category
        category_texts = df[df[count_col] > 0].copy()
        
        # Sort by metaphor count and return top examples
        category_texts = category_texts.sort_values(count_col, ascending=False)
        
        return category_texts['text'].head(limit).tolist()
    
    def compare_metaphor_usage(self, df1: pd.DataFrame, df2: pd.DataFrame, 
                              label1: str = "Dataset 1", label2: str = "Dataset 2") -> Dict:
        """
        Compare metaphor usage between two datasets
        
        Args:
            df1, df2: DataFrames with metaphor analysis results
            label1, label2: Labels for the datasets
            
        Returns:
            Comparison results
        """
        comparison = {
            'datasets': {label1: {}, label2: {}},
            'differences': {}
        }
        
        # Get summaries for each dataset
        summary1 = self.get_metaphor_summary(df1)
        summary2 = self.get_metaphor_summary(df2)
        
        comparison['datasets'][label1] = summary1
        comparison['datasets'][label2] = summary2
        
        # Calculate differences
        for category in self.metaphor_patterns.keys():
            avg1 = summary1.get('metaphor_category_counts', {}).get(category, {}).get('average_per_text', 0)
            avg2 = summary2.get('metaphor_category_counts', {}).get(category, {}).get('average_per_text', 0)
            
            comparison['differences'][category] = {
                'difference': avg2 - avg1,
                'ratio': avg2 / avg1 if avg1 > 0 else float('inf') if avg2 > 0 else 1
            }
        
        return comparison


if __name__ == "__main__":
    # Example usage
    detector = MetaphorDetector()
    
    # Sample AI-related texts with different metaphors
    sample_texts = [
        "AI is like a brilliant brain that can learn and think faster than humans",
        "We need to use AI as a powerful tool to solve complex problems",
        "The AI overlords will control humanity unless we resist their dominance",
        "Humans and AI should work together in partnership for a better future",
        "AI evolution is happening rapidly in this digital ecosystem",
        "We must defend against the AI invasion threatening our jobs"
    ]
    
    # Analyze metaphors
    results = detector.analyze_batch(sample_texts)
    summary = detector.get_metaphor_summary(results)
    
    print("Metaphor Analysis Results:")
    print(results[['text', 'total_metaphors', 'metaphor_density']].to_string())
    print("\nSummary:", summary)
    
    # Extract examples
    print("\nHuman-like metaphor examples:")
    examples = detector.extract_metaphor_examples(results, 'human_like')
    for example in examples:
        print(f"- {example}")