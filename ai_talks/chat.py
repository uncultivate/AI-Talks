from pathlib import Path
from random import randrange
import streamlit as st
from src.styles.menu_styles import FOOTER_STYLES, HEADER_STYLES
from src.utils.conversation import show_conversation, show_chat_buttons, show_conversation2, show_conversation3, clear_chat
from src.utils.lang import en
from src.utils.footer import plot_asx_200
from streamlit_option_menu import option_menu
import numpy as np
import pandas as pd
import numpy as np
#import plotly.graph_objects as go
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
if 'major_event' not in st.session_state:
    st.session_state.major_event = []
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

# Indexes: 1 - Current, 2 - Previous, 3 - Change, 4 - Fract Change
if 'gdp' not in st.session_state:
    st.session_state['gdp'] = [2.0, 2.2, -0.2, -0.1]  # initial value

if 'inflation' not in st.session_state:
    st.session_state['inflation'] = [3.4, 3.4, 0.3, 0.3]  # initial value

if 'govt_debt' not in st.session_state:
    st.session_state['govt_debt'] = [897000000000, 897000000000, 17000000000, 0.3]  # initial value

if 'unemployment' not in st.session_state:
    st.session_state['unemployment'] = [4.2, 4.2, 0.3, 0.3]  # initial value

if 'house_prices' not in st.session_state:
    st.session_state['house_prices'] = [920000, 920000, 10000,0.3]  # initial value

if 'consumer_sentiment' not in st.session_state:
    st.session_state['consumer_sentiment'] = [50, 50, 2, 0.2] # initial value

if 'imports' not in st.session_state:
    st.session_state['imports'] = [123000000000, 123000000000, 1000000, 0.2] # initial value

if 'exports' not in st.session_state:
    st.session_state['exports'] = [153000000000, 153000000000, 1000000000, 0.2] # initial value

if 'asx_200' not in st.session_state:
    st.session_state['asx_200'] = [7012.12, 7012.12, 1000, 0.2] # initial value


if 'prev_interest_rate' not in st.session_state:
    st.session_state['prev_interest_rate'] = 3.0  # initial value for previous GDP growth


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
    st.session_state['gdp'][0] -= 0.2 * raise_fifty_factor
    st.session_state['inflation'][0] -= 0.1 * raise_fifty_factor
    st.session_state['govt_debt'][0] = st.session_state['govt_debt'][0] * (1 + raise_fifty_factor/20)
    st.session_state['unemployment'][0] += 0.2 * raise_fifty_factor
    st.session_state['house_prices'][0] = st.session_state['house_prices'][0] * (1 + raise_fifty_factor/10)
    st.session_state['consumer_sentiment'][0] += 2 * raise_fifty_factor
    st.session_state['imports'][0] = st.session_state['imports'][0] * (1 + raise_fifty_factor/10)
    st.session_state['exports'][0] = st.session_state['exports'][0] * (1 + lower_fifty_factor/10)
    st.session_state['asx_200'][0] = st.session_state['asx_200'][0] * (1 + raise_fifty_factor/10)  

def raise_25():  
    st.session_state['count'] = st.session_state['count'] + 1
    st.session_state.newsprint = False
    st.session_state.confirmed = True
    st.session_state['interest_rate'] += 0.25
    st.session_state['gdp'][0] -= 0.2 * raise_twentyfive_factor
    st.session_state['inflation'][0] -= 0.1 * raise_twentyfive_factor
    st.session_state['unemployment'][0] += 0.2 * raise_twentyfive_factor
    st.session_state['house_prices'][0] = st.session_state['house_prices'][0] * (1 + raise_twentyfive_factor/10)
    st.session_state['consumer_sentiment'][0] += 1.5 * raise_twentyfive_factor
    st.session_state['govt_debt'][0] = st.session_state['govt_debt'][0] * (1 + raise_twentyfive_factor/20)
    st.session_state['imports'][0] = st.session_state['imports'][0] * (1 + raise_twentyfive_factor/10)
    st.session_state['exports'][0] = st.session_state['exports'][0] * (1 + lower_twentyfive_factor/10)
    st.session_state['asx_200'][0] = st.session_state['asx_200'][0] * (1 + raise_twentyfive_factor/10)

