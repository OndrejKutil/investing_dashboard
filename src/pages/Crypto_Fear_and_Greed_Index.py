import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from utils.theme import chart_background, FEAR_GREED_COLORS, TEXT_COLORS

from helper.data.fag_index_request import fetch_fear_and_greed_crypto_index

st.title("Crypto Fear and Greed Index")

time_options = ["1m", "3m", "6m", "1y", '5y', 'ytd', 'max']


selected_time = st.selectbox("Select Time Period", 
                             time_options,
                             index=3
                             )

with st.spinner("Loading..."):

    # calculate number of days
    if selected_time == "1m":
        days = 30
    elif selected_time == "3m":
        days = 90
    elif selected_time == "6m":
        days = 180
    elif selected_time == "1y":
        days = 365
    elif selected_time == "5y":
        days = 500
    elif selected_time == "ytd":
        days = (pd.Timestamp.now() - pd.Timestamp(year=pd.Timestamp.now().year, month=1, day=1)).days
    elif selected_time == "max":
        days = 500
    else:
        raise ValueError("Invalid time period selected.")

    df = fetch_fear_and_greed_crypto_index(limit=days)

# Get the latest value and previous value for the gauge chart
latest_value = df['fear_greed_index'].iloc[0]
latest_date = df['date'].iloc[0]

# Calculate delta if we have enough data points
if len(df) > 1:
    previous_value = df['fear_greed_index'].iloc[1]
    delta_value = latest_value - previous_value
else:
    previous_value = latest_value
    delta_value = 0

# Create gauge chart
gauge_fig = go.Figure(go.Indicator(
    mode = "gauge+number+delta",
    value = latest_value,
    delta = {
        'reference': previous_value,
        'increasing': {'color': FEAR_GREED_COLORS["greed"]}, 
        'decreasing': {'color': FEAR_GREED_COLORS["fear"]},
        'position': "bottom",
        'font': {'size': 16}
    },
    domain = {'x': [0, 1], 'y': [0, 1]},
    title = {'text': f"Current index value ({latest_date.strftime('%Y-%m-%d')})"},
    gauge = {
        'axis': {'range': [None, 100]},
        'bar': {'color': FEAR_GREED_COLORS["line"]},
        'steps': [
            {'range': [0, 20], 'color': FEAR_GREED_COLORS["extreme_fear"]},
            {'range': [20, 40], 'color': FEAR_GREED_COLORS["fear"]},
            {'range': [40, 60], 'color': FEAR_GREED_COLORS["neutral"]},
            {'range': [60, 80], 'color': FEAR_GREED_COLORS["greed"]},
            {'range': [80, 100], 'color': FEAR_GREED_COLORS["extreme_greed"]}
        ]
    }
))

gauge_fig.update_layout(
    height=400,
    font=dict(color=TEXT_COLORS["primary"]),
    **chart_background
)

# Display the gauge chart
st.plotly_chart(gauge_fig, use_container_width=True)

st.markdown('---')


fig = go.Figure()

fig.add_hrect(y0=0, y1=20, fillcolor=FEAR_GREED_COLORS["extreme_fear"], opacity=0.2, line_width=0, annotation_text="Extreme Fear", annotation_position="top left")
fig.add_hrect(y0=20, y1=40, fillcolor=FEAR_GREED_COLORS["fear"], opacity=0.1, line_width=0, annotation_text="Fear", annotation_position="top left")
fig.add_hrect(y0=40, y1=60, fillcolor=FEAR_GREED_COLORS["neutral"], opacity=0.1, line_width=0, annotation_text="Neutral", annotation_position="top left")
fig.add_hrect(y0=60, y1=80, fillcolor=FEAR_GREED_COLORS["greed"], opacity=0.1, line_width=0, annotation_text="Greed", annotation_position="top left")
fig.add_hrect(y0=80, y1=100, fillcolor=FEAR_GREED_COLORS["extreme_greed"], opacity=0.2, line_width=0, annotation_text="Extreme Greed", annotation_position="top left")

fig.add_trace(go.Scatter(x=df['date'], y=df['fear_greed_index'], mode='lines', name='Fear and Greed Index', line=dict(color=FEAR_GREED_COLORS["line"], width=2)))

fig.update_layout(title='Crypto Fear and Greed Index',
                  xaxis_title='Date',
                  yaxis_title='Index Value',
                  hovermode='x unified',
                  font=dict(color=TEXT_COLORS["primary"]),  # Light text for better visibility
                  **chart_background
                  )

st.plotly_chart(fig, use_container_width=True)

with st.expander("View DataFrame"):
    st.dataframe(df)
