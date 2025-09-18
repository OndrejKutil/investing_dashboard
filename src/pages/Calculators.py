import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from helper.calc.portfolio_growth_calc import calculate_cumulative_growth, format_currency

tab1, tab2, tab3 = st.tabs(["Growth Calculator", "Calculator 2", "Calculator 3"])

with tab1:
    st.header("Portfolio Growth Calculator")
    st.markdown("Calculate how your investments will grow over time with regular contributions.")
    
    # Create columns for better layout
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Investment Parameters")
        
        # Starting balance
        starting_balance = st.number_input(
            "Initial Investment",
            min_value=0.0,
            value=10000.0,
            help="Your starting investment amount"
        )
        
        # Periodic contribution
        periodic_contribution = st.number_input(
            "Regular Contribution",
            min_value=0.0,
            value=500.0,
            help="Amount you plan to invest regularly"
        )
        
        # Contribution frequency
        contribution_frequency = st.selectbox(
            "Contribution Frequency",
            options=['monthly', 'quarterly', 'weekly', 'daily'],
            index=0,
            help="How often you plan to make contributions"
        )
        
        # Years to invest
        years = st.slider(
            "Investment Period (Years)",
            min_value=1,
            value=20,
            help="How long you plan to invest"
        )
        
        # Annual return
        annual_return = st.slider(
            "Expected Annual Return (%)",
            min_value=0.0,
            max_value=50.0,
            value=7.0,
            step=0.5,
            help="Expected annual return rate"
        ) / 100
        
        # Inflation settings
        st.subheader("Inflation Settings")
        
        include_inflation = st.checkbox(
            "Include Inflation Analysis",
            value=False,
            help="Factor in inflation for more realistic projections"
        )
        
        annual_inflation = 0.0
        inflation_adjust_contributions = False
        
        if include_inflation:
            annual_inflation = st.slider(
                "Annual Inflation Rate (%)",
                min_value=0.0,
                max_value=10.0,
                value=3.0,
                step=0.5,
                help="Expected annual inflation rate"
            ) / 100
            
            inflation_adjust_contributions = st.checkbox(
                "Adjust Contributions for Inflation",
                value=False,
                help="Increase contributions each year to maintain purchasing power"
            )
    
    # Calculate results
    try:
        results = calculate_cumulative_growth(
            starting_balance=starting_balance,
            periodic_contribution=periodic_contribution,
            contribution_frequency=contribution_frequency,
            years=years,
            annual_return=annual_return,
            annual_inflation=annual_inflation,
            inflation_adjust_contributions=inflation_adjust_contributions
        )
        
        # Extract data for visualization
        timeline_data = results['timeline']
        summary_data = results['summary']
        
        # Create DataFrame for easier plotting
        df = pd.DataFrame({
            'Years': timeline_data['years'],
            'Total Balance': timeline_data['balance'],
            'Contributions': timeline_data['contributions'],
            'Interest Earned': timeline_data['interest']
        })
        
        if include_inflation:
            df['Real Value Balance'] = timeline_data['real_value_balance']
        
    except Exception as e:
        st.error(f"Error in calculation: {str(e)}")
        st.stop()
    
    with col2:
        st.subheader("Growth Projection")
        
        # Create interactive chart
        fig = go.Figure()
        
        # Add traces for different components
        fig.add_trace(go.Scatter(
            x=df['Years'],
            y=df['Total Balance'],
            mode='lines',
            fill='tozeroy',
            name='Total Balance',
            line=dict(color='#1f77b4', width=3),
            fillcolor='rgba(31, 119, 180, 0.3)',
            hovertemplate='<b>Year %{x:.1f}</b><br>Total Balance: %{y:,.0f}<extra></extra>'
        ))
        
        fig.add_trace(go.Scatter(
            x=df['Years'],
            y=df['Contributions'],
            mode='lines',
            name='Total Contributions',
            line=dict(color='#ff7f0e', width=2),
            hovertemplate='<b>Year %{x:.1f}</b><br>Contributions: %{y:,.0f}<extra></extra>'
        ))
        
        fig.add_trace(go.Scatter(
            x=df['Years'],
            y=df['Interest Earned'],
            mode='lines',
            name='Interest Earned',
            line=dict(color='#2ca02c', width=2),
            hovertemplate='<b>Year %{x:.1f}</b><br>Interest: %{y:,.0f}<extra></extra>'
        ))
        
        # Add inflation-adjusted balance if inflation is included
        if include_inflation and annual_inflation > 0:
            fig.add_trace(go.Scatter(
                x=df['Years'],
                y=df['Real Value Balance'],
                mode='lines',
                name='Real Value (Inflation-Adjusted)',
                line=dict(color='#d62728', width=2, dash='dash'),
                hovertemplate='<b>Year %{x:.1f}</b><br>Real Value: %{y:,.0f}<extra></extra>'
            ))
        
        # Update layout
        fig.update_layout(
            title="Investment Growth Over Time",
            xaxis_title="Years",
            yaxis_title="Amount",
            hovermode='x unified',
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            ),
            height=500
        )
        
        # Format y-axis with commas
        fig.update_yaxes(tickformat=',.0f')
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Summary metrics section
    st.markdown("---")
    st.subheader("Summary Metrics")
    
    # Create metric columns
    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
    
    with metric_col1:
        st.metric(
            label="Final Balance",
            value=format_currency(summary_data['final_balance']),
            help="Total portfolio value after the investment period"
        )
    
    with metric_col2:
        st.metric(
            label="Total Contributions",
            value=format_currency(summary_data['total_contributed']),
            help="Total amount you will have contributed over the period"
        )
    
    with metric_col3:
        st.metric(
            label="Interest Earned",
            value=format_currency(summary_data['total_interest']),
            help="Total interest/growth earned on your investments"
        )
    
    with metric_col4:
        st.metric(
            label="Effective Annual Return",
            value=f"{summary_data['effective_annual_return']:.2%}",
            help="Your actual annualized return considering all contributions"
        )
    
    # Additional metrics if inflation is considered
    if include_inflation and annual_inflation > 0:
        st.markdown("### Inflation-Adjusted Analysis")
        
        inflation_col1, inflation_col2, inflation_col3 = st.columns(3)
        
        with inflation_col1:
            st.metric(
                label="Real Value (Today's Dollars)",
                value=format_currency(summary_data['final_real_value']),
                help="Final balance adjusted for inflation (purchasing power in today's dollars)"
            )
        
        with inflation_col2:
            purchasing_power_loss = summary_data['final_balance'] - summary_data['final_real_value']
            st.metric(
                label="Purchasing Power Lost to Inflation",
                value=format_currency(purchasing_power_loss),
                help="Amount of value lost due to inflation over the investment period"
            )
        
        with inflation_col3:
            real_growth_rate = ((summary_data['final_real_value'] / starting_balance) ** (1/years) - 1) if years > 0 else 0
            st.metric(
                label="Real Growth Rate (After Inflation)",
                value=f"{real_growth_rate:.2%}",
                help="Annualized growth rate after accounting for inflation"
            )
    
    # Investment breakdown chart
    st.markdown("### Investment Breakdown")
    
    # Create pie chart showing final composition
    breakdown_data = {
        'Component': ['Principal', 'Contributions', 'Interest Earned'],
        'Amount': [
            starting_balance,
            summary_data['total_contributed'] - starting_balance,
            summary_data['total_interest']
        ]
    }
    
    pie_fig = px.pie(
        values=breakdown_data['Amount'],
        names=breakdown_data['Component'],
        title=f"Final Portfolio Composition: {format_currency(summary_data['final_balance'])}",
        color_discrete_sequence=['#ff7f0e', '#1f77b4', '#2ca02c']
    )
    
    pie_fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hovertemplate='<b>%{label}</b><br>Amount: %{value:,.0f}<br>Percentage: %{percent}<extra></extra>'
    )
    
    st.plotly_chart(pie_fig, use_container_width=True)

with tab2:
    st.header("Calculator 2")
    st.write("Content for Calculator 2 goes here.")

with tab3:
    st.header("Calculator 3")
    st.write("Content for Calculator 3 goes here.")