def koh():
    st.session_state['count'] = st.session_state['count'] + 1
    st.session_state.newsprint = False
    st.session_state.confirmed = True
    st.session_state['gdp'][0] += keepsame_factor
    st.session_state['inflation'][0] += keepsame_factor
    st.session_state['unemployment'][0] += keepsame_factor
    st.session_state['house_prices'][0] = st.session_state['house_prices'][0] * (1 + keepsame_factor/10)
    st.session_state['consumer_sentiment'][0] += keepsame_factor*10
    st.session_state['govt_debt'][0] = st.session_state['govt_debt'][0] * (1 + keepsame_factor/10)
    st.session_state['imports'][0] = st.session_state['imports'][0] * (1 + keepsame_factor/10)
    st.session_state['asx_200'][0] = st.session_state['asx_200'][0] * (1 + keepsame_factor/10)

def lower_25():
    st.session_state['count'] = st.session_state['count'] + 1
    st.session_state.newsprint = False
    st.session_state.confirmed = True
    st.session_state['interest_rate'] -= 0.25
    st.session_state['gdp'][0] += 0.2 * lower_twentyfive_factor
    st.session_state['inflation'][0] += 0.1 * lower_twentyfive_factor
    st.session_state['unemployment'][0] -= 0.2 * lower_twentyfive_factor
    st.session_state['house_prices'][0] = st.session_state['house_prices'][0] * (1 + lower_twentyfive_factor/10)
    st.session_state['consumer_sentiment'][0] += 1 * lower_twentyfive_factor
    st.session_state['govt_debt'][0] = st.session_state['govt_debt'][0] * (1 + lower_twentyfive_factor/20)
    st.session_state['imports'][0] = st.session_state['imports'][0] * (1 + lower_twentyfive_factor/10)
    st.session_state['exports'][0] = st.session_state['exports'][0] * (1 + raise_twentyfive_factor/10)
    st.session_state['asx_200'][0] = st.session_state['asx_200'][0] * (1 + lower_twentyfive_factor/10)   

def lower_50():
    st.session_state['count'] = st.session_state['count'] + 1
    st.session_state.newsprint = False
    st.session_state.confirmed = True
    st.session_state['interest_rate'] -= 0.50
    st.session_state['gdp'][0] += 0.2 * lower_fifty_factor
    st.session_state['inflation'][0] += 0.1 * lower_fifty_factor
    st.session_state['govt_debt'][0] = st.session_state['govt_debt'][0] * (1 + lower_fifty_factor/20)
    st.session_state['unemployment'][0] -= 0.2 * lower_fifty_factor
    st.session_state['house_prices'][0] = st.session_state['house_prices'][0] * (1 + lower_fifty_factor/10)
    st.session_state['consumer_sentiment'][0] += 2 * lower_fifty_factor
    st.session_state['imports'][0] = st.session_state['imports'][0] * (1 + lower_fifty_factor/10)
    st.session_state['exports'][0] = st.session_state['exports'][0] * (1 + raise_fifty_factor/10)
    st.session_state['asx_200'][0] = st.session_state['asx_200'][0] * (1 + lower_fifty_factor/10)

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
#st.image('ai_talks/assets/img/boardroom.jpg')
st.title("The Chair")
st.subheader(f'Month {st.session_state.count}')






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
    st.write("Here are the news headlines")
    st.session_state.news = ['a','b','c','d']
    #show_conversation3(np1, performance)
    #show_conversation3(np2, performance)
    #show_conversation3(np3, performance, angle2)
    #show_conversation3(np4, performance, angle1)
    # Generate some major random event
    rand_event = random.randint(0,9)
    
    st.session_state.major_event = major_events[rand_event][0]
    print(st.session_state[major_events[rand_event][1]][0])
    #st.session_state[major_events[rand_event][1]][1] = st.session_state[major_events[rand_event][1]]
    st.session_state[major_events[rand_event][1]][0] = st.session_state[major_events[rand_event][1]][0] * major_events[rand_event][2]
    print(st.session_state[major_events[rand_event][1]][0])
    st.session_state.newsprint = True

