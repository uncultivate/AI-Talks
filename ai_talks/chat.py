from pathlib import Path
from random import randrange
import streamlit as st
from src.styles.menu_styles import FOOTER_STYLES, HEADER_STYLES
from src.utils.conversation import show_conversation, show_chat_buttons, show_conversation2, show_conversation3, clear_chat
from src.utils.lang import en
from streamlit_option_menu import option_menu
import streamlit as st
import matplotlib.pyplot as plt
#import matplotlib.dates as mdates
import pandas as pd
import numpy as np
import random
import math
import time

# --- PATH SETTINGS ---
current_dir: Path = Path(__file__).parent if "__file__" in locals() else Path.cwd()
css_file: Path = current_dir / "src/styles/.css"
assets_dir: Path = current_dir / "assets"
icons_dir: Path = assets_dir / "icons"
img_dir: Path = assets_dir / "img"
tg_svg: Path = icons_dir / "tg.svg"

# --- GENERAL SETTINGS ---
PAGE_TITLE: str = "Do what is necessary"
PAGE_ICON: str = "💸"
LANG_EN: str = "En"
AI_MODEL_OPTIONS: list[str] = [
    "gpt-3.5-turbo",
    "gpt-4",
    "gpt-4-32k",
]

st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON)

# --- LOAD CSS ---
with open(css_file) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Storing The Context
if "locale" not in st.session_state:
    st.session_state.locale = en
if "generated" not in st.session_state:
    st.session_state.generated = []
if "past" not in st.session_state:
    st.session_state.past = []
if "messages" not in st.session_state:
    st.session_state.messages = []
if "user_text" not in st.session_state:
    st.session_state.user_text = ""
if "input_kind" not in st.session_state:
    st.session_state.input_kind = st.session_state.locale.input_kind_1
if "seed" not in st.session_state:
    st.session_state.seed = randrange(10**3)  # noqa: S311
if "costs" not in st.session_state:
    st.session_state.costs = []
if "total_tokens" not in st.session_state:
    st.session_state.total_tokens = []



# Initialize session state variables if they don't exist
if 'news' not in st.session_state:
    st.session_state.news = [
        "Shockwaves in Canberra: New Reserve Bank Governor Appointed! But Are They Ready to Steer Australia's Economy?",
        "Corporate Blues: Businesses Grapple with Profit Downturn Amid Economic Uncertainty",
        "Job Market Volatility: Unemployment Spikes to 4% in a Month, Caution Sweeps the Workforce"
        ]
if 'model' not in st.session_state:
    st.session_state.model = "gpt-3.5-turbo"
if'count' not in st.session_state:
    st.session_state.count = 1
if 'confirmed' not in st.session_state:
    st.session_state.confirmed = False
if 'meeting' not in st.session_state:
    st.session_state.meeting = False
if 'newsprint' not in st.session_state:
    st.session_state.newsprint = False
if 'interest_rate' not in st.session_state:
    st.session_state['interest_rate'] = 3.0  # initial value

if 'gdp' not in st.session_state:
    st.session_state['gdp'] = 2.0  # initial value

if 'inflation' not in st.session_state:
    st.session_state['inflation'] = 3.4  # initial value

if 'govt_debt' not in st.session_state:
    st.session_state['govt_debt'] = 897000000000  # initial value

if 'unemployment' not in st.session_state:
    st.session_state['unemployment'] = 4.2  # initial value

if 'house_prices' not in st.session_state:
    st.session_state['house_prices'] = 920000  # initial value

if 'consumer_sentiment' not in st.session_state:
    st.session_state['consumer_sentiment'] = 50 # initial value

if 'imports' not in st.session_state:
    st.session_state['imports'] = 123000000000 # initial value

if 'exports' not in st.session_state:
    st.session_state['exports'] = 153000000000 # initial value

if 'asx_200' not in st.session_state:
    st.session_state['asx_200'] = 7012.12 # initial value


if 'prev_interest_rate' not in st.session_state:
    st.session_state['prev_interest_rate'] = 3.0  # initial value for previous GDP growth

if 'prev_gdp' not in st.session_state:
    st.session_state['prev_gdp'] = 2.0  # initial value for previous GDP growth

if 'prev_govt_debt' not in st.session_state:
    st.session_state['prev_govt_debt'] = 897000000000  # initial value

if 'prev_inflation' not in st.session_state:
    st.session_state['prev_inflation'] = 3.4  # initial value for previous inflation rate

