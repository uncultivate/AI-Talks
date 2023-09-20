from pathlib import Path

import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
import random
import math


def show_info(icon: Path) -> None:

    st.header("Key Metrics")
 
    m1, m2, m3 = st.columns((1,1,1))
    m1.metric("GDP Growth", value=f"{round(st.session_state['gdp_growth'],2)}%", delta=gdp_change)
    m2.metric("Inflation Rate", value=f"{round(st.session_state['inflation_rate'],2)}%", delta=inflation_change)
    m3.metric("Unemployment Rate", value=f"{round(st.session_state['unemployment_rate'],2)}%", delta=unemployment_change)

    m4, m5, m6 = st.columns((1,1,1))
    m4.metric("National Mean Housing Price", value=f"{house_prices}", delta=housing_change)
    m5.metric("Government Debt", value=f"{govt_debt}", delta=govt_debt_change)



def show_charts() -> None:
    def plot_asx_200():
        dates = pd.date_range(end=pd.Timestamp.today(), periods=30, freq='D')
        start_value = 7000
        random_changes = np.random.normal(loc=0, scale=50, size=len(dates))
        asx_200_values = np.cumsum(random_changes) + start_value
        df = pd.DataFrame({'Date': dates, 'ASX 200': asx_200_values})
        direction = 'Down' if asx_200_values[0] > asx_200_values[-1] else 'Up'
        st.write(f"{direction} {round(asx_200_values[-1] - asx_200_values[0])} points ({round(1 - asx_200_values[0]/asx_200_values[-1],2)}%) in the past month")
        fig, ax = plt.subplots()

        # Set dark background
        ax.set_facecolor('none')  # Make the axis background transparent
        fig.patch.set_facecolor('none')  # Make the figure background transparent

        # Set text and line colors to light color for visibility against dark background
        ax.tick_params(axis='both', colors='white')
        ax.xaxis.label.set_color('white')
        ax.yaxis.label.set_color('white')
        ax.title.set_color('white')

        ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d %b'))

        ax.fill_between(df['Date'], df['ASX 200'], color="skyblue", alpha=0.4)
        ax.plot(df['Date'], df['ASX 200'], color="Slateblue", alpha=0.6)

        # Remove x-axis margins to extend the line to the sides of the chart
        ax.set_xlim(df['Date'].iloc[0], df['Date'].iloc[-1])
        plt.ylim(min(df['ASX 200']) - 50, max(df['ASX 200']) + 50)
        plt.grid(True)

        st.pyplot(fig)

    # Streamlit app
    st.title('S&P / ASX 200')
    plot_asx_200()

