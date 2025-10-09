import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc

# Import components
from utils.navigation import create_navigation
from pages.home import create_home_layout
from pages.page_404 import create_404_layout

app = dash.Dash(__name__,
                title="Dashboard",
                update_title=None,
                assets_folder='styles')

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    
    # Navigation Header - will be updated dynamically
    html.Div(id='navigation-container'),
    
    # Page content
    html.Div(id='page-content')
])

@app.callback(
    [Output("navigation-container", "children"),
     Output("page-content", "children")],
    Input("url", "pathname")
)
def update_page(pathname):
    # Update navigation with current path
    navigation = create_navigation(pathname)
    
    # Update page content
    if pathname == "/":
        content = create_home_layout()
    elif pathname == "/ticker-analysis":
        content = html.Div()  # Empty for now
    elif pathname == "/calculators":
        content = html.Div()  # Empty for now
    elif pathname == "/crypto-sentiment":
        content = html.Div()  # Empty for now
    else:
        content = create_404_layout()
    
    return navigation, content
    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050)