if 'prev_unemployment' not in st.session_state:
    st.session_state['prev_unemployment'] = 4.2  # initial value for previous GDP growth

if 'prev_house_prices' not in st.session_state:
    st.session_state['prev_house_prices'] = 920000  # initial value for previous inflation rate

if 'prev_consumer_sentiment' not in st.session_state:
    st.session_state['prev_consumer_sentiment'] = 50 # initial value

if 'prev_imports' not in st.session_state:
    st.session_state['prev_imports'] = 50 # initial value

if 'prev_exports' not in st.session_state:
    st.session_state['prev_exports'] = 50 # initial value

if 'prev_asx_200' not in st.session_state:
    st.session_state['prev_asx_200'] = 6821 # initial value

if 'gdp_change' not in st.session_state:
    st.session_state['gdp_change'] =  -0.2
if 'inflation_change' not in st.session_state:    
    st.session_state['inflation_change'] =  0.3
if 'f_govt_debt' not in st.session_state:
    st.session_state['f_govt_debt'] = '$897 bn'
if 'f_govt_debt_change' not in st.session_state:
    st.session_state['f_govt_debt_change'] = '17 bn'
if 'govt_debt_change' not in st.session_state:    
    st.session_state['govt_debt_change'] = '$17 bn'
if 'unemployment_change' not in st.session_state:    
    st.session_state['unemployment_change'] =  0.3
if 'house_prices_change' not in st.session_state:    
    st.session_state['house_prices_change'] = '-$10,000'
if 'f_house_prices' not in st.session_state:
    st.session_state['f_house_prices'] = '$920,000'
if 'f_house_prices_change' not in st.session_state:
    st.session_state['f_house_prices_change'] = '10,000'
if 'consumer_sentiment_change' not in st.session_state:
    st.session_state['consumer_sentiment_change'] = -5
if 'imports_change' not in st.session_state:
    st.session_state['imports_change'] = "$5 bn" 
if 'f_imports' not in st.session_state:
    st.session_state['f_imports'] = '$123 bn'
if 'f_imports_change' not in st.session_state:
    st.session_state['f_imports_change'] = '5 bn'
if 'exports_change' not in st.session_state:
    st.session_state['exports_change'] = "$7 bn" 
if 'f_exports' not in st.session_state:
    st.session_state['f_exports'] = '$153 bn'
if 'f_exports_change' not in st.session_state:
    st.session_state['f_exports_change'] = '7 bn'
if 'asx_200_change' not in st.session_state:
    st.session_state['asx_200_change'] = 191.12





lower_fifty_factor = random.uniform(-0.5, 2)
lower_twentyfive_factor = random.uniform(-0.5, 1.5)
keepsame_factor = random.uniform(-0.5, 0.5)
raise_fifty_factor = random.uniform(-2, 1)
raise_twentyfive_factor = random.uniform(-1.5, 1)




st.sidebar.metric("Current Interest Rate", f"{st.session_state['interest_rate']}%", delta=st.session_state['interest_rate'] - st.session_state['prev_interest_rate'], delta_color="off")

st.sidebar.header("Actions")

def raise_50():
    st.session_state['count'] = st.session_state['count'] + 1
    st.session_state.newsprint = False
    st.session_state.confirmed = True
    st.session_state['interest_rate'] += 0.50   
    st.session_state['gdp'] -= 0.2 * raise_fifty_factor
    st.session_state['inflation'] -= 0.1 * raise_fifty_factor
    st.session_state['govt_debt'] = st.session_state['govt_debt'] * (1 + raise_fifty_factor/20)
    st.session_state['unemployment'] += 0.2 * raise_fifty_factor
    st.session_state['house_prices'] = st.session_state['house_prices'] * (1 + raise_fifty_factor/10)
    st.session_state['consumer_sentiment'] += 2 * raise_fifty_factor
    st.session_state['imports'] = st.session_state['imports'] * (1 + raise_fifty_factor/10)
    st.session_state['exports'] = st.session_state['exports'] * (1 + lower_fifty_factor/10)
    st.session_state['asx_200'] = st.session_state['asx_200'] * (1 + raise_fifty_factor/10)  

