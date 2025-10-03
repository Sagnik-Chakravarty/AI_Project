# Copilot Instructions for AI_Project

## Project Overview
This is a data collection and analysis project focused on gathering and processing AI-related content from social media platforms, particularly Reddit. The project uses R with Quarto for data collection, analysis, and reporting.

## Architecture & Structure
```
AI_Project/
├── Data Collection/          # Data gathering modules organized by source
│   └── Internet/            # Web-based data collection scripts
│       └── reddit.qmd      # Reddit data extraction using RedditExtractoR
└── README.md               # Project documentation
```

## Technology Stack
- **R**: Primary language for data collection and analysis
- **Quarto (.qmd)**: Literate programming for reproducible research and reporting
- **RedditExtractoR**: R package for Reddit API data extraction
- **dplyr**: Data manipulation and transformation

## Development Patterns

### File Organization
- Use `.qmd` (Quarto markdown) files for data collection scripts that combine code, analysis, and documentation
- Organize data sources under `Data Collection/` with subdirectories by platform (`Internet/`, future: `APIs/`, `Files/`, etc.)
- Each data source should have its own `.qmd` file with descriptive names (e.g., `reddit.qmd`, `twitter.qmd`)

### Quarto Document Structure
Follow this pattern for `.qmd` files:
```yaml
---
title: "[Source] data collection"
format: pdf
editor: visual
---
```

### R Code Conventions
- Install packages in separate code chunks at the beginning of documents
- Use `library()` calls in dedicated chunks before main analysis
- Structure data collection scripts with clear sections: "Finding", "Extracting", "Processing"
- Use `dplyr` pipes (`%>%`) for data transformations
- Include `print()` statements for debugging and verification

### Data Collection Workflow
1. **Package Installation**: Always start with `install.packages()` in first chunk
2. **Library Loading**: Load required libraries in second chunk  
3. **Data Discovery**: Use search/find functions to identify relevant data sources
4. **Data Extraction**: Collect raw data using appropriate APIs/packages
5. **Data Processing**: Clean and transform using `dplyr` operations

## Key Dependencies
- **RedditExtractoR**: For Reddit data collection - use `find_subreddits()` for discovery and `reddit_content()` for extraction
- **dplyr**: Standard data manipulation - prefer pipe operations for readability

## Workflow Commands
- Render Quarto documents: `quarto render filename.qmd`
- Install R packages interactively in RStudio or R console
- View PDF outputs after rendering

## Common Patterns
- Start with broad searches (`find_subreddits("Artificial Intelligence")`) then filter
- Use `select()` operations to choose relevant columns for analysis
- Structure code in logical chunks for step-by-step execution and debugging

## Future Expansion Areas
Based on current structure, expect expansion into:
- Additional social media platforms under `Data Collection/Internet/`
- API-based collection under `Data Collection/APIs/`
- Analysis and modeling scripts in separate directories
- Configuration files for API credentials and settings