if st.session_state.count > 1: 

    st.warning(st.session_state.major_event, icon="🌏")

    # Other news
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


if st.session_state.confirmed == True:
    # Initiate session state values for metric changes
    st.session_state['gdp'][2] =  f"{round(st.session_state['gdp'][0] - st.session_state['gdp'][1],2)}%"
    st.session_state['inflation'][2] =  f"{round(st.session_state['inflation'][0] - st.session_state['inflation'][1],2)}%"
    st.session_state['govt_debt'][2] = st.session_state['govt_debt'][0] - st.session_state['govt_debt'][1]
    st.session_state['unemployment'][2] =  f"{round(st.session_state['unemployment'][0] - st.session_state['unemployment'][1],2)}%"
    st.session_state['house_prices'][2] = st.session_state['house_prices'][0] - st.session_state['house_prices'][1]
    st.session_state['consumer_sentiment'][2] =  f"{round(st.session_state['consumer_sentiment'][0] - st.session_state['consumer_sentiment'][1],2)}%"
    st.session_state['imports'][2] = st.session_state['imports'][0] - st.session_state['imports'][1]
    st.session_state['exports'][2] = st.session_state['exports'][0] - st.session_state['exports'][1]
    st.session_state['asx_200'][2] =  st.session_state['asx_200'][0] - st.session_state['asx_200'][1]

    


    # Format monetary values prices
    st.session_state['f_house_prices'] = math.ceil(st.session_state['house_prices'][0] / 100) * 100
    st.session_state['f_house_prices_change'] = math.ceil(st.session_state['house_prices'][2] / 100) * 100

    st.session_state['f_house_prices'] = f"${st.session_state['f_house_prices']:,.0f}"
    st.session_state['f_house_prices_change'] = f"{st.session_state['f_house_prices_change']:,.0f}"

    st.session_state['f_govt_debt'] = round(st.session_state['govt_debt'][0] / 1e9)
    st.session_state['f_govt_debt_change'] = f"{round(st.session_state['govt_debt'][2] / 1e9)} bn"
    st.session_state['f_govt_debt'] = f"${int(st.session_state['f_govt_debt'])} bn" 

    st.session_state['f_imports'] = round(st.session_state['imports'][0] / 1e9)
    st.session_state['f_imports_change'] = f"{round(st.session_state['imports'][2] / 1e9)} bn"
    st.session_state['f_imports'] = f"${int(st.session_state['f_imports'])} bn" 

    st.session_state['f_exports'] = round(st.session_state['exports'][0] / 1e9)
    st.session_state['f_exports_change'] = f"{round(st.session_state['exports'][2] / 1e9)} bn"
    st.session_state['f_exports'] = f"${int(st.session_state['f_exports'])} bn" 