def raise_25():  
    st.session_state['count'] = st.session_state['count'] + 1
    st.session_state.newsprint = False
    st.session_state.confirmed = True
    st.session_state['interest_rate'] += 0.25
    st.session_state['gdp'] -= 0.2 * raise_twentyfive_factor
    st.session_state['inflation'] -= 0.1 * raise_twentyfive_factor
    st.session_state['unemployment'] += 0.2 * raise_twentyfive_factor
    st.session_state['house_prices'] = st.session_state['house_prices'] * (1 + raise_twentyfive_factor/10)
    st.session_state['consumer_sentiment'] += 1.5 * raise_twentyfive_factor
    st.session_state['govt_debt'] = st.session_state['govt_debt'] * (1 + raise_twentyfive_factor/20)
    st.session_state['imports'] = st.session_state['imports'] * (1 + raise_twentyfive_factor/10)
    st.session_state['exports'] = st.session_state['exports'] * (1 + lower_twentyfive_factor/10)
    st.session_state['asx_200'] = st.session_state['asx_200'] * (1 + raise_twentyfive_factor/10)

def koh():
    st.session_state['count'] = st.session_state['count'] + 1
    st.session_state.newsprint = False
    st.session_state.confirmed = True
    st.session_state['gdp'] += keepsame_factor
    st.session_state['inflation'] += keepsame_factor
    st.session_state['unemployment'] += keepsame_factor
    st.session_state['house_prices'] = st.session_state['house_prices'] * (1 + keepsame_factor/10)
    st.session_state['consumer_sentiment'] += keepsame_factor*10
    st.session_state['govt_debt'] = st.session_state['govt_debt'] * (1 + keepsame_factor/10)
    st.session_state['imports'] = st.session_state['imports'] * (1 + keepsame_factor/10)
    st.session_state['asx_200'] = st.session_state['asx_200'] * (1 + keepsame_factor/10)

def lower_25():
    st.session_state['count'] = st.session_state['count'] + 1
    st.session_state.newsprint = False
    st.session_state.confirmed = True
    st.session_state['interest_rate'] -= 0.25
    st.session_state['gdp'] += 0.2 * lower_twentyfive_factor
    st.session_state['inflation'] += 0.1 * lower_twentyfive_factor
    st.session_state['unemployment'] -= 0.2 * lower_twentyfive_factor
    st.session_state['house_prices'] = st.session_state['house_prices'] * (1 + lower_twentyfive_factor/10)
    st.session_state['consumer_sentiment'] += 1 * lower_twentyfive_factor
    st.session_state['govt_debt'] = st.session_state['govt_debt'] * (1 + lower_twentyfive_factor/20)
    st.session_state['imports'] = st.session_state['imports'] * (1 + lower_twentyfive_factor/10)
    st.session_state['exports'] = st.session_state['exports'] * (1 + raise_twentyfive_factor/10)
    st.session_state['asx_200'] = st.session_state['asx_200'] * (1 + lower_twentyfive_factor/10)   

def lower_50():
    st.session_state['count'] = st.session_state['count'] + 1
    st.session_state.newsprint = False
    st.session_state.confirmed = True
    st.session_state['interest_rate'] -= 0.50
    st.session_state['gdp'] += 0.2 * lower_fifty_factor
    st.session_state['inflation'] += 0.1 * lower_fifty_factor
    st.session_state['govt_debt'] = st.session_state['govt_debt'] * (1 + lower_fifty_factor/20)
    st.session_state['unemployment'] -= 0.2 * lower_fifty_factor
    st.session_state['house_prices'] = st.session_state['house_prices'] * (1 + lower_fifty_factor/10)
    st.session_state['consumer_sentiment'] += 2 * lower_fifty_factor
    st.session_state['imports'] = st.session_state['imports'] * (1 + lower_fifty_factor/10)
    st.session_state['exports'] = st.session_state['exports'] * (1 + raise_fifty_factor/10)
    st.session_state['asx_200'] = st.session_state['asx_200'] * (1 + lower_fifty_factor/10)

st.sidebar.button("Raise 50 points", on_click=raise_50, type="primary")
st.sidebar.button("Raise 25 points", on_click=raise_25, type="primary")
st.sidebar.button("Keep on hold", on_click=koh, type="secondary")
st.sidebar.button("Lower 25 points", on_click=lower_25, type="primary")
st.sidebar.button("Lower 50 points", on_click=lower_50, type="primary")


