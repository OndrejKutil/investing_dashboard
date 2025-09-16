import streamlit as st
import plotly.graph_objects as go
import pandas as pd

from helper.download_data import fetch_price_data, fetch_benchmark_data, fetch_pe_ratio, fetch_trailing_pe_ratio, fetch_forward_pe_ratio, fetch_comprehensive_data
from helper.data import add_statistics
from helper.stats import Metrics


# TODO ################################################################################################
# TODO Move all dataframe calcultation to seperate helper function, this file should only handle the UI
# TODO ################################################################################################


def main():
    """Main function for the Ticker Analysis page"""
    
    # Page header
    st.title("Ticker Analysis")
    st.markdown("Analyze individual stocks, ETFs, and other securities with comprehensive metrics and visualizations.")
    
    # Create dropdown controls in one row
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        asset_type = st.text_input(
            "Ticker symbol",
            value="",
            label_visibility="collapsed",
            placeholder="Enter ticker symbol (e.g., AAPL, MSFT)"
        )

    with col2:
        # Benchmark selection dropdown
        benchmark_options = {
            "MSCI World (URTH)": "URTH",
            "S&P 500 (SPY)": "SPY", 
            "Russell 2000 (IWM)": "IWM",
            "Europe (VGK)": "VGK",
            "Prague Index (^PX)": "^PX"
        }
        
        selected_benchmark = st.selectbox(
            "Benchmark",
            options=list(benchmark_options.keys()),
            index=0,  # Default to MSCI World
            label_visibility="collapsed"
        )
        
        benchmark_ticker = benchmark_options[selected_benchmark]

    with col3:
        time_period = st.selectbox(
            "Time Period",
            [
                "1d", "5d", "1wk", "1mo", "3mo", "6mo",
                "1y", "2y", "5y", "10y", "ytd", "max"
            ],
            index=9,  # "10y" is at index 9
            label_visibility="collapsed"
        )

    with col4:
        interval = st.selectbox(
            "Interval (yfinance)",
            [
                "1m", "2m", "5m", "15m", "30m", "60m", "90m",
                "1h", "1d", "5d", "1wk", "1mo", "3mo"
            ],
            index=8,  # "1d" is at index 8
            label_visibility="collapsed"
        )

    # React to any input changes - no button needed
    if asset_type.strip() == "":
        st.info("Please enter a ticker symbol to get started.")
        st.markdown("""
        ### Examples of supported tickers:
        - **Stocks**: AAPL, MSFT, GOOGL, TSLA, AMZN
        - **ETFs**: SPY, QQQ, VTI, VXUS, GLD
        - **Indices**: ^GSPC (S&P 500), ^IXIC (NASDAQ), ^DJI (Dow Jones)
        - **Crypto**: BTC-USD, ETH-USD, ADA-USD
        """)
    else:
        try:
            # Fetch price data
            ticker = asset_type.strip().upper()

            with st.spinner(f"Fetching data for {ticker}..."):
                # Fetch comprehensive data (OHLCV)
                comprehensive_data = fetch_comprehensive_data(ticker, period=time_period, interval=interval)
                
                # Extract just price data for existing calculations
                price_data = comprehensive_data[[ticker]]
                df = add_statistics(price_data, ticker)

                benchmark_data = fetch_benchmark_data(ticker=benchmark_ticker, period=time_period, interval=interval)

                # Merge benchmark data and comprehensive data into main dataframe
                df = df.join(benchmark_data, how='left')
                df = df.join(comprehensive_data.drop(columns=[ticker]), how='left')  # Don't duplicate price column

            if df.empty:
                st.error("No data found for the given ticker symbol and parameters.")
            else:
                
                # Display key metrics in cards
                if not df.empty:
                    latest_data = df.iloc[-1]
                    col1, col2, col3, col4, col5 = st.columns(5)
                    
                    with col1:
                        current_price = latest_data[ticker]
                        st.metric("Current Price", f"{current_price:.2f}")
                    
                    with col2:
                        # Fetch Trailing P/E ratio
                        trailing_pe = fetch_trailing_pe_ratio(ticker)
                        if trailing_pe is not None:
                            st.metric("Trailing P/E", f"{trailing_pe:.2f}")
                        else:
                            st.metric("Trailing P/E", "N/A")
                    
                    with col3:
                        # Fetch Forward P/E ratio
                        forward_pe = fetch_forward_pe_ratio(ticker)
                        if forward_pe is not None:
                            st.metric("Forward P/E", f"{forward_pe:.2f}")
                        else:
                            st.metric("Forward P/E", "N/A")
                    
                    with col4:
                        if 'Cumulative_Return' in df.columns:
                            total_return = latest_data['Cumulative_Return'] * 100
                            st.metric("Total Return", f"{total_return:.2f}%")
                    
                    with col5:
                        if 'Drawdown_From_High' in df.columns:
                            drawdown = latest_data['Drawdown_From_High'] * 100
                            st.metric("Current Drawdown", f"{drawdown:.2f}%")

                st.markdown('---')

                # Show a line chart of cumulative returns over time in plotly
                fig = go.Figure()
                
                # Add benchmark cumulative return line first (background)
                if 'benchmark_cumulative_return' in df.columns:
                    fig.add_trace(go.Scatter(
                        x=df.index, 
                        y=df['benchmark_cumulative_return'] * 100,  # Convert to percentage
                        mode='lines', 
                        name=f'Benchmark ({selected_benchmark}) Cumulative Return',
                        line=dict(color='rgba(128, 128, 128, 0.7)', width=2, dash='dot'),
                        opacity=0.8,
                        hovertemplate='<b>Date:</b> %{x}<br><b>Benchmark Return:</b> %{y:.2f}%<extra></extra>'
                    ))
                
                # Add ticker cumulative return line (foreground)
                if 'Cumulative_Return' in df.columns:
                    fig.add_trace(go.Scatter(
                        x=df.index, 
                        y=df['Cumulative_Return'] * 100,  # Convert to percentage
                        mode='lines', 
                        name=f'{ticker} Cumulative Return',
                        line=dict(color='#1f77b4', width=3),
                        hovertemplate=f'<b>Date:</b> %{{x}}<br><b>{ticker} Return:</b> %{{y:.2f}}%<extra></extra>'
                    ))
                
                # Add zero reference line
                fig.add_hline(
                    y=0,
                    line_dash="solid",
                    line_color="rgba(0, 0, 0, 0.3)",
                    line_width=1
                )
                
                fig.update_layout(
                    title=f'{ticker} vs {selected_benchmark} Cumulative Returns',
                    xaxis_title='Date',
                    yaxis_title='Cumulative Return (%)',
                    height=500,
                    yaxis=dict(
                        tickformat=".1f",
                        ticksuffix="%"
                    ),
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=1.02,
                        xanchor="right",
                        x=1
                    ),
                    hovermode='x unified'
                )
                st.plotly_chart(fig, width='stretch')

                st.markdown('---')

                # Show drawdown chart if data is available
                if 'Drawdown_From_High' in df.columns:
                    fig2 = go.Figure()
                    
                    # Create drawdown data (convert to percentage for better readability)
                    drawdown_pct = df['Drawdown_From_High'] * 100
                    drawdown_percentile = df['Drawdown_Percentile'] * 100
                    
                    # Define percentile thresholds programmatically
                    percentiles = [0.0, 0.05, 0.25, 0.50, 1.0]
                    zone_labels = ['Worst', 'Deep', 'Moderate', 'Normal']
                    zone_colors = [
                        'rgba(34, 197, 94, 0.15)',   # Green
                        'rgba(132, 204, 22, 0.15)',  # Light green  
                        'rgba(245, 158, 11, 0.15)',  # Orange
                        'rgba(220, 38, 38, 0.15)'    # Red
                    ]
                    legend_colors = [
                        'rgba(34, 197, 94, 0.8)',   # Green
                        'rgba(132, 204, 22, 0.8)',  # Light green
                        'rgba(245, 158, 11, 0.8)',  # Orange
                        'rgba(220, 38, 38, 0.8)'    # Red
                    ]
                    
                    # Calculate actual percentile values
                    percentile_values = [drawdown_pct.quantile(p) for p in percentiles]
                    
                    # Add horizontal rectangles for percentile zones
                    for i in range(len(percentiles) - 1):
                        y0 = percentile_values[i]
                        y1 = percentile_values[i + 1]
                        pct_low = percentiles[i] * 100
                        pct_high = percentiles[i + 1] * 100
                        
                        fig2.add_hrect(
                            y0=y0, y1=y1,
                            fillcolor=zone_colors[i],
                            line_width=0,
                            annotation_text=f"{zone_labels[i]} ({pct_low:.0f}-{pct_high:.0f}%)",
                            annotation_position="top left",
                            annotation=dict(font_size=10)
                        )
                    
                    # Add main drawdown line on top
                    fig2.add_trace(go.Scatter(
                        x=df.index,
                        y=drawdown_pct,
                        mode='lines',
                        name='Drawdown from High',
                        line=dict(color='#1f2937', width=2),
                        fill='tozeroy',
                        fillcolor='rgba(31, 41, 55, 0.1)',
                        hovertemplate='<b>Date:</b> %{x}<br><b>Drawdown:</b> %{y:.2f}%<br><b>Percentile:</b> %{customdata:.1f}%<extra></extra>',
                        customdata=drawdown_percentile
                    ))

                    # Add invisible traces for legend (percentile zones)
                    for i in range(len(percentiles) - 1):
                        pct_low = percentiles[i] * 100
                        pct_high = percentiles[i + 1] * 100
                        val_low = percentile_values[i]
                        val_high = percentile_values[i + 1]
                        
                        fig2.add_trace(go.Scatter(
                            x=[None], y=[None],
                            mode='markers',
                            marker=dict(size=12, color=legend_colors[i]),
                            name=f'{zone_labels[i]} ({pct_low:.0f}-{pct_high:.0f}%): {val_low:.1f}% to {val_high:.1f}%',
                            showlegend=True
                        ))

                    # Add horizontal reference lines at percentile boundaries
                    for i in range(1, len(percentiles) - 1):  # Skip first (0%) and last (100%)
                        level = percentile_values[i]
                        pct = percentiles[i] * 100
                        fig2.add_hline(
                            y=level,
                            line_dash="dash",
                            line_color="rgba(107, 114, 128, 0.6)",
                            line_width=1
                        )

                    fig2.update_layout(
                        title=f'{ticker} Drawdown from All-Time High (Percentile Zones)',
                        xaxis_title='Date',
                        yaxis_title='Drawdown (%)',
                        height=500,
                        yaxis=dict(
                            tickformat=".1f",
                            ticksuffix="%"
                        ),
                        showlegend=True,
                        hovermode='x unified',
                        legend=dict(
                            orientation="h",
                            yanchor="bottom",
                            y=1.02,
                            xanchor="right",
                            x=1
                        )
                    )
                    
                    st.plotly_chart(fig2, width='stretch')

                st.markdown('---')

                # Volume chart with moving averages
                if 'Volume' in df.columns:
                    
                    # Calculate volume moving averages
                    df['Volume_MA_20'] = df['Volume'].rolling(window=20).mean()
                    df['Volume_MA_50'] = df['Volume'].rolling(window=50).mean()
                    
                    fig_volume = go.Figure()
                    
                    # Add volume bars
                    fig_volume.add_trace(go.Bar(
                        x=df.index,
                        y=df['Volume'],
                        name='Volume',
                        marker_color='rgba(31, 119, 180, 0.6)',
                        hovertemplate='<b>Date:</b> %{x}<br><b>Volume:</b> %{y:,.0f}<extra></extra>'
                    ))
                    
                    # Add volume moving averages
                    fig_volume.add_trace(go.Scatter(
                        x=df.index,
                        y=df['Volume_MA_20'],
                        mode='lines',
                        name='20-day MA',
                        line=dict(color='orange', width=2),
                        hovertemplate='<b>Date:</b> %{x}<br><b>20-day MA:</b> %{y:,.0f}<extra></extra>'
                    ))
                    
                    fig_volume.add_trace(go.Scatter(
                        x=df.index,
                        y=df['Volume_MA_50'],
                        mode='lines',
                        name='50-day MA',
                        line=dict(color='red', width=2),
                        hovertemplate='<b>Date:</b> %{x}<br><b>50-day MA:</b> %{y:,.0f}<extra></extra>'
                    ))
                    
                    fig_volume.update_layout(
                        title=f'{ticker} Trading Volume with Moving Averages',
                        xaxis_title='Date',
                        yaxis_title='Volume',
                        height=400,
                        yaxis=dict(tickformat=".2s"),
                        legend=dict(
                            orientation="h",
                            yanchor="bottom",
                            y=1.02,
                            xanchor="right",
                            x=1
                        ),
                        hovermode='x unified'
                    )
                    
                    st.plotly_chart(fig_volume, width='stretch')

                st.markdown('---')

                # Price chart with moving averages
                if ticker in df.columns:
                    
                    # Calculate price moving averages
                    df['MA_20'] = df[ticker].rolling(window=20).mean()
                    df['MA_50'] = df[ticker].rolling(window=50).mean()
                    df['MA_200'] = df[ticker].rolling(window=200).mean()
                    
                    fig_ma = go.Figure()
                    
                    # Add price line
                    fig_ma.add_trace(go.Scatter(
                        x=df.index,
                        y=df[ticker],
                        mode='lines',
                        name=f'{ticker} Price',
                        line=dict(color='#1f77b4', width=2),
                        hovertemplate=f'<b>Date:</b> %{{x}}<br><b>{ticker}:</b> $%{{y:.2f}}<extra></extra>'
                    ))
                    
                    # Add moving averages
                    ma_configs = [
                        ('MA_20', '20-day MA', 'orange'),
                        ('MA_50', '50-day MA', 'red'),
                        ('MA_200', '200-day MA', 'purple')
                    ]
                    
                    for ma_col, ma_name, color in ma_configs:
                        if ma_col in df.columns:
                            fig_ma.add_trace(go.Scatter(
                                x=df.index,
                                y=df[ma_col],
                                mode='lines',
                                name=ma_name,
                                line=dict(color=color, width=1.5),
                                hovertemplate=f'<b>Date:</b> %{{x}}<br><b>{ma_name}:</b> $%{{y:.2f}}<extra></extra>'
                            ))
                    
                    fig_ma.update_layout(
                        title=f'{ticker} Price with Moving Averages',
                        xaxis_title='Date',
                        yaxis_title='Price ($)',
                        height=500,
                        yaxis=dict(tickformat=".2f"),
                        legend=dict(
                            orientation="h",
                            yanchor="bottom",
                            y=1.02,
                            xanchor="right",
                            x=1
                        ),
                        hovermode='x unified'
                    )
                    
                    st.plotly_chart(fig_ma, width='stretch')

                st.markdown('---')

                # Volatility analysis
                
                # Calculate rolling volatility (annualized)
                returns = df[ticker].pct_change().dropna()
                df['Volatility_30d'] = returns.rolling(window=30).std() * (252 ** 0.5) * 100  # Annualized volatility in %
                df['Volatility_60d'] = returns.rolling(window=60).std() * (252 ** 0.5) * 100
                
                fig_vol = go.Figure()
                
                # Add volatility lines
                fig_vol.add_trace(go.Scatter(
                    x=df.index,
                    y=df['Volatility_30d'],
                    mode='lines',
                    name='30-day Volatility',
                    line=dict(color='#1f77b4', width=2),
                    hovertemplate='<b>Date:</b> %{x}<br><b>30-day Vol:</b> %{y:.1f}%<extra></extra>'
                ))
                
                fig_vol.add_trace(go.Scatter(
                    x=df.index,
                    y=df['Volatility_60d'],
                    mode='lines',
                    name='60-day Volatility',
                    line=dict(color='orange', width=2),
                    hovertemplate='<b>Date:</b> %{x}<br><b>60-day Vol:</b> %{y:.1f}%<extra></extra>'
                ))
                
                fig_vol.update_layout(
                    title=f'{ticker} Rolling Volatility (Annualized)',
                    xaxis_title='Date',
                    yaxis_title='Volatility (%)',
                    height=400,
                    yaxis=dict(
                        tickformat=".1f",
                        ticksuffix="%"
                    ),
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=1.02,
                        xanchor="right",
                        x=1
                    ),
                    hovermode='x unified'
                )
                
                st.plotly_chart(fig_vol, width='stretch')

                st.markdown('---')

                # Performance comparison table
                
                # Calculate performance metrics for different periods
                # Adjust period calculations based on the selected interval
                if interval in ['1d']:
                    # Daily data - use standard trading day counts
                    periods = {
                        '1M': 21,
                        '3M': 63,
                        '6M': 126,
                        '1Y': 252,
                        'YTD': None,
                        'Total': len(df)
                    }
                    annualization_factor = 252  # Trading days per year
                elif interval in ['1wk', '5d']:
                    # Weekly data - use weekly counts
                    periods = {
                        '1M': 4,    # ~4 weeks
                        '3M': 13,   # ~13 weeks
                        '6M': 26,   # ~26 weeks
                        '1Y': 52,   # ~52 weeks
                        'YTD': None,
                        'Total': len(df)
                    }
                    annualization_factor = 52  # Weeks per year
                elif interval in ['1mo']:
                    # Monthly data - use monthly counts
                    periods = {
                        '1M': 1,    # 1 month
                        '3M': 3,    # 3 months
                        '6M': 6,    # 6 months
                        '1Y': 12,   # 12 months
                        'YTD': None,
                        'Total': len(df)
                    }
                    annualization_factor = 12  # Months per year
                else:
                    # For other intervals (intraday), use a reasonable approximation
                    # Convert based on how many periods per day
                    if interval in ['1h', '60m']:
                        periods_per_day = 24
                    elif interval in ['30m']:
                        periods_per_day = 48
                    elif interval in ['15m']:
                        periods_per_day = 96
                    elif interval in ['5m']:
                        periods_per_day = 288
                    elif interval in ['1m']:
                        periods_per_day = 1440
                    else:
                        periods_per_day = 24  # Default assumption
                    
                    periods = {
                        '1M': 21 * periods_per_day,
                        '3M': 63 * periods_per_day,
                        '6M': 126 * periods_per_day,
                        '1Y': 252 * periods_per_day,
                        'YTD': None,
                        'Total': len(df)
                    }
                    annualization_factor = 252 * periods_per_day  # Periods per year
                
                perf_data = []
                
                for period_name, days in periods.items():
                    try:
                        if period_name == 'YTD':
                            # Year-to-date calculation
                            current_year = df.index[-1].year
                            ytd_data = df[df.index.year == current_year]
                            if len(ytd_data) > 1:
                                ticker_return = (ytd_data[ticker].iloc[-1] / ytd_data[ticker].iloc[0] - 1) * 100
                                if 'benchmark' in ytd_data.columns:
                                    benchmark_return = (ytd_data['benchmark'].iloc[-1] / ytd_data['benchmark'].iloc[0] - 1) * 100
                                    benchmark_vol = ytd_data['benchmark'].pct_change().std() * (annualization_factor ** 0.5) * 100
                                else:
                                    benchmark_return = None
                                    benchmark_vol = None
                                
                                ticker_vol = ytd_data[ticker].pct_change().std() * (annualization_factor ** 0.5) * 100
                                
                                period_data = ytd_data
                        elif days and days <= len(df):
                            period_data = df.tail(days)
                            ticker_return = (period_data[ticker].iloc[-1] / period_data[ticker].iloc[0] - 1) * 100
                            if 'benchmark' in period_data.columns:
                                benchmark_return = (period_data['benchmark'].iloc[-1] / period_data['benchmark'].iloc[0] - 1) * 100
                                benchmark_vol = period_data['benchmark'].pct_change().std() * (annualization_factor ** 0.5) * 100
                            else:
                                benchmark_return = None
                                benchmark_vol = None
                            
                            ticker_vol = period_data[ticker].pct_change().std() * (annualization_factor ** 0.5) * 100
                        elif period_name == 'Total':
                            period_data = df
                            ticker_return = (period_data[ticker].iloc[-1] / period_data[ticker].iloc[0] - 1) * 100
                            if 'benchmark' in period_data.columns:
                                benchmark_return = (period_data['benchmark'].iloc[-1] / period_data['benchmark'].iloc[0] - 1) * 100
                                benchmark_vol = period_data['benchmark'].pct_change().std() * (annualization_factor ** 0.5) * 100
                            else:
                                benchmark_return = None
                                benchmark_vol = None
                            
                            ticker_vol = period_data[ticker].pct_change().std() * (annualization_factor ** 0.5) * 100
                        else:
                            continue
                        
                        # Calculate Sharpe ratio (assuming 0% risk-free rate)
                        ticker_returns = period_data[ticker].pct_change().dropna()
                        if len(ticker_returns) > 0 and ticker_vol > 0:
                            sharpe_ratio = (ticker_returns.mean() * annualization_factor) / (ticker_vol / 100)
                        else:
                            sharpe_ratio = None
                        
                        # Calculate benchmark Sharpe ratio
                        if 'benchmark' in period_data.columns and benchmark_vol is not None and benchmark_vol > 0:
                            benchmark_returns = period_data['benchmark'].pct_change().dropna()
                            if len(benchmark_returns) > 0:
                                benchmark_sharpe = (benchmark_returns.mean() * annualization_factor) / (benchmark_vol / 100)
                            else:
                                benchmark_sharpe = None
                        else:
                            benchmark_sharpe = None
                        
                        perf_data.append({
                            'Period': period_name,
                            f'{ticker} Return (%)': f"{ticker_return:.2f}%",
                            f'Benchmark Return (%)': f"{benchmark_return:.2f}%" if benchmark_return is not None else "N/A",
                            f'{ticker} Volatility (%)': f"{ticker_vol:.2f}%",
                            f'Benchmark Volatility (%)': f"{benchmark_vol:.2f}%" if benchmark_vol is not None else "N/A",
                            f'{ticker} Sharpe Ratio': f"{sharpe_ratio:.2f}" if sharpe_ratio is not None else "N/A",
                            f'Benchmark Sharpe Ratio': f"{benchmark_sharpe:.2f}" if benchmark_sharpe is not None else "N/A"
                        })
                    
                    except (IndexError, KeyError):
                        continue
                
                if perf_data:
                    perf_df = pd.DataFrame(perf_data)
                    st.dataframe(perf_df, width='stretch', hide_index=True)

                st.markdown('---')


                # Put complete dataframe in a collapsible container
                with st.expander("📊 Data Table", expanded=False):
                    st.dataframe(df, width='stretch')

        except Exception as e:
            st.error(f"An error occurred while fetching data for {ticker}: {str(e)}")
            st.info("Please check if the ticker symbol is valid and try again.")

if __name__ == "__main__":
    main()