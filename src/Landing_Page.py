import streamlit as st

# Configure the page for full-screen layout
st.set_page_config(
    page_title="Investment Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    # Header section
    st.title("Investment Dashboard")
    st.markdown("### Your Personal Finance & Investment Analysis Tool")
    st.markdown("---")
    
    # Welcome section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        Welcome to your comprehensive investment analysis dashboard! This tool provides you with 
        essential features for analyzing markets, calculating portfolio growth, and tracking 
        cryptocurrency sentiment.
        
        **Navigate through the sidebar** to explore different analysis tools and calculators.
        """)
    
    with col2:
        st.info("""
        **Quick Start**
        
        1. Use the sidebar to navigate
        2. Start with Ticker Analysis
        3. Try the Portfolio Calculator
        4. Check Crypto sentiment
        """)
    
    st.markdown("---")
    
    # Features overview
    st.markdown("## Dashboard Features")
    
    # Create three columns for features
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### Ticker Analysis
        
        Analyze individual stocks, ETFs, and securities with:
        - **Price charts** and technical indicators
        - **Financial metrics** and ratios
        - **Performance statistics**
        - **Comprehensive data** visualization
        
        Perfect for researching potential investments and tracking your holdings.
        """)
        
        if st.button("Start Analysis", key="ticker_btn"):
            st.switch_page("pages/Ticker_Analysis.py")
    
    with col2:
        st.markdown("""
        ### Investment Calculators
        
        Plan your financial future with:
        - **Portfolio Growth Calculator**
        - **Compound interest** projections
        - **Regular contribution** planning
        - **Visual growth** charts
        
        See how your investments can grow over time with different scenarios.
        """)
        
        if st.button("Calculate Growth", key="calc_btn"):
            st.switch_page("pages/Calculators.py")
    
    with col3:
        st.markdown("""
        ### Crypto Fear & Greed Index
        
        Track cryptocurrency market sentiment:
        - **Real-time** fear & greed data
        - **Historical trends** analysis
        - **Market psychology** insights
        - **Interactive charts**
        
        Understand market emotions to make better crypto decisions.
        """)
        
        if st.button("Check Sentiment", key="crypto_btn"):
            st.switch_page("pages/Crypto_Fear_and_Greed_Index.py")
    
    st.markdown("---")
    
    # Additional information
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### Market Data
        
        This dashboard provides access to:
        - Real-time and historical stock prices
        - Financial ratios and metrics
        - Cryptocurrency market data
        - Fear & greed sentiment indicators
        """)
    
    with col2:
        st.markdown("""
        ### Tools & Features
        
        Built with modern technologies:
        - Interactive Plotly charts
        - Real-time data fetching
        - Responsive design
        - Easy navigation
        """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <small>
        Investment Dashboard | Built for personal investment analysis<br>
        Use the sidebar navigation to explore all features
        </small>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()