# Economic performance list for feeding into GPT
performance = [
    ["Economic Indicator: ASX 200",
    f"Current Value: {st.session_state['asx_200']}",
    f"Change in value from previous month: {st.session_state['asx_200'][2]}"
    ],
    ["Economic Indicator: GDP",
    f"Current Value: {st.session_state['gdp']}",
    f"Change in value from previous month: {st.session_state['gdp'][2]}"
    ],
    ["Economic Indicator: Inflation",
    f"Current Value: {st.session_state['inflation']}",
    f"Change in value from previous month: {st.session_state['inflation'][2]}"
    ],
        ["Economic Indicator: Government Debt",
    f"Current Value: {st.session_state['govt_debt']}",
    f"Change in value from previous month: {st.session_state['govt_debt'][2]}"
    ],
        ["Economic Indicator: Unemployment",
    f"Current Value: {st.session_state['unemployment']}",
    f"Change in value from previous month: {st.session_state['unemployment'][2]}"
    ],
        ["Economic Indicator: House Prices",
    f"Current Value: {st.session_state['house_prices']}",
    f"Change in value from previous month: {st.session_state['house_prices'][2]}"
    ],
        ["Economic Indicator: Imports",
    f"Current Value: {st.session_state['imports']}",
    f"Change in value from previous month: {st.session_state['imports'][2]}"
    ],
        ["Economic Indicator: Exports",
    f"Current Value: {st.session_state['exports']}",
    f"Change in value from previous month: {st.session_state['exports'][2]}"
    ],
        ["Economic Indicator: Consumer Sentiment",
    f"Current Value: {st.session_state['consumer_sentiment']}",
    f"Change in value from previous month: {st.session_state['consumer_sentiment'][2]}"
    ]
]


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
            m1.metric("GDP Growth", value=f"{round(st.session_state['gdp'][0],2)}%", delta=st.session_state['gdp'][2])
            m2.metric("Inflation Rate", value=f"{round(st.session_state['inflation'][0],2)}%", delta=st.session_state['inflation'][2], delta_color="inverse")
            m3.metric("Government Debt", value=f"{st.session_state['f_govt_debt']}", delta=st.session_state['f_govt_debt_change'], delta_color="inverse")

            m4, m5, m6 = st.columns((1,1,1))
            m4.metric("National Mean House Price", value=f"{st.session_state['f_house_prices']}", delta=st.session_state['f_house_prices_change'])
            m5.metric("Unemployment Rate", value=f"{round(st.session_state['unemployment'][0],2)}%", delta=st.session_state['unemployment'][2], delta_color="inverse")
            m6.metric("Consumer Sentiment", value=f"{round(st.session_state['consumer_sentiment'][0],2)}%", delta=st.session_state['consumer_sentiment'][2])

            m7, m8, m9 = st.columns((1,1,1))
            m7.metric("Imports", value=f"{st.session_state['f_imports']}", delta=st.session_state['f_imports_change'])
            m8.metric("Exports", value=f"{st.session_state['f_exports']}", delta=st.session_state['f_exports_change'])
            m9.metric("Stock Market Index", value=round(st.session_state['asx_200'][0],2), delta=round(st.session_state['asx_200'][2],2))

        case st.session_state.locale.footer_option2:
            st.header('S&P / ASX 200')
            stock_dir = "Down" if st.session_state['asx_200'][0] < 0 else "Up"
            st.write(f"{stock_dir} {round(st.session_state['asx_200'][2],2)} points ({round(100*(1 - st.session_state['asx_200'][1]/st.session_state['asx_200'][0]),2)}%) in the past month")
            plot_asx_200(st.session_state['asx_200'][0] - st.session_state['asx_200'][1], st.session_state['asx_200'][0], 1)




if __name__ == "__main__":
    run_agi()
    

# Update previous metrics for the next round
if st.session_state.confirmed:  
    st.session_state['prev_interest_rate'] = st.session_state['interest_rate']
    st.session_state['gdp'][1] = st.session_state['gdp'][0]
    st.session_state['inflation'][1] = st.session_state['inflation'][0]
    st.session_state['govt_debt'][1] = st.session_state['govt_debt'][0]
    st.session_state['unemployment'][1] = st.session_state['unemployment'][0]
    st.session_state['house_prices'][1] = st.session_state['house_prices'][0]
    st.session_state['consumer_sentiment'][1] = st.session_state['consumer_sentiment'][0]
    st.session_state['imports'][1] = st.session_state['imports'][0]
    st.session_state['exports'][1] = st.session_state['exports'][0]
    st.session_state['asx_200'][1] = st.session_state['asx_200'][0]
    st.session_state.meeting = False
    st.session_state.confirmed = False 
    clear_chat()  