# Creating a Python list to represent the major, wacky, or unforeseen world events and their economic impacts
major_events = [
    [
        "Aliens Make First Contact with Earth! Increased spending on defense and research could significantly impact debt levels.",
        "govt_debt",
        1.5

    ],
    [
        "Elixir of Immortality Discovered! Increased life expectancy could lead to higher demand for housing, pushing prices up.",
        "house_prices",
        1.5
    ],
    [
        "Massive Solar Flare Wipes Out All Electronics! Severe crashes expected due to operational disruptions.",
        "asx_200",
        0.5
    ],
    [
        "Global Pandemic Even Worse Than COVID-19 Strikes! Significant rise in job losses across sectors expected.",
        "unemployment",
        3
    ],
    [
        "Limitless Clean Energy Source Unearthed! Costs to fall as energy costs plummet.",
        "inflation",
        0.75
    ],
    [
        "AI Gains Consciousness: Rise of the Machines! Fear about AI's role in society could affect spending.",
        "consumer_sentiment",
        0.5
    ],
    [
        "Chinese Yuan Collapses Overnight! Exports to plunge.",
        "exports",
        0.5
    ],
    [
        "Month-long Global Internet Shutdown: Back to the Stone Age! Companies forecast a massive drop in productivity and digital commerce.",
        "gdp",
        0.5
    ],
    [
        "United States and European Union Merge into Single Nation! Stock market uncertainty leading to short-term volatility, potential long-term gains.",
        "asx_200",
        1.3
    ],
    [
        "Time Travelers Arrive with Future Knowledge! The potential for economic forecasting could change debt management strategies.",
        "govt_debt",
        0.75
    ]
]


st.sidebar.divider()
st.sidebar.header('Quantitative Easing')
st.sidebar.write('Increase the money supply by purchasing longer-term securities from the open market to encourage borrowing, investment, and spending')
qe_action = st.sidebar.slider("Asset Purchases Amount ($Bn)", 0, 1000, 0)
st.image('ai_talks/assets/img/boardroom.jpg')
st.title("The Chair")
st.subheader(f'Month {st.session_state.count}')




if st.session_state.confirmed == True:
    # Initiate session state values for metric changes
    st.session_state['gdp_change'] =  f"{round(st.session_state['gdp'] - st.session_state['prev_gdp'],2)}%"
    st.session_state['inflation_change'] =  f"{round(st.session_state['inflation'] - st.session_state['prev_inflation'],2)}%"
    st.session_state['govt_debt_change'] = st.session_state['govt_debt'] - st.session_state['prev_govt_debt']
    st.session_state['unemployment_change'] =  f"{round(st.session_state['unemployment'] - st.session_state['prev_unemployment'],2)}%"
    st.session_state['house_prices_change'] = st.session_state['house_prices'] - st.session_state['prev_house_prices']
    st.session_state['consumer_sentiment_change'] =  f"{round(st.session_state['consumer_sentiment'] - st.session_state['prev_consumer_sentiment'],2)}%"
    st.session_state['imports_change'] = st.session_state['imports'] - st.session_state['prev_imports']
    st.session_state['exports_change'] = st.session_state['exports'] - st.session_state['prev_exports']
    st.session_state['asx_200_change'] =  st.session_state['asx_200'] - st.session_state['prev_asx_200']


    # Format monetary values prices
    st.session_state['f_house_prices'] = math.ceil(st.session_state['house_prices'] / 100) * 100
    st.session_state['f_house_prices_change'] = math.ceil(st.session_state['house_prices_change'] / 100) * 100

    st.session_state['f_house_prices'] = f"${st.session_state['f_house_prices']:,.0f}"
    st.session_state['f_house_prices_change'] = f"{st.session_state['f_house_prices_change']:,.0f}"

    st.session_state['f_govt_debt'] = round(st.session_state['govt_debt'] / 1e9)
    st.session_state['f_govt_debt_change'] = f"{round(st.session_state['govt_debt_change'] / 1e9)} bn"
    st.session_state['f_govt_debt'] = f"${int(st.session_state['f_govt_debt'])} bn" 

    st.session_state['f_imports'] = round(st.session_state['imports'] / 1e9)
    st.session_state['f_imports_change'] = f"{round(st.session_state['imports_change'] / 1e9)} bn"
    st.session_state['f_imports'] = f"${int(st.session_state['f_imports'])} bn" 

    st.session_state['f_exports'] = round(st.session_state['exports'] / 1e9)
    st.session_state['f_exports_change'] = f"{round(st.session_state['exports_change'] / 1e9)} bn"
    st.session_state['f_exports'] = f"${int(st.session_state['f_exports'])} bn" 

