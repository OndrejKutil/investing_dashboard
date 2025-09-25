"""
Home/Landing page layout for the Investment Dashboard
"""

from dash import html


def create_home_layout():
    """Create the home page layout"""
    
    return html.Div([
        html.Div([
            html.H2("Welcome to the Investment Dashboard!", className="text-center mb-4"),
            html.P([
                "Your comprehensive tool for financial analysis and investment calculations. ",
                "Choose from the options below to get started:"
            ], className="text-center text-muted mb-5"),
            
            # Feature cards
            html.Div([
                # Ticker Analysis Card
                html.Div([
                    html.Div([
                        html.Div([
                            html.H4("Ticker Analysis", className="text-accent mb-3"),
                            html.P("Analyze stocks, ETFs, and other securities with comprehensive metrics, charts, and technical indicators.", 
                                   className="text-muted mb-3"),
                            html.A("Analyze Tickers", href="/ticker-analysis", className="btn btn-primary")
                        ], className="feature-card-content")
                    ], className="card feature-card text-center")
                ], className="col-md-4 mb-4"),
                
                # Investment Calculators Card
                html.Div([
                    html.Div([
                        html.Div([
                            html.H4("Investment Calculators", className="text-accent mb-3"),
                            html.P("Calculate portfolio growth, compound interest, and plan your investment strategy with our powerful calculators.", 
                                   className="text-muted mb-3"),
                            html.A("Use Calculators", href="/calculators", className="btn btn-primary")
                        ], className="feature-card-content")
                    ], className="card feature-card text-center")
                ], className="col-md-4 mb-4"),
                
                # Crypto Fear & Greed Card
                html.Div([
                    html.Div([
                        html.Div([
                            html.H4("Crypto Fear & Greed", className="text-accent mb-3"),
                            html.P("Monitor cryptocurrency market sentiment with the Fear and Greed Index to time your crypto investments.", 
                                   className="text-muted mb-3"),
                            html.A("Check Sentiment", href="/crypto-sentiment", className="btn btn-primary")
                        ], className="feature-card-content")
                    ], className="card feature-card text-center")
                ], className="col-md-4 mb-4"),
            ], className="row justify-content-center"),
            
        ], className="container-fluid home-content")
    ])