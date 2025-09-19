# Investment Dashboard

A personal investment analysis tool built with Streamlit for analyzing stocks, calculating portfolio growth, and tracking cryptocurrency market sentiment.

## Features

### Ticker Analysis

- Analyze individual stocks, ETFs, and securities
- Price charts and technical indicators
- Financial metrics and ratios
- Performance statistics
- Comprehensive data visualization

### Investment Calculators

- Portfolio Growth Calculator
- Compound interest projections
- Regular contribution planning
- Visual growth charts

### Crypto Fear & Greed Index

- Real-time fear & greed data
- Historical trends analysis
- Market psychology insights
- Interactive charts

## Installation

1. Clone the repository
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the dashboard:

```bash
streamlit run src/Landing_Page.py
```

Navigate through the sidebar to access different features:

- **Ticker Analysis** - Research stocks and ETFs
- **Calculators** - Plan your investment growth
- **Crypto Fear & Greed Index** - Track crypto market sentiment

## Technologies Used

- **Streamlit** - Web app framework
- **Plotly** - Interactive charts
- **Pandas** - Data manipulation
- **Python** - Core programming language

## Project Structure

```bash
src/
├── Landing_Page.py          # Main landing page
├── pages/
│   ├── Calculators.py       # Investment calculators
│   ├── Ticker_Analysis.py   # Stock analysis tools
│   └── Crypto_Fear_and_Greed_Index.py  # Crypto sentiment
├── helper/
│   ├── calc/               # Calculation modules
│   ├── data/               # Data fetching modules
│   └── stats.py            # Statistical functions
└── utils/
    └── theme.py            # UI theme configuration
```

## Note

This is a personal project for investment analysis and educational purposes.