# Economic performance list for feeding into GPT
performance = [
    ["Economic Indicator: ASX 200",
    f"Current Value: {st.session_state['asx_200']}",
    f"Change in value from previous month: {st.session_state['asx_200_change']}"
    ],
    ["Economic Indicator: GDP",
    f"Current Value: {st.session_state['gdp']}",
    f"Change in value from previous month: {st.session_state['gdp_change']}"
    ],
    ["Economic Indicator: Inflation",
    f"Current Value: {st.session_state['inflation']}",
    f"Change in value from previous month: {st.session_state['inflation_change']}"
    ],
        ["Economic Indicator: Government Debt",
    f"Current Value: {st.session_state['govt_debt']}",
    f"Change in value from previous month: {st.session_state['govt_debt_change']}"
    ],
        ["Economic Indicator: Unemployment",
    f"Current Value: {st.session_state['unemployment']}",
    f"Change in value from previous month: {st.session_state['unemployment_change']}"
    ],
        ["Economic Indicator: House Prices",
    f"Current Value: {st.session_state['house_prices']}",
    f"Change in value from previous month: {st.session_state['house_prices_change']}"
    ],
        ["Economic Indicator: Imports",
    f"Current Value: {st.session_state['imports']}",
    f"Change in value from previous month: {st.session_state['imports_change']}"
    ],
        ["Economic Indicator: Exports",
    f"Current Value: {st.session_state['exports']}",
    f"Change in value from previous month: {st.session_state['exports_change']}"
    ],
        ["Economic Indicator: Consumer Sentiment",
    f"Current Value: {st.session_state['consumer_sentiment']}",
    f"Change in value from previous month: {st.session_state['consumer_sentiment_change']}"
    ]
]

if st.session_state['prev_interest_rate'] == st.session_state['interest_rate']:
    decision = 'hold'
elif st.session_state['prev_interest_rate'] < st.session_state['interest_rate']:
    decision = 'hike'
else:
    decision = 'lower'

st.header("Recent News Headlines:")
np1 = "Tabloid newspaper with catchy headlines"
np2 = "Local area newspaper"
np3 = "The Daily Mail, full of salacious gossip"
np4 = "The Financial Review"
angle1 = f"The reserve bank's recent decision to {decision} interest rates"
angle2 = f"Criticism of the Reserve Bank Governor by a senior government minister"

if st.session_state.newsprint == False and st.session_state.confirmed == True and st.session_state.count > 1:
    st.session_state.news = []
    show_conversation3(np1, performance)
    show_conversation3(np2, performance)
    show_conversation3(np3, performance, angle2)
    show_conversation3(np4, performance, angle1)
    st.session_state.newsprint = True

if st.session_state.count > 1: 
    st.info(st.session_state.news[0], icon="📰")
    time.sleep(0.3)
    st.info(st.session_state.news[1], icon="📰")
    time.sleep(0.3)
    st.info(st.session_state.news[2], icon="📰")
    time.sleep(0.3)
    st.info(st.session_state.news[3], icon="📰")
    time.sleep(0.3)
if st.session_state.count == 1:
    st.info(st.session_state.news[0], icon="📰")
    time.sleep(0.3)
    st.info(st.session_state.news[1], icon="📰")
    time.sleep(0.3)
    st.info(st.session_state.news[2], icon="📰")
    time.sleep(0.3)

if st.session_state.count == random.randint(2,12):
    rand_event = random.randint(0,9)
    st.warning(major_events[rand_event][0], icon="🌏")
    st.session_state[major_events[rand_event][1]] = st.session_state[major_events[rand_event][1]] * major_events[rand_event][2]




