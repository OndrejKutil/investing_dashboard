"""
404 Not Found page for the Investment Dashboard
"""

from dash import html, dcc


def create_404_layout():
    """Create the 404 not found page layout"""
    
    return html.Div([
        html.Div([
            html.H1("404", className="error-404"),
            html.H2("Page Not Found", className="text-center"),
            html.P([
                "Oops! The page you're looking for doesn't exist. ",
                "It might have been moved, deleted, or you entered the wrong URL."
            ], className="text-center text-muted"),
            
        ], className="error-404")
    ])


# Layout function to be imported by main.py
layout = create_404_layout()