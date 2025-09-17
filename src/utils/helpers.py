"""
Utility functions for the AI Sentiment Analysis project
"""

import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


def setup_logging(level: str = "INFO", log_file: Optional[str] = None):
    """Setup logging configuration"""
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(log_file) if log_file else logging.NullHandler()
        ]
    )


def ensure_directory(path: str):
    """Ensure a directory exists, create if it doesn't"""
    if not os.path.exists(path):
        os.makedirs(path)
        logger.info(f"Created directory: {path}")


def save_results(data: Dict, filename: str, output_dir: str = "results"):
    """Save analysis results to JSON file"""
    ensure_directory(output_dir)
    filepath = os.path.join(output_dir, filename)
    
    # Convert any datetime objects to strings for JSON serialization
    def convert_datetime(obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, dict):
            return {k: convert_datetime(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_datetime(item) for item in obj]
        return obj
    
    with open(filepath, 'w') as f:
        json.dump(convert_datetime(data), f, indent=2)
    
    logger.info(f"Results saved to {filepath}")


def load_config(config_path: str) -> Dict:
    """Load configuration from JSON file"""
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            return json.load(f)
    else:
        logger.warning(f"Config file {config_path} not found")
        return {}


def create_sample_config():
    """Create a sample configuration file"""
    sample_config = {
        "api_keys": {
            "twitter_bearer_token": "your_twitter_bearer_token_here",
            "reddit_client_id": "your_reddit_client_id_here",
            "reddit_client_secret": "your_reddit_client_secret_here",
            "news_api_key": "your_news_api_key_here"
        },
        "data_collection": {
            "default_keywords": ["artificial intelligence", "AI", "machine learning", "AI ethics"],
            "days_back": 7,
            "max_results": 1000
        },
        "analysis": {
            "sentiment_model": "textblob",
            "enable_metaphor_analysis": True,
            "save_detailed_results": True
        }
    }
    
    ensure_directory("config")
    with open("config/config.json", 'w') as f:
        json.dump(sample_config, f, indent=2)
    
    logger.info("Sample configuration created at config/config.json")


def plot_sentiment_distribution(sentiment_data: pd.DataFrame, save_path: str = None):
    """Create visualization for sentiment distribution"""
    if 'sentiment_category' not in sentiment_data.columns:
        # Add sentiment categories if not present
        sentiment_data['sentiment_category'] = sentiment_data['compound'].apply(
            lambda x: 'positive' if x >= 0.05 else 'negative' if x <= -0.05 else 'neutral'
        )
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Sentiment distribution pie chart
    sentiment_counts = sentiment_data['sentiment_category'].value_counts()
    colors = ['lightgreen', 'lightcoral', 'lightblue']
    ax1.pie(sentiment_counts.values, labels=sentiment_counts.index, autopct='%1.1f%%', 
            colors=colors, startangle=90)
    ax1.set_title('Sentiment Distribution')
    
    # Sentiment score histogram
    ax2.hist(sentiment_data['compound'], bins=30, alpha=0.7, color='skyblue', edgecolor='black')
    ax2.set_xlabel('Sentiment Score')
    ax2.set_ylabel('Frequency')
    ax2.set_title('Distribution of Sentiment Scores')
    ax2.axvline(x=0, color='red', linestyle='--', alpha=0.7, label='Neutral')
    ax2.legend()
    
    plt.tight_layout()
    
    if save_path:
        ensure_directory(os.path.dirname(save_path))
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        logger.info(f"Sentiment plot saved to {save_path}")
    
    plt.show()


def plot_metaphor_analysis(metaphor_data: pd.DataFrame, save_path: str = None):
    """Create visualization for metaphor analysis"""
    # Get metaphor category columns
    metaphor_columns = [col for col in metaphor_data.columns if col.endswith('_count')]
    
    if not metaphor_columns:
        logger.warning("No metaphor count columns found in data")
        return
    
    # Calculate metaphor category totals
    metaphor_totals = {}
    for col in metaphor_columns:
        category = col.replace('_count', '')
        metaphor_totals[category] = metaphor_data[col].sum()
    
    # Create visualization
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Bar chart of metaphor categories
    categories = list(metaphor_totals.keys())
    counts = list(metaphor_totals.values())
    
    bars = ax1.bar(categories, counts, color='lightsteelblue', edgecolor='navy')
    ax1.set_xlabel('Metaphor Categories')
    ax1.set_ylabel('Total Occurrences')
    ax1.set_title('Metaphor Category Usage')
    ax1.tick_params(axis='x', rotation=45)
    
    # Add value labels on bars
    for bar, count in zip(bars, counts):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, 
                str(count), ha='center', va='bottom')
    
    # Metaphor density distribution
    if 'metaphor_density' in metaphor_data.columns:
        ax2.hist(metaphor_data['metaphor_density'], bins=20, alpha=0.7, 
                color='lightcoral', edgecolor='darkred')
        ax2.set_xlabel('Metaphor Density (metaphors per word)')
        ax2.set_ylabel('Frequency')
        ax2.set_title('Distribution of Metaphor Density')
    
    plt.tight_layout()
    
    if save_path:
        ensure_directory(os.path.dirname(save_path))
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        logger.info(f"Metaphor plot saved to {save_path}")
    
    plt.show()


