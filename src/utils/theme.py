chart_background = {
    "paper_bgcolor": "#212430",
    "plot_bgcolor": '#212430'
}

# Primary brand colors - bright and visible on dark backgrounds
LINE_COLOR: str = "#4bb4ff"  # Bright blue - main line color
PRIMARY_BLUE = "#4bb4ff"      # Same as LINE_COLOR for consistency
SECONDARY_BLUE = "#3b82f6"    # Medium blue

# Chart colors for different data series - high contrast on dark backgrounds
CHART_COLORS = {
    # Moving averages
    "ma_20": "#f97316",      # Bright orange - 20-day MA
    "ma_50": "#ef4444",      # Bright red - 50-day MA  
    "ma_200": "#a855f7",     # Bright purple - 200-day MA
    
    # Volume and bars
    "volume": "#4bb4ff",     # Primary blue for volume bars
    "volume_alpha": "rgba(75, 180, 255, 0.7)",  # Semi-transparent volume
    
    # Technical indicators
    "macd": "#3b82f6",       # Blue for MACD line
    "macd_signal": "#f97316", # Orange for MACD signal
    "macd_hist": "rgba(75, 180, 255, 0.5)",  # Semi-transparent blue for histogram
    "rsi": "#8b5cf6",        # Purple for RSI
    
    # Volatility
    "volatility_30d": "#4bb4ff",  # Primary blue
    "volatility_60d": "#f97316",   # Orange
    
    # Benchmark/reference
    "benchmark": "rgba(156, 163, 175, 0.8)",  # Light gray for benchmark
    "reference_line": "rgba(156, 163, 175, 0.4)",  # Very light gray for reference lines
}

# Status and zone colors - semantic colors for performance zones
STATUS_COLORS = {
    # Performance zones (for drawdown analysis)
    "excellent": "#10b981",    # Bright green
    "good": "#84cc16",         # Lime green  
    "moderate": "#f59e0b",     # Amber/orange
    "poor": "#ef4444",         # Red
    
    # Zone colors with transparency for background fills
    "excellent_zone": "rgba(16, 185, 129, 0.15)",
    "good_zone": "rgba(132, 204, 22, 0.15)", 
    "moderate_zone": "rgba(245, 158, 11, 0.15)",
    "poor_zone": "rgba(239, 68, 68, 0.15)",
    
    # Legend colors (more opaque)
    "excellent_legend": "rgba(16, 185, 129, 0.8)",
    "good_legend": "rgba(132, 204, 22, 0.8)",
    "moderate_legend": "rgba(245, 158, 11, 0.8)", 
    "poor_legend": "rgba(239, 68, 68, 0.8)",
}

# RSI indicator colors  
RSI_COLORS = {
    "line": "#8b5cf6",        # Purple for RSI line
    "overbought": "#ceff1d",   # Red for overbought level (70+)
    "oversold": "#ff4646",     # Cyan for oversold level (30-)
}

# Fear and Greed index colors
FEAR_GREED_COLORS = {
    "extreme_fear": "#dc2626",    # Dark red
    "fear": "#f87171",            # Light red
    "neutral": "#eab308",         # Yellow
    "greed": "#84cc16",           # Light green
    "extreme_greed": "#16a34a",   # Dark green
    "line": "#4bb4ff",            # Primary blue for the line
}

# Text and grid colors for dark theme
TEXT_COLORS = {
    "primary": "#f3f4f6",      # Light gray for primary text
    "secondary": "#d1d5db",    # Medium gray for secondary text
    "muted": "#9ca3af",        # Darker gray for muted text
}

GRID_COLORS = {
    "major": "rgba(156, 163, 175, 0.2)",   # Light grid lines
    "minor": "rgba(156, 163, 175, 0.1)",   # Very light grid lines
    "zero_line": "rgba(156, 163, 175, 0.3)", # Zero reference line
}

# Fill colors for areas under curves
FILL_COLORS = {
    "drawdown": "rgba(239, 68, 68, 0.15)",   # Light red for drawdown fill (more visible)
    "positive": "rgba(16, 185, 129, 0.1)",  # Light green for positive areas
    "negative": "rgba(239, 68, 68, 0.1)",   # Light red for negative areas
}
