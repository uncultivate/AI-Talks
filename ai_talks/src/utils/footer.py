from pathlib import Path

import streamlit as st
import pandas as pd
import numpy as np
import random
import math
import plotly.graph_objects as go
from plotly.subplots import make_subplots


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
    random_noise = np.random.normal(loc=0, scale=end_value/random.randint(50,100), size=len(dates))
    
    # Create a series of changes that trend from the start_value to the end_value
    linear_trend = np.linspace(start_value, end_value, len(dates))
    
    # Add a sinusoidal wave to the linear trend
    wave_amplitude = (start_value - end_value)/random.randint(1,10)  # Amplitude of the wave
    wave_frequency = random.randint(1,3) / 10  # Frequency of the wave
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

# def plot_final(seed=None):
#     # Set the random seed for reproducibility
#     if seed is not None:
#         np.random.seed(seed)
                
#     # Create Plotly Figure
#     # Create subplots
#     fig = make_subplots(rows=9, cols=1, \
#                         subplot_titles=(
#                             'Cash Rate',
#                             'GDP',
#                             'Inflation',
#                             'Government Debt',
#                             'House Prices',
#                             'Unemployment Rate',
#                             'Consumer Sentiment',
#                             'Exports & Imports',
#                             'ASX 200'
#                         ))


#     # Add line plot
#     fig.add_trace(go.Scatter(y=st.session_state['interest_rate'], mode='lines', name="Cash Rate", line=dict(color='Slateblue'),
#         showlegend=False), row=1, col=1)
#     fig.add_trace(go.Scatter(y=st.session_state['gdp'], mode='lines', name="GDP", line=dict(color='Slateblue'),
#         showlegend=False), row=2, col=1)
#     fig.add_trace(go.Scatter(y=st.session_state['inflation'], mode='lines', name="Inflation", line=dict(color='Slateblue'),
#         showlegend=False), row=3, col=1)
#     fig.add_trace(go.Scatter(y=st.session_state['govt_debt'], mode='lines', name="Govt Debt", line=dict(color='Slateblue'),
#         showlegend=False), row=4, col=1)
#     fig.add_trace(go.Scatter(y=st.session_state['house_prices'], mode='lines', name="House Prices", line=dict(color='Slateblue'),
#         showlegend=False), row=5, col=1)
#     fig.add_trace(go.Scatter(y=st.session_state['unemployment'], mode='lines', name="Unemployment Rate", line=dict(color='Slateblue'),
#         showlegend=False), row=6, col=1)
#     fig.add_trace(go.Scatter(y=st.session_state['consumer_sentiment'], mode='lines', name="Consumer Sentiment", line=dict(color='Slateblue'),
#         showlegend=False), row=7, col=1)
#     fig.add_trace(go.Scatter(y=st.session_state['imports'], mode='lines', name="Imports", line=dict(color='Slateblue'),
#         showlegend=False), row=8, col=1)
#     fig.add_trace(go.Scatter(y=st.session_state['exports'], mode='lines', name="Exports", line=dict(color='lightsalmon'),
#         showlegend=False), row=8, col=1)
#     fig.add_trace(go.Scatter(y=st.session_state['asx_200'], mode='lines', name="ASX 200", line=dict(color='Slateblue'),
#         showlegend=False), row=9, col=1)
    

#     grid_color_rgba = 'rgba(200, 200, 200, 0.1)' 
#     fig.update_xaxes(range=[1, len(st.session_state.interest_rate)])  
#     fig.update_yaxes(showgrid=True, gridwidth=0.1, gridcolor=grid_color_rgba)   

#     # Customize layout
#     fig.update_layout(
#         plot_bgcolor='rgba(0,0,0,0)',
#         paper_bgcolor='rgba(0,0,0,0)',
        
#         xaxis=dict(
#             tickformat='%d %b',
#             tickfont=dict(
#                 color='white'
#             )
#         ),
#         margin=go.layout.Margin(
#             l=0, #left margin
#             r=0, #right margin
#             b=0, #bottom margin
#             t=30, #top margin
#         ),
#         yaxis=dict(

#         tickfont=dict(
#             color='white'
#         )
        
#     )
#     )
#     fig.update_layout(height=2300)

#     # Display Plotly chart in Streamlit
#     st.plotly_chart(fig)

def plot_chart(chart_name, y_data, row, color='Slateblue', name=None):
    fig = make_subplots(rows=1, cols=1, subplot_titles=(chart_name,))

    # Preprocess Y-data for specific charts
    if chart_name in ['Cash Rate', 'GDP', 'Inflation', 'Unemployment Rate']:
        y_data = [y / 100 for y in y_data]  # Divide by 100 for correct percentage scaling

    fig.add_trace(go.Scatter(y=y_data, mode='lines', name=name or chart_name, line=dict(color=color), showlegend=False), row=1, col=1)

    grid_color_rgba = 'rgba(200, 200, 200, 0.1)'
    fig.update_xaxes(range=[1, len(y_data)], tickformat='%d %b', title='Month')  # Added label 'Month' to X-axis
    fig.update_yaxes(showgrid=True, gridwidth=0.1, gridcolor=grid_color_rgba)

    # Format Y-axis as rounded percentage for specific charts
    if chart_name in ['Cash Rate', 'GDP', 'Inflation', 'Unemployment Rate']:
        fig.update_yaxes(showgrid=True, gridwidth=0.1, gridcolor=grid_color_rgba, tickformat='.0%')
    else:
        fig.update_yaxes(showgrid=True, gridwidth=0.1, gridcolor=grid_color_rgba)

    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=go.layout.Margin(l=0, r=0, b=0, t=30),
        xaxis=dict(tickfont=dict(color='white')),
        yaxis=dict(tickfont=dict(color='white'))
    )
    fig.update_layout(height=400)

    st.plotly_chart(fig)



def plot_final(seed=None):
    # Set the random seed for reproducibility
    if seed is not None:
        np.random.seed(seed)

    # Initialize or update the state variable for the currently selected chart
    if 'current_chart' not in st.session_state:
        st.session_state['current_chart'] = ('Cash Rate', st.session_state['interest_rate'], 1)

    # Define a function to update the current chart
    def update_chart(name, data, chart_number, color=None):
        st.session_state['current_chart'] = (name, data, chart_number, color)

    # Sidebar buttons for each chart
    chart_buttons = {
        'Cash Rate': ('Cash Rate', st.session_state['interest_rate'], 1),
        'GDP': ('GDP', st.session_state['gdp'], 2),
        'Inflation': ('Inflation', st.session_state['inflation'], 3),
        'Government Debt': ('Government Debt', st.session_state['govt_debt'], 4),
        'House Prices': ('House Prices', st.session_state['house_prices'], 5),
        'Unemployment Rate': ('Unemployment Rate', st.session_state['unemployment'], 6),
        'Consumer Sentiment': ('Consumer Sentiment', st.session_state['consumer_sentiment'], 7),
        'Exports': ('Exports', st.session_state['exports'], 8),
        'Imports': ('Imports', st.session_state['imports'], 8),
        'ASX 200': ('ASX 200', st.session_state['asx_200'], 9)
    }

    for button_name, chart_info in chart_buttons.items():
        if st.sidebar.button(button_name):
            update_chart(*chart_info)

    # Display the current chart
    plot_chart(*st.session_state['current_chart'])


