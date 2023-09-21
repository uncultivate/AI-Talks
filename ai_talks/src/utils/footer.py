from pathlib import Path

import streamlit as st
import pandas as pd
import numpy as np
import random
import math
import plotly.graph_objects as go


def show_info(icon: Path) -> None:

    st.header("Key Metrics")
 
    m1, m2, m3 = st.columns((1,1,1))
    m1.metric("GDP Growth", value=f"{round(st.session_state['gdp_growth'],2)}%", delta=gdp_change)
    m2.metric("Inflation Rate", value=f"{round(st.session_state['inflation_rate'],2)}%", delta=inflation_change)
    m3.metric("Unemployment Rate", value=f"{round(st.session_state['unemployment_rate'],2)}%", delta=unemployment_change)

    m4, m5, m6 = st.columns((1,1,1))
    m4.metric("National Mean Housing Price", value=f"{house_prices}", delta=housing_change)
    m5.metric("Government Debt", value=f"{govt_debt}", delta=govt_debt_change)




def plot_asx_200(start_value, end_value, seed=None):
    # Set the random seed for reproducibility
    if seed is not None:
        np.random.seed(seed)
        
    dates = pd.date_range(end=pd.Timestamp.today(), periods=30, freq='D')
    
    # Generate random noise
    random_noise = np.random.normal(loc=0, scale=end_value/200, size=len(dates))
    
    # Create a series of changes that trend from the start_value to the end_value
    linear_trend = np.linspace(start_value, end_value, len(dates))
    
    # Add a sinusoidal wave to the linear trend
    wave_amplitude = end_value/100  # Amplitude of the wave
    wave_frequency = 2 * np.pi / 15  # Frequency of the wave, 2*pi/period
    sinusoidal_wave = wave_amplitude * np.sin(wave_frequency * np.arange(len(dates)))

    # Combine the linear trend, sinusoidal wave, and random noise
    asx_200_values = linear_trend + sinusoidal_wave + random_noise
    
    # Ensure the last value is exactly the end_value
    asx_200_values[-1] = end_value
    
    # Ensure the first value is exactly the start_value
    asx_200_values[0] = start_value
    
    df = pd.DataFrame({'Date': dates, 'ASX 200': asx_200_values})
        
    # Create Plotly Figure
    fig = go.Figure()

    # Add area plot
    fig.add_trace(go.Scatter(
        x=df['Date'],
        y=df['ASX 200'],
        mode='lines',
        line=dict(width=0.5, color='Slateblue'),
        stackgroup='one',
        fill='tozeroy',
        name='ASX 200 Area',
        showlegend=False 
    ))

    # Add line plot
    fig.add_trace(go.Scatter(
        x=df['Date'],
        y=df['ASX 200'],
        mode='lines',
        line=dict(color='Slateblue'),
        showlegend=False 
    ))



    y_min = min(df['ASX 200']) - 100
    y_max = max(df['ASX 200']) + 100
    # Customize layout
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        
        xaxis=dict(
            tickformat='%d %b',
            tickfont=dict(
                color='white'
            )
        ),
        margin=go.layout.Margin(
            l=0, #left margin
            r=0, #right margin
            b=0, #bottom margin
            t=0, #top margin
        ),
        yaxis=dict(
        range=[y_min, y_max],
        tickfont=dict(
            color='white'
        )
        
    )
    )
    # Display Plotly chart in Streamlit
    st.plotly_chart(fig)