def generate_report(sentiment_results: Dict, metaphor_results: Dict, 
                   output_path: str = "results/analysis_report.html"):
    """Generate an HTML report with analysis results"""
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>AI Sentiment and Metaphor Analysis Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            .header {{ background-color: #f0f0f0; padding: 20px; border-radius: 5px; }}
            .section {{ margin: 20px 0; }}
            .metric {{ background-color: #e8f4fd; padding: 10px; margin: 5px 0; border-radius: 3px; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>AI Sentiment and Metaphor Analysis Report</h1>
            <p>Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        
        <div class="section">
            <h2>Sentiment Analysis Summary</h2>
            <div class="metric">
                <strong>Total Texts Analyzed:</strong> {sentiment_results.get('total_texts', 'N/A')}
            </div>
            <div class="metric">
                <strong>Average Sentiment Score:</strong> {sentiment_results.get('average_compound', 'N/A'):.3f}
            </div>
            
            <h3>Sentiment Distribution</h3>
            <table>
                <tr><th>Sentiment</th><th>Count</th><th>Percentage</th></tr>
    """
    
    # Add sentiment distribution
    sentiment_dist = sentiment_results.get('sentiment_distribution', {})
    total = sum(sentiment_dist.values()) if sentiment_dist else 1
    for sentiment, count in sentiment_dist.items():
        percentage = (count / total) * 100
        html_content += f"<tr><td>{sentiment.title()}</td><td>{count}</td><td>{percentage:.1f}%</td></tr>"
    
    html_content += """
            </table>
        </div>
        
        <div class="section">
            <h2>Metaphor Analysis Summary</h2>
    """
    
    # Add metaphor analysis
    if metaphor_results:
        html_content += f"""
            <div class="metric">
                <strong>Texts with Metaphors:</strong> {metaphor_results.get('texts_with_metaphors', 'N/A')}
            </div>
            <div class="metric">
                <strong>Average Metaphor Density:</strong> {metaphor_results.get('average_metaphor_density', 'N/A'):.4f}
            </div>
            
            <h3>Metaphor Categories</h3>
            <table>
                <tr><th>Category</th><th>Total Occurrences</th><th>Texts with Category</th></tr>
        """
        
        metaphor_categories = metaphor_results.get('metaphor_category_counts', {})
        for category, data in metaphor_categories.items():
            html_content += f"""
                <tr>
                    <td>{category.replace('_', ' ').title()}</td>
                    <td>{data.get('total_occurrences', 0)}</td>
                    <td>{data.get('texts_with_category', 0)}</td>
                </tr>
            """
    
    html_content += """
            </table>
        </div>
        
        <div class="section">
            <h2>Key Insights</h2>
            <ul>
                <li>This analysis provides insights into public sentiment about AI</li>
                <li>Metaphor usage reveals how people conceptualize AI technology</li>
                <li>Results can inform AI communication and policy strategies</li>
            </ul>
        </div>
    </body>
    </html>
    """
    
    ensure_directory(os.path.dirname(output_path))
    with open(output_path, 'w') as f:
        f.write(html_content)
    
    logger.info(f"Report generated: {output_path}")


def validate_data(df: pd.DataFrame, required_columns: List[str]) -> bool:
    """Validate that DataFrame has required columns"""
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        logger.error(f"Missing required columns: {missing_columns}")
        return False
    
    return True


def clean_text(text: str) -> str:
    """Basic text cleaning function"""
    if not isinstance(text, str):
        return ""
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    # Remove very short texts
    if len(text.split()) < 3:
        return ""
    
    return text


if __name__ == "__main__":
    # Example usage
    setup_logging()
    create_sample_config()
    logger.info("Utilities module loaded successfully")