"""
Navigation component for the Investment Dashboard
"""

from dash import html


def create_navigation(current_path="/"):
    """Create the navigation header component with active state management"""
    
    return html.Div([
        html.Nav([
            html.A(
                "Home", 
                href="/", 
                className="nav-link" + (" active" if current_path == "/" else "")
            ),
            html.A(
                "Ticker Analysis", 
                href="/ticker-analysis", 
                className="nav-link" + (" active" if current_path == "/ticker-analysis" else "")
            ),
            html.A(
                "Calculators", 
                href="/calculators", 
                className="nav-link" + (" active" if current_path == "/calculators" else "")
            ),
            html.A(
                "Crypto F&G Index", 
                href="/crypto-sentiment", 
                className="nav-link" + (" active" if current_path == "/crypto-sentiment" else "")
            ),
        ], className="nav-container")
    ], className="navigation-wrapper")