def main() -> None:
    # c1, c2 = st.columns(2)
    # with c1, c2:
    #     c1.selectbox(label=st.session_state.locale.select_placeholder1, key="model", options=AI_MODEL_OPTIONS)
    
    if st.session_state.meeting == False:
        st.write(f'Ready to convene the month {st.session_state.count} Reserve Bank board meeting?')
        if st.button(f'Call to Order', type="primary"):
            bm1 = "You are an eminent economist on the Reserve Bank Board. You need to make a recommendation to the governor in no more than 80 words whether to lower, hike or leave interest rates on hold. You speak obliquely with a technocratic tone."
            bm2 = "Take on a different persona with a different writing style. You are a business tycoon on the Reserve Bank Board. You need to make a recommendation to the governor in no more than 80 words whether to lower, hike or leave interest rates on hold. You speak directly with a callous tone"
            bm3 = "Take on a different persona with a different writing style. You are a compassionate advocate for families and workers on the Reserve Bank Board. You need to make a recommendation to the governor in no more than 80 words whether to lower, hike or leave interest rates on hold. You speak modestly with a sympathetic tone."

            show_conversation(bm1, performance)
            show_conversation2(bm2)
            show_conversation2(bm3)
            st.session_state.meeting = True
    if st.session_state.meeting == True:
        st.write("Board Member Milton Keynesian: Eminent Economist")
        st.session_state.generated[0]
        
        
        st.write("Board Member Clarissa Vanthorn: Business Tycoon")
        st.session_state.generated[1]
        
        
        
        st.write("Board Member Ella Fairbrook: Social Campaigner")
        st.session_state.generated[2]
        st.divider()
        st.write("Board meeting adjourned! Now the interest rates decision is in the Governor's hands alone.")

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

def run_agi():
    st.session_state.locale = en

    selected_footer = option_menu(
        menu_title=None,
        options=[
            st.session_state.locale.footer_option1,
            st.session_state.locale.footer_option0,
            st.session_state.locale.footer_option2,
        ],
        icons=["info-circle", "chat-square-text", "graph-up"],  # https://icons.getbootstrap.com/
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
        styles=FOOTER_STYLES
    )
    match selected_footer:
        case st.session_state.locale.footer_option0:
            main()
        case st.session_state.locale.footer_option1:
            m1, m2, m3 = st.columns((1,1,1))
            m1.metric("GDP Growth", value=f"{round(st.session_state['gdp'],2)}%", delta=st.session_state['gdp_change'])
            m2.metric("Inflation Rate", value=f"{round(st.session_state['inflation'],2)}%", delta=st.session_state['inflation_change'], delta_color="inverse")
            m3.metric("Government Debt", value=f"{st.session_state['f_govt_debt']}", delta=st.session_state['f_govt_debt_change'], delta_color="inverse")

            m4, m5, m6 = st.columns((1,1,1))
            m4.metric("National Mean House Price", value=f"{st.session_state['f_house_prices']}", delta=st.session_state['f_house_prices_change'])
            m5.metric("Unemployment Rate", value=f"{round(st.session_state['unemployment'],2)}%", delta=st.session_state['unemployment_change'], delta_color="inverse")
            m6.metric("Consumer Sentiment", value=f"{round(st.session_state['consumer_sentiment'],2)}%", delta=st.session_state['consumer_sentiment_change'])

            m7, m8, m9 = st.columns((1,1,1))
            m7.metric("Imports", value=f"{st.session_state['f_imports']}", delta=st.session_state['f_imports_change'])
            m8.metric("Exports", value=f"{st.session_state['f_exports']}", delta=st.session_state['f_exports_change'])
            m9.metric("Stock Market Index", value=round(st.session_state['asx_200'],2), delta=round(st.session_state['asx_200_change'],2))

        case st.session_state.locale.footer_option2:
            st.header('S&P / ASX 200')
            stock_dir = "Down" if st.session_state['asx_200_change'] < 0 else "Up"
            st.write(f"{stock_dir} {round(st.session_state['asx_200_change'],2)} points ({round(100*(1 - st.session_state['prev_asx_200']/st.session_state['asx_200']),2)}%) in the past month")
            plot_asx_200(st.session_state['asx_200'] - st.session_state['asx_200_change'], st.session_state['asx_200'], 1)




if __name__ == "__main__":
    run_agi()
    

# Update previous metrics for the next round
if st.session_state.confirmed:  
    st.session_state['prev_interest_rate'] = st.session_state['interest_rate']
    st.session_state['prev_gdp'] = st.session_state['gdp']
    st.session_state['prev_inflation'] = st.session_state['inflation']
    st.session_state['prev_govt_debt'] = st.session_state['govt_debt']
    st.session_state['prev_unemployment'] = st.session_state['unemployment']
    st.session_state['prev_house_prices'] = st.session_state['house_prices']
    st.session_state['prev_consumer_sentiment'] = st.session_state['consumer_sentiment']
    st.session_state['prev_imports'] = st.session_state['imports']
    st.session_state['prev_exports'] = st.session_state['exports']
    st.session_state['prev_asx_200'] = st.session_state['asx_200']
    st.session_state.meeting = False
    st.session_state.confirmed = False 
    clear_chat()  
