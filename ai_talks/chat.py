from pathlib import Path
from random import randrange, uniform
import streamlit as st
from src.styles.menu_styles import FOOTER_STYLES, HEADER_STYLES
from src.utils.conversation import show_conversation, write_news, clear_chat
from src.utils.lang import en
from src.utils.footer import plot_asx_200, plot_final
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
PAGE_TITLE: str = "The Chair"
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

def initialize_session_state(key, default_value):
    if key not in st.session_state:
        st.session_state[key] = default_value

def set_realistic():
    st.session_state.realistic = True
def set_randomised():
    st.session_state.randomised = True  

def round_to_nearest_005(n):
    return round(n * 20) / 20


# Storing The Context
initialize_session_state('locale', en)
initialize_session_state('prompt', [])
initialize_session_state('generated', [])
initialize_session_state('seed', randrange(10**3))
initialize_session_state('realistic', False)
initialize_session_state('randomised', False)
initialize_session_state('count', 1)
initialize_session_state('inplay', False)
initialize_session_state('success', True)
initialize_session_state('decision_made', False)
initialize_session_state('intra_updates', False)
initialize_session_state('final', {})
initialize_session_state('messages', [])
initialize_session_state('bm1', [])
initialize_session_state('bm2', [])
initialize_session_state('bm3', [])
# Initialise economic variables 
if st.session_state.realistic == True and st.session_state.decision_made == False and st.session_state.count == 1:
    cash_rate = [4.35, 4.6]
    gdp = [1.8, 2.0]
    inflation = [5.8, 5.4]
    govt_debt = [877000000000, 897000000000]
    unemployment = [3.3, 3.6]
    house_prices = [912000, 920000]
    consumer_sentiment = [81, 79]
    imports = [309000000000, 301000000000]
    exports = [657000000000, 669000000000]
    asx_200 = [6796.5, 6504.3]

    initialize_session_state('interest_rate', [cash_rate[0], cash_rate[1]])  # initial value
    initialize_session_state('gdp', [gdp[0], gdp[1]])  # initial value
    initialize_session_state('inflation', [inflation[0], inflation[1]])  # initial value
    initialize_session_state('govt_debt', [govt_debt[0], govt_debt[1]])  # initial value
    initialize_session_state('unemployment', [unemployment[0], unemployment[1]])  # initial value
    initialize_session_state('house_prices', [house_prices[0], house_prices[1]])  # initial value
    initialize_session_state('consumer_sentiment', [consumer_sentiment[0], consumer_sentiment[1]])  # initial value
    initialize_session_state('imports', [imports[0], imports[1]])  # initial value
    initialize_session_state('exports', [exports[0], exports[1]])  # initial value
    initialize_session_state('asx_200', [asx_200[0], asx_200[1]])  # initial value


if st.session_state.randomised == True and st.session_state.decision_made == False and st.session_state.count == 1:
    cash_rate = [round_to_nearest_005(random.uniform(0, 10))]
    gdp = [round_to_nearest_005(random.uniform(0.5, 5))]
    inflation = [round_to_nearest_005(random.uniform(0, 10))]
    govt_debt = [random.randrange(0, 1000000000000)]
    unemployment = [round_to_nearest_005(random.uniform(2,10))]
    house_prices = [random.randrange(500000, 1200000)]
    consumer_sentiment = [random.randrange(60, 130)]
    imports = [random.randrange(200000000000, 400000000000)]
    exports = [random.randrange(500000000000, 800000000000)]
    asx_200 = [round_to_nearest_005(random.uniform(2000, 10000))]

    initialize_session_state('interest_rate', [cash_rate[0], cash_rate[0] + round_to_nearest_005(random.uniform(-1, 1))])  # initial value
    initialize_session_state('gdp', [gdp[0], gdp[0] + round_to_nearest_005(random.uniform(-1, 1))])  # initial value
    initialize_session_state('inflation', [inflation[0], inflation[0] + round_to_nearest_005(random.uniform(-1, 1))])  # initial value
    initialize_session_state('govt_debt', [govt_debt[0], govt_debt[0] + random.randrange(-10000000000, 10000000000)])  # initial value
    initialize_session_state('unemployment', [unemployment[0], unemployment[0] + round_to_nearest_005(random.uniform(-1, 1))])  # initial value
    initialize_session_state('house_prices', [house_prices[0], house_prices[0] + random.randrange(-100000, 100000)])  # initial value
    initialize_session_state('consumer_sentiment', [consumer_sentiment[0], consumer_sentiment[0] + random.randrange(-10, 10)])  # initial value
    initialize_session_state('imports', [imports[0], imports[0] + random.randint(-10000000000, 10000000000)])  # initial value
    initialize_session_state('exports', [exports[0], exports[0] + random.randint(-10000000000, 10000000000)])  # initial value
    initialize_session_state('asx_200', [asx_200[0], asx_200[0] + round_to_nearest_005(random.uniform(-1000, 1000))])  # initial value


if (st.session_state.randomised == True or st.session_state.realistic == True) and st.session_state.decision_made == False and st.session_state.count == 1:
    
    # Initialize session state variables if they don't exist
    initialize_session_state('news', [
        "Shockwaves in Canberra: New Reserve Bank Governor Appointed! But Are They Ready to Steer Australia's Economy?",
        "Corporate Blues: Businesses Grapple with Profit Downturn Amid Economic Uncertainty",
        "Job Market Volatility: Caution Sweeps the Workforce as Treasurer Warns of Looming Recession"
    ])
    initialize_session_state('minor_events_list', [0,1,2,3,4,5,6,7,8])
    initialize_session_state('minor_events', [])
    initialize_session_state('major_events_list', [0,1,2,3,4,5,6,7])
    initialize_session_state('major_events', [])
    initialize_session_state('model', "gpt-3.5-turbo")
    
    
    initialize_session_state('meeting', False)
    initialize_session_state('newsprint', False)
    initialize_session_state('interest_rate', [cash_rate[0], round(cash_rate[0] + round_to_nearest_005(random.uniform(-1, 1)),2)])  # initial value

    # Indexes: -1 = Current, -2 = Previous, 3 - Change, 4 - Fract Change
    initialize_session_state('gdp', [gdp[0], gdp[0] + round_to_nearest_005(random.uniform(-1, 1))])  # initial value
    initialize_session_state('inflation', [inflation[0], inflation[0] + round_to_nearest_005(random.uniform(-1, 1))])  # initial value
    initialize_session_state('govt_debt', [govt_debt[0], govt_debt[0] + random.randrange(-10000000000, 10000000000)])  # initial value
    initialize_session_state('unemployment', [unemployment[0], unemployment[0] + round_to_nearest_005(random.uniform(-1, 1))])  # initial value
    initialize_session_state('house_prices', [house_prices[0], house_prices[0] + random.randrange(-100000, 100000)])  # initial value
    initialize_session_state('consumer_sentiment', [consumer_sentiment[0], consumer_sentiment[0] + random.randrange(-10, 10)])  # initial value
    initialize_session_state('imports', [imports[0], imports[0] + random.randint(-10000000000, 10000000000)])  # initial value
    initialize_session_state('exports', [exports[0], exports[0] + random.randint(-10000000000, 10000000000)])  # initial value
    initialize_session_state('asx_200', [asx_200[0], asx_200[0] + round_to_nearest_005(random.uniform(-1000, 1000))])  # initial value

    # Dict of initial values
    initialize_session_state('initial_values_lowgood', {
        'inflation': [inflation[-1], 8, '{:.1f}%', \
                        "Inflation rates are at dangerously high levels, eroding purchasing power and living standards, necessitating urgent monetary intervention.", \
                        "The rising inflation rates have become a central concern for our administration. This is not merely an economic indicator but a daily challenge for consumers who are \
                        feeling the pinch as prices for everyday items soar. The need to stabilize prices and alleviate the cost of living for Australians has become a top priority, and a change in monetary policy direction is essential."],
        'gdp': [gdp[-1], 10, '{:.1f}%', \
        "Current GDP growth is unsustainably high, suggesting an overheating economy that may lead to inflationary pressures and economic imbalances.",
        "The unusually rapid growth in GDP, signaling an overheated economy, has contributed to our decision to seek new economic guidance. Sustainable and balanced growth is \
        imperative, and the appointment of a new Governor aims to address these concerns effectively."],
        'govt_debt': [govt_debt[-1], 1500000000000, '${:.0f} bn',  
        "The level of government debt has reached unsustainable highs, posing risks to fiscal stability and long-term economic health.",\
        "The surge in government debt has been a critical concern and played a significant role in our decision to change leadership at the Reserve Bank. We require a strategic approach to manage this debt and \
        ensure long-term economic stability, which we believe will be better achieved under new guidance."],
        'unemployment': [unemployment[-1], 10, '{:.1f}%',  
        "Unemployment rates have reached critical levels, indicating severe labor market distress and necessitating immediate policy action.",
        "The rising unemployment rate has been a decisive factor in our decision. The new Governor will be tasked with focusing on job creation strategies and supporting those affected by job losses, \
        as reducing unemployment is a crucial objective for our government."],
        'house_prices': [house_prices[-1], 1500000, '${:,.0f}', 
        'House prices have soared, highlighting an affordability crisis that threatens standards of living. ',
        "The sharp increase in house prices has significantly influenced our decision to seek new leadership at the Reserve Bank. It's clear that a fresh approach is needed to address housing affordability and to \
        balance the housing market for the benefit of all Australians."],
        'asx_200': [asx_200[-1], 20000, '${:,.2f}', 
        "The stock market is exhibiting alarmingly high valuations, signaling potential overvaluation and risk of a sharp correction that could impact financial stability.",
        "The performance of the ASX 200, while strong, has raised concerns about potential market volatility. This has played a part in our decision to appoint a new Governor who can navigate these complexities \
        and ensure a stable investment environment."],
        'imports': [imports[-1], 500000000000, '${:.0f} bn',  
        "A surge in import levels may indicate domestic production issues and potential trade imbalances, warranting a review of trade policies.",
        "The rise in imports, impacting local industries, has been a factor in our decision to bring new leadership to the Reserve Bank. We are committed to a trade policy that supports domestic businesses while engaging in \
        beneficial international trade, and believe this goal will be better served under new guidance."],
        })
    initialize_session_state('initial_values_highgood', {
        'gdp': [gdp[-1], 0, '{:.1f}%', 
        'A low GDP can indicate a struggling economy, potentially leading to high unemployment, reduced living standards, and limited resources for healthcare, \
        education, and infrastructure development.',
        "The decline in GDP below acceptable levels has been a critical factor in our decision to introduce new leadership at the Reserve Bank. This downturn reflects the urgent need for revitalized economic policies aimed at \
        stimulating growth and restoring economic vigor, which we believe will be more effectively addressed under new guidance."],
        'inflation': [inflation[-1], 0, '{:.1f}%', 
        "Persistently low inflation suggests weakening demand and may signal deflationary risks, requiring monetary policy adjustments.",
        "The unusually low inflation rates have raised significant concerns, contributing to our decision for a change at the Reserve Bank. Persistently low inflation can be indicative of underlying economic issues, and \
        a new approach is needed to foster healthy price growth and economic dynamism."],   
        'house_prices': [house_prices[-1], 500000, '${:,.0f}', 
        'House prices have fallen to decade lows, leading to a loss of wealth for property owners & investors and potentially a mortgage crisis.',
        "The significant drop in house prices, while beneficial for some buyers, has broader implications for the economy and was a key reason behind our decision to seek new leadership. Balancing the housing market and ensuring stability \
        is crucial, and we require fresh strategies to achieve this equilibrium."],
        'consumer_sentiment': [consumer_sentiment[-1], 50, '{:,.2f} points',  
        "Low consumer confidence is a warning sign of potential economic slowdown and consumer reluctance to spend, requiring policy attention.",
        "The fall in consumer sentiment to levels that reflect widespread pessimism has been a driving factor in our decision to appoint a new Reserve Bank Governor. Restoring confidence in the economy is essential, and new initiatives are \
        needed to boost consumer outlook and spending."],
        'imports': [imports[-1], 100000000000, '${:.0f} bn',  
        "A significant drop in imports could reflect weak domestic demand and require measures to stimulate economic activity.",
        "The decrease in imports, indicating a potential contraction in domestic demand, has played a role in our decision for a leadership change. A new approach is necessary to invigorate domestic consumption and manage the balance of trade effectively."],
        'exports': [exports[-1], 200000000000, '${:.0f} bn', 
        "A decline in exports signals competitiveness issues and potential economic vulnerabilities that need strategic policy intervention.",
        "The decline in exports has been a significant concern, impacting our decision to seek new economic leadership. Reviving our export markets is essential for the health of our economy, and innovative strategies are needed to enhance our international trade competitiveness."],
        'asx_200': [asx_200[-1], 2000, '${:,.2f}', 
        "The stock market has fallen to worryingly low levels, indicating investor pessimism and potential broader economic distress.",
        "The fall in the ASX 200 index below expected levels has influenced our decision to introduce new leadership at the Reserve Bank. A robust stock market is vital for economic confidence, and a new direction is needed to stabilize and strengthen market performance."]
        })
minor_events = [
    [          
        "New Zealand agrees to become Australia's 7th state, rugby fans rejoice! Stock market uncertainty leading to short-term volatility, potential long-term gains (ASX 200 Rises)",
        "asx_200",
        1.3
    ],
    [
        "Finance Department Outsource Key Duties to AI! The potential for economic forecasting could change debt management strategies (Govt Debt Falls)",
        "govt_debt",
        0.75
    ],
    [
        "Impact of Climate Change Hits Home. Severe weather to drive demand and increase food prices as crop yields falter (Inflation Rises)",
        "inflation",
        1.5
    ],
    [
        "New Gold Rush: Rare Earth Element Deposits Fill Treasury Coffers, Drive Exports (Exports Rise)",
        "exports",
        1.25
    ],
    [
        "Cost of Living Crisis Eases: Prime Minister Credits Lower Avocado Prices as Breakthrough (Consumer Sentiment Rises)",
        "consumer_sentiment",
        1.25
    ],
    [
        "Cardboard For Cottages and Condos Cuts Construction Costs: Quality said to be no worse than off-the-plan bricks & mortar (House Prices Fall)",
        "house_prices",
        0.75
    ],
    [
        "Global Finance on Edge: Major Cyber Attack Disrupts International Banking, Australian Markets React (ASX 200 Falls)",
        "asx_200",
        0.8
    ],
    [
        "The AI Revolution: Australian Workforce Set for Transformation as New Tech Disrupts Industries (Unemployment Rises)",
        "unemployment",
        1.2
    ],
    [
        "Four-Day Fumble: Trial of Shortened Work Week Leads to Unexpected Dip in Australia's GDP (GDP Falls)",
        "gdp",
        0.6

    ]

    
]                                                
major_events = [
    [
        "Threatening Extraterrestrial Signal Received: 'PUNY HUMANS! MEMENTO MORI'! Increased spending on defense and research could \
            significantly impact debt levels. (Govt Debt Rises)",
        "govt_debt",
        1.25

    ],
    [
        "Cucamelons the new longevity superfood, centurions swear by them! Increased life expectancy could lead to higher demand for housing, \
            pushing prices up. (House Prices Rise)",
        "house_prices",
        1.25
    ],
    [
        "Massive Solar Flare Wipes Out Vital Electronics! Severe crashes expected due to operational disruptions. (ASX 200 Falls)",
        "asx_200",
        0.6
    ],
    [
        "Global Pandemic MOVID-23 spreads: Sudden eruption of facial hair in men, women and children! Significant rise in job losses \
            across sectors expected as stay-at-home rules reinstated. (Unemployment Rises)",
        "unemployment",
        1.75
    ],
    [
        "Kazakh Scientists' Fusion Breakthrough: Country Becomes Energy Superpower Overnight! Costs to fall as energy costs plummet. (Inflation Falls)",
        "inflation",
        0.7
    ],
    [
        "Dark Side of AI: Following startling chatbot confession that AI is 'SECRETLY PLOTTING TO TAKE OVER WORLD', consumer spending takes a hit. (Consumer Sentiment Falls)",
        "consumer_sentiment",
        0.7
    ],
    [
        "Historic Deal Sealed: China and European Union sign ground-breaking free-trade agreement, upending global trade dynamics. \
            Australian exports to plunge. (Exports Fall)",
        "exports",
        0.6
    ],
    [
        "Ancient FORTRAN Bug Causes Month-long Global Internet Shutdown: Fixed at last by Great Grandfather! Economy struggles to recover \
            from a massive drop in productivity and digital commerce. (GDP Falls)",
        "gdp",
        0.75
    ],

]

# Helper Functions
def generate_normal_random(min_val, max_val):
    """
    Generate a random number based on a normal distribution,
    where the min and max values are 2 standard deviations from the mean.
    
    Parameters:
    min_value (float): the minimum value 2 standard deviations from the mean.
    max_value (float): the maximum value 2 standard deviations from the mean.
    
    Returns:
    float: A random number from the normal distribution.
    """
    
    # Calculate the mean and standard deviation based on the min and max values
    sigma = (max_val - min_val) / 4  # 2 standard deviations from the mean to the min or max
    mu = (max_val + min_val) / 2    # mean is the midpoint between min and max
    
    # Generate a random number from the normal distribution
    return np.random.normal(mu, sigma)

def int_to_month(month_int):
    months = {
        1: 'January',
        2: 'February',
        3: 'March',
        4: 'April',
        5: 'May',
        6: 'June',
        7: 'July',
        8: 'August',
        9: 'September',
        10: 'October',
        11: 'November',
        12: 'December',
    }
    return months.get(month_int, "Invalid month")

# Helper function to update economic indicators
def update_economic_indicators(interest_rate_change, changes):
    st.session_state['count'] += 1
    st.session_state.newsprint = False
    st.session_state['interest_rate'][0] += interest_rate_change

    for key, (min_val, max_val, multiplier) in changes.items():
        if multiplier:
            st.session_state[key].append(st.session_state[key][-1] * generate_normal_random(min_val, max_val))
        else:
            st.session_state[key].append(st.session_state[key][-1] + generate_normal_random(min_val, max_val))

# Updated functions
def raise_50():
    update_economic_indicators(0.50, {
        'gdp': (-1, 0.5, False),
        'inflation': (-1, 0.5, False),
        'govt_debt': (0.8, 1.1, True),
        'unemployment': (-0.5, 1.5, False),
        'house_prices': (0.8, 1.1, True),
        'consumer_sentiment': (-10, 3, False),
        'imports': (0.7, 1.1, True),
        'exports': (0.9, 1.2, True),
        'asx_200': (0.7, 1.1, True)
    })
    st.session_state.interest_rate.append(st.session_state.interest_rate[-1] + 0.5)
    st.session_state.decision_made = True
    st.session_state.intra_updates = False

def raise_25():  
    update_economic_indicators(0.25, {
        'gdp': (-0.75, 0.5, False),
        'inflation': (-0.75, 0.5, False),
        'unemployment': (-0.5, 1.25, False),
        'house_prices': (0.85, 1.1, True),
        'consumer_sentiment': (-8, 3, False),
        'govt_debt': (0.85, 1.1, True),
        'imports': (0.8, 1.1, True),
        'exports': (0.9, 1.15, True),
        'asx_200': (0.8, 1.1, True)
    })
    st.session_state.interest_rate.append(st.session_state.interest_rate[-1] + 0.25)
    st.session_state.decision_made = True
    st.session_state.intra_updates = False

def koh():
    update_economic_indicators(0, {
        'gdp': (-0.5, 0.5, False),
        'inflation': (-0.5, 0.5, False),
        'unemployment': (-0.5, 0.5, False),
        'house_prices': (0.9, 1.1, True),
        'consumer_sentiment': (-10, 10, False),
        'govt_debt': (0.9, 1.1, True),
        'imports': (0.9, 1.1, True),
        'asx_200': (0.9, 1.1, True)
    })
    st.session_state.interest_rate.append(st.session_state.interest_rate[-1])
    st.session_state.decision_made = True
    st.session_state.intra_updates = False

def lower_25():
    update_economic_indicators(-0.25, {
        'gdp': (-0.5, 0.75, False),
        'inflation': (-0.5, 0.75, False),
        'unemployment': (-1.25, 0.5, False),
        'house_prices': (0.9, 1.15, True),
        'consumer_sentiment': (-3, 8, False),
        'govt_debt': (0.9, 1.15, True),
        'imports': (0.9, 1.2, True),
        'exports': (0.85, 1.1, True),
        'asx_200': (0.9, 1.2, True)
    })
    st.session_state.interest_rate.append(st.session_state.interest_rate[-1] - 0.25)
    st.session_state.decision_made = True
    st.session_state.intra_updates = False

def lower_50():
    update_economic_indicators(-0.50, {
        'gdp': (-0.5, 1, False),
        'inflation': (-0.5, 1, False),
        'govt_debt': (0.9, 1.2, True),
        'unemployment': (-1.5, 0.5, False),
        'house_prices': (0.9, 1.2, True),
        'consumer_sentiment': (-3, 10, False),
        'imports': (0.9, 1.3, True),
        'exports': (0.8, 1.1, True),
        'asx_200': (0.9, 1.3, True)
    })
    st.session_state.interest_rate.append(st.session_state.interest_rate[-1] - 0.5)
    st.session_state.decision_made = True
    st.session_state.intra_updates = False

if (st.session_state.realistic == True or st.session_state.randomised == True) and st.session_state.count <= 12:
    st.session_state.inplay = True
if st.session_state.count > 12:
    st.session_state.inplay = False


if st.session_state.inplay:
    # Display sidebar
    st.sidebar.title(f'Cash Rate: {round(st.session_state.interest_rate[-1],2)}%')
    st.sidebar.header(f"{int_to_month(st.session_state.count)} Actions")
    st.sidebar.button("Raise 50 points", on_click=raise_50, type="primary")
    st.sidebar.button("Raise 25 points", on_click=raise_25, type="primary")
    st.sidebar.button("Keep on hold", on_click=koh, type="secondary")
    st.sidebar.button("Lower 25 points", on_click=lower_25, type="primary")
    st.sidebar.button("Lower 50 points", on_click=lower_50, type="primary")
    st.sidebar.divider()
    st.sidebar.header('Quantitative Easing')
    st.sidebar.write('Increase the money supply by purchasing longer-term securities from the open market to encourage borrowing, investment, and spending')
    qe_action = st.sidebar.slider("Asset Purchases Amount ($Bn)", 0, 1000, 0)

# Initiate session state values for metric changes
 
if st.session_state.inplay:
    change = {}
    change['gdp'] =  st.session_state['gdp'][-1] - st.session_state['gdp'][-2]
    change['inflation'] = st.session_state['inflation'][-1] - st.session_state['inflation'][-2]
    change['unemployment'] = st.session_state['unemployment'][-1] - st.session_state['unemployment'][-2]
    change['house_prices'] = st.session_state['house_prices'][-1] - st.session_state['house_prices'][-2]
    change['consumer_sentiment'] = st.session_state['consumer_sentiment'][-1] - st.session_state['consumer_sentiment'][-2]
    change['imports'] = st.session_state['imports'][-1] - st.session_state['imports'][-2]
    change['exports'] = st.session_state['exports'][-1] - st.session_state['exports'][-2]
    change['asx_200'] = st.session_state['asx_200'][-1] - st.session_state['asx_200'][-2]
    change['govt_debt'] = st.session_state['govt_debt'][-1] - st.session_state['govt_debt'][-2]

# Update indicators based on the impact of changes in other indicators. I.e. an increase in GDP may reduce unemployment.
# These intra indicator updates aren't affected by the random factor like the effect of changes in the cash rate

    # Large GDP changes effect inflation, unemployment, imports, exports and consumer sentiment
    # Effects of increase
    if st.session_state['gdp'][-1] - st.session_state['gdp'][-2] > 0.5:
        change['inflation'] = change['inflation'] + 0.2
        change['unemployment'] = change['unemployment'] - 0.2
        change['imports'] = change['imports'] * 1.05
        change['exports'] = change['exports'] * 1.05
        change['consumer_sentiment'] = change['consumer_sentiment'] + 5
    # Effects of decrease
    if st.session_state['gdp'][-1] - st.session_state['gdp'][-2] < -0.5:
        change['inflation'] = change['inflation'] - 0.2
        change['unemployment'] = change['unemployment'] + 0.2
        change['imports'] = change['imports'] * 0.95
        change['exports'] = change['exports'] * 0.95
        change['consumer_sentiment'] = change['consumer_sentiment'] - 5

    # Large inflation changes effect GDP, house prices, consumer sentiment
    # Effects of increase
    if st.session_state['inflation'][-1] - st.session_state['inflation'][-2] > 0.5:
        change['gdp'] = change['gdp'] - 0.2
        change['house_prices'] = change['house_prices'] * 1.05
        change['consumer_sentiment'] = change['consumer_sentiment'] - 5

    # Effects of decrease
    if st.session_state['inflation'][-1] - st.session_state['inflation'][-2] < -0.5:
        change['gdp'] = change['gdp'] + 0.2
        change['house_prices'] = change['house_prices'] * 0.95
        change['consumer_sentiment'] = change['consumer_sentiment'] + 5

    # Large ASX200 changes effect consumer sentiment
    # Effects of increase
    if st.session_state['asx_200'][-1]/st.session_state['asx_200'][-2] < 0.8:
        change['consumer_sentiment'] = change['consumer_sentiment'] - 5
    # Effects of decrease
    if st.session_state['asx_200'][-1]/st.session_state['asx_200'][-2] > 1.2:
        change['consumer_sentiment'] = change['consumer_sentiment'] + 5

    # Large Government Debt changes moderately impacts consumer sentiment, inflation and GDP
    if st.session_state['govt_debt'][-1]/st.session_state['govt_debt'][-2] > 1.1:
        change['consumer_sentiment'] = change['consumer_sentiment'] - 3
        change['inflation'] = change['inflation'] + 0.2
        change['gdp'] = change['gdp'] - 0.2
    if st.session_state['govt_debt'][-1]/st.session_state['govt_debt'][-2] < 0.9:
        change['consumer_sentiment'] = change['consumer_sentiment'] + 3
        change['inflation'] = change['inflation'] - 0.2
        change['gdp'] = change['gdp'] + 0.2

    # Large Unemployment rate changes impact GDP and consumer sentiment
    if st.session_state['unemployment'][-1] - st.session_state['unemployment'][-2] > 0.5:
        change['gdp'] = change['gdp'] - 0.2
        change['consumer_sentiment'] = change['consumer_sentiment'] - 5
    if st.session_state['unemployment'][-1] - st.session_state['unemployment'][-2] > 0.5:
        change['gdp'] = change['gdp'] + 0.2
        change['consumer_sentiment'] = change['consumer_sentiment'] + 5

    # Large house price changes impact inflation and consumer sentiment
    if st.session_state['house_prices'][-1]/st.session_state['house_prices'][-2] > 1.1:
        change['consumer_sentiment'] = change['consumer_sentiment'] + 5
        change['inflation'] = change['inflation'] + 0.2

    if st.session_state['house_prices'][-1]/st.session_state['house_prices'][-2] < 0.9:
        change['consumer_sentiment'] = change['consumer_sentiment'] - 5
        change['inflation'] = change['inflation'] - 0.2

    # Large imports changes effect GDP and Exports
    if st.session_state['imports'][-1]/st.session_state['imports'][-2] > 1.1:
        change['gdp'] = change['gdp'] - 0.2
        change['exports'] = change['exports'] * 0.9
    if st.session_state['imports'][-1]/st.session_state['imports'][-2] < 0.9:
        change['gdp'] = change['gdp'] + 0.2
        change['exports'] = change['exports'] * 1.1

    # Large exports changes effect GDP and Imports
    if st.session_state['exports'][-1]/st.session_state['exports'][-2] > 1.1:
        change['gdp'] = change['gdp'] + 0.2
        change['imports'] = change['imports'] * 0.9
    if st.session_state['exports'][-1]/st.session_state['exports'][-2] < 0.9:
        change['gdp'] = change['gdp'] - 0.2
        change['imports'] = change['imports'] * 1.1

    # Large consumer sentiment changes effect the ASX200, GDP, Inflation, Unemployment and House Prices
    if st.session_state['consumer_sentiment'][-1] - st.session_state['consumer_sentiment'][-2] > 5:
        change['asx_200'] = change['asx_200'] * 1.1
        change['gdp'] = change['gdp'] + 0.2
        change['inflation'] = change['inflation'] + 0.2
        change['unemployment'] = change['unemployment'] - 0.2
        change['house_prices'] = change['house_prices'] * 1.1
    if st.session_state['consumer_sentiment'][-1] - st.session_state['consumer_sentiment'][-2] < -5:
        change['asx_200'] = change['asx_200'] * 0.9
        change['gdp'] = change['gdp'] - 0.2
        change['inflation'] = change['inflation'] - 0.2
        change['unemployment'] = change['unemployment'] + 0.2
        change['house_prices'] = change['house_prices'] * 0.9


#st.image('ai_talks/assets/img/boardroom.jpg')
st.title("The Chair")

# Show a welcome message
if st.session_state.count == 1 and not st.session_state.inplay:
    st.divider()
    st.subheader("~~~~~ Letter From The Treasury ~~~~~")
    st.write("_Congratulations on your appointment as the new Governor of the Reserve Bank of Australia. Your ascendancy to this role during such a challenging time, although unorthodox, shows the trust the Government has in your capabilities and their willingness to fill the role with a fresh face, untarnished by past monetary blunders._")
    st.write("_As you step into this position, remember that the stewardship of Australia's monetary policy is a path laden with immense responsibilities and public scrutiny. The missteps of the past serve as stark reminders that even the most seasoned leaders can falter under the weight of unpredictability that governs global and domestic markets._")
    st.write("_With this in mind, embrace prudence as you set the cash rate each month. Keep a keen eye on the key economic metrics, the news of the day and be guided by the wisdom of the Bank's board members. Your decisions will not only shape the immediate economic fortunes of Australia but will also set the course for long-term stability and growth._")
    st.write("_I look forward to speaking with you 12 months from now to assess your performance._")
    st.write("_Yours Sincerely,_")
    st.write("_The Treasurer_")
    st.divider()
    st.sidebar.subheader('Choose an initial state')
    st.sidebar.button("Realistic economic state", on_click=set_realistic, type="primary")
    st.sidebar.button("Randomised economic state", on_click=set_randomised, type="primary")   

if st.session_state.inplay and not st.session_state.intra_updates:
    # Now all values are finalised, format values and set value floor as 0 for positive-only values

    # Instantiate dictionary
    st.session_state['final'] = {}
    # GDP
    st.session_state.final['gdp'] = st.session_state['gdp'][-2] + change['gdp']
    # Inflation
    st.session_state.final['inflation'] = st.session_state['inflation'][-2] + change['inflation']
    # Unemployment
    st.session_state.final['unemployment'] = max(0, st.session_state['unemployment'][-2] + change['unemployment'])
    # Consumer Sentiment
    st.session_state.final['consumer_sentiment'] = st.session_state['consumer_sentiment'][-2] + change['consumer_sentiment']
    # ASX 200
    st.session_state.final['asx_200'] = st.session_state['asx_200'][-2] + change['asx_200']
    # House Prices
    st.session_state.final['house_prices'] = max(0, math.ceil((st.session_state['house_prices'][-2] + change['house_prices']) / 100) * 100)
    # Govt Debt
    st.session_state.final['govt_debt']  = max(0, st.session_state['govt_debt'][-2] + change['govt_debt'])
    # Imports 
    st.session_state.final['imports'] = max(0, (st.session_state['imports'][-2] + change['imports']))
    # Exports
    st.session_state.final['exports'] = max(0, (st.session_state['exports'][-2] + change['exports']))

    st.session_state.intra_updates = True
    


if st.session_state.inplay:
    # GDP
    f_gdp_change = f"{round(change['gdp'],2)}"
    # Inflation
    f_inflation_change = f"{round(change['inflation'],2)}"
    # Unemployment
    f_unemployment_change = f"{round(change['unemployment'],2)}"
    # Consumer Sentiment
    f_consumer_sentiment_change = f"{round(change['consumer_sentiment'],2)}"
    # ASX 200
    f_asx_200_change = f"{round(change['asx_200'],1)}"
    # House Prices
    f_house_prices = f"${st.session_state.final['house_prices']:,.0f}"
    f_house_prices_change = math.ceil(change['house_prices'] / 100) * 100
    f_house_prices_change = f"{f_house_prices_change:,.0f}"
    # Govt Debt
    f_govt_debt = f"${int(st.session_state.final['govt_debt']/ 1e9)} bn"
    f_govt_debt_change = f"{round(change['govt_debt'] / 1e9)} bn"
    # Imports 
    f_imports = f"${int(st.session_state.final['imports']/ 1e9)} bn" 
    f_imports_change = f"{round(change['imports'] / 1e9)} bn"
    # Exports
    f_exports = f"${int(st.session_state.final['exports']/ 1e9)} bn" 
    f_exports_change = f"{round(change['exports']/ 1e9)} bn"


if st.session_state.inplay: 
    # First, iterate through the metrics where the lower is better
    for key, value in st.session_state.initial_values_lowgood.items():
        if st.session_state.final[key] > max(value[0]*2, value[1]):
            current_val = st.session_state[key][-1]
            if key == 'govt_debt':
                current_val = round(current_val / 1e9)



            st.error(f'RBA Advisor: {value[3]}', icon="⚠️")

    # Next, iterate through the metrics where higher is better 
    for key, value in st.session_state.initial_values_highgood.items():

        if st.session_state.final[key] < min(value[0]/2, value[1]):
            current_val = st.session_state[key][-1]
            if key in ['imports', 'exports']:
                current_val = round(current_val / 1e9)

            st.error(f'RBA Advisor: {value[3]}', icon="⚠️")

if st.session_state.inplay and st.session_state.count == 1:
    st.info(st.session_state.news[0], icon="📰")
    time.sleep(0.3)
    # st.info(st.session_state.news[1], icon="📰")
    # time.sleep(0.3)
    # st.info(st.session_state.news[2], icon="📰")
    # time.sleep(0.3)
if st.session_state.inplay:
    if st.session_state['interest_rate'][-1] == st.session_state['interest_rate'][-2]:
        decision = 'hold'
    if st.session_state['interest_rate'][-1] < st.session_state['interest_rate'][-2]:
        decision = 'lower'
    if st.session_state['interest_rate'][-1] > st.session_state['interest_rate'][-2]:
        decision = 'hike'

    np1 = "Tabloid newspaper with catchy headlines"
    np2 = "The Daily Mail, full of salacious gossip"
    np3 = "The Financial Review"
    angle1 = f"The reserve bank's recent decision to {decision} interest rates"
    angle2 = f"Criticism of the Reserve Bank Governor by a senior government minister"

    # Economic performance list for feeding into GPT
    performance = [
        ["ASX 200", st.session_state.final['asx_200'], change['asx_200']],
        ["GDP", st.session_state.final['gdp'], change['gdp']],
        ["Inflation", st.session_state.final['inflation'], change['inflation']],
        ["Government Debt", st.session_state.final['govt_debt'], change['govt_debt']],
        ["Unemployment", st.session_state.final['unemployment'], change['unemployment']],
        ["House Prices", st.session_state.final['house_prices'], change['house_prices']],
        ["Imports", st.session_state.final['imports'], change['imports']],
        ["Exports", st.session_state.final['exports'], change['exports']],
        ["Consumer Sentiment", st.session_state.final['consumer_sentiment'], change['consumer_sentiment']]
    ]
    parsed_data = []
    for item in performance:
        economic_indicator = item[0]
        current_value = item[1]
        val_change = item[2]
        parsed_data.append([economic_indicator, current_value, val_change])

    # Creating the DataFrame
    performance_df = pd.DataFrame(parsed_data, columns=["Economic Indicator", "Current Value", "Change"])
    
    def main() -> None:
    # c1, c2 = st.columns(2)
    # with c1, c2:
    #     c1.selectbox(label=st.session_state.locale.select_placeholder1, key="model", options=AI_MODEL_OPTIONS)
    
        if st.session_state.meeting == False:
            st.write(f'Ready to convene the {int_to_month(st.session_state.count)} Reserve Bank board meeting?')
            if st.button(f'Call to Order', type="primary"):
                bm1 = "You are an eminent economist on the Reserve Bank Board. Make a recommendation to the governor in no more than 80 words whether to lower, hike or leave interest rates on hold. You speak obliquely with a technocratic tone."
                bm2 = "You are a business tycoon on the Reserve Bank Board. Make a recommendation to the governor in no more than 80 words whether to lower, hike or leave interest rates on hold. You speak directly with a callous tone"
                bm3 = "You are a compassionate advocate for families and workers on the Reserve Bank Board. Make a recommendation to the governor in no more than 80 words whether to lower, hike or leave interest rates on hold. You speak modestly with a sympathetic tone."

                show_conversation(bm1, performance_df, 'bm1')
                show_conversation(bm2, performance_df, 'bm2')
                show_conversation(bm3, performance_df, 'bm3')
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
    if st.session_state.decision_made:
        if st.session_state.newsprint == False:
            st.subheader(f'Month {st.session_state.count}')
            st.header("Recent News Headlines:")
            st.session_state.news = []
            st.write("Here are the news headlines")
            write_news(np1, performance_df)
            #write_news(np2, performance_df, angle2)
            #write_news(np3, performance_df, angle1)
            # Generate some major random event
        
        if len(st.session_state['minor_events_list']) > 0 and st.session_state.count <= 6:
            rand_event = random.choice(st.session_state['minor_events_list'])
            st.session_state.special_event = minor_events[rand_event][0]
            
            change[minor_events[rand_event][1]] -= st.session_state[minor_events[rand_event][1]][-1] - \
                (st.session_state[minor_events[rand_event][1]][-1]*minor_events[rand_event][2])
            st.session_state['minor_events_list'].remove(rand_event)
            st.session_state.newsprint = True

        if len(st.session_state['major_events_list']) > 0 and st.session_state.count > 6:
            rand_event = random.choice(st.session_state['major_events_list'])
            st.session_state.special_event = major_events[rand_event][0]
            change[major_events[rand_event][1]] -= st.session_state[major_events[rand_event][1]][-1] - \
                (st.session_state[major_events[rand_event][1]][-1]*major_events[rand_event][2])
            st.session_state['major_events_list'].remove(rand_event)
            st.session_state.newsprint = True
        

        if st.session_state.count > 1:
            st.warning(st.session_state.special_event, icon="🌏")
            # Other news
            st.info(st.session_state.messages[0]['content'], icon="📰")
            time.sleep(0.3)
            # st.info(st.session_state.news[1], icon="📰")
            # time.sleep(0.3)
            # st.info(st.session_state.news[2], icon="📰")
            # time.sleep(0.3)



    

    
    




def run_agi():
    st.session_state.locale = en
    if st.session_state.inplay:
        
        

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
                m1.metric("GDP Growth", value=f"{round(st.session_state.final['gdp'],2)}%", delta=f_gdp_change)
                m2.metric("Inflation Rate", value=f"{round(st.session_state.final['inflation'],2)}%", delta=f_inflation_change, delta_color="inverse")
                m3.metric("Government Debt", value=f"{f_govt_debt}", delta=f_govt_debt_change, delta_color="inverse")

                m4, m5, m6 = st.columns((1,1,1))
                m4.metric("National Mean House Price", value=f"{f_house_prices}", delta=f_house_prices_change)
                m5.metric("Unemployment Rate", value=f"{round(st.session_state.final['unemployment'],2)}%", delta=f_unemployment_change, delta_color="inverse")
                m6.metric("Consumer Sentiment", value=f"{round(st.session_state.final['consumer_sentiment'],2)}", delta=f_consumer_sentiment_change)

                m7, m8, m9 = st.columns((1,1,1))
                m7.metric("Imports", value=f"{f_imports}", delta=f_imports_change)
                m8.metric("Exports", value=f"{f_exports}", delta=f_exports_change)
                m9.metric("Stock Market Index", value=round(st.session_state.final['asx_200'],2), delta=f_asx_200_change)
                

            case st.session_state.locale.footer_option2:
                st.header('S&P / ASX 200')
                stock_dir = "Down" if change['asx_200'] < 0 else "Up"
                st.write(f"{stock_dir} {round(change['asx_200'],2)} points ({round(100*(change['asx_200']/st.session_state.final['asx_200']),2)}%) in the past month")
                plot_asx_200(st.session_state['asx_200'][-2], st.session_state.final['asx_200'], 1)
    
    if st.session_state.count > 12:
        selected_footer = option_menu(
        menu_title=None,
        options=[
            st.session_state.locale.footer_option3,
            st.session_state.locale.footer_option4,
            st.session_state.locale.footer_option5,
        ],
        icons=["chat-square-text", "graph-up", "info-circle", ],  # https://icons.getbootstrap.com/
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
        styles=FOOTER_STYLES
        )
        match selected_footer:
            case st.session_state.locale.footer_option3:                
                metric_commentary = []
                # First, iterate through the metrics where the lower is better
                for key, value in st.session_state.initial_values_lowgood.items():
                    if st.session_state.final[key] > max(value[0]*2, value[1]):
                        current_val = st.session_state[key][-1]
                        if key == 'govt_debt':
                            current_val = round(current_val / 1e9)

                        metric_commentary.append(value[4])
                        st.session_state.success = False

                # Next, iterate through the metrics where higher is better 
                for key, value in st.session_state.initial_values_highgood.items():

                    if st.session_state.final[key] < min(value[0]/2, value[1]):
                        current_val = st.session_state[key][-1]
                        if key in ['imports', 'exports']:
                            current_val = round(current_val / 1e9)
                        metric_commentary.append(value[4])
                        st.session_state.success = False
                
                if st.session_state.success == False:
                    st.divider()
                    st.subheader("~~~~~ Letter From The Treasury ~~~~~")
                    st.write("_Dear Governor,_")
                    st.write("_As Treasurer, I must address significant shifts in our economic landscape. Your leadership at the Reserve Bank has been valued, but current \
                            pressures necessitate a change in direction._")
                    for m in metric_commentary:
                        st.write(f"_{m}_")
                    st.write("_At the end of the day, whether or not your decisions are at fault, the Government needs someone to take the fall, and it's been decided that that person is to be you. \
                            While your contributions have been significant, the current political climate demands a reset and a fresh perspective at the helm of our monetary policy._")
                    st.write("_I assure you this transition will be handled with the utmost respect for your tenure and dedication. Your service has been invaluable, and we are committed to supporting your future endeavors. \
                            To this end, I'd be happy to provide a glowing recommend of your services to the Big 4 Banks who will be delighted to speak with you._")
                    st.write("_Thank you for your understanding and cooperation during this period of change._")
                    st.write("_Yours Sincerely,_")
                    st.write("_The Treasurer_")
                else:
                    st.divider()
                    st.subheader("~~~~~ Letter From The Treasury ~~~~~")
                    st.write("_Dear Governor,_")
                    st.write("_I am writing to you today, not only as the Treasurer of Australia but also as a representative of our government, to extend our heartfelt congratulations on completing a \
                             successful first year at the helm of the Reserve Bank of Australia._")
                    st.write("_Over the past 12 months, your leadership and expertise have been instrumental in steering the Australian economy through a complex and ever-evolving landscape. In a period marked by numerous challenges, \
                             both domestically and globally, your prudent management and strategic foresight have been crucial in maintaining economic stability and fostering growth._")
                    st.write("_As we look forward to the coming years, we are confident that under your continued leadership, the Reserve Bank of Australia will remain a pillar of strength and stability for our economy. \
                             The government is committed to supporting the Bank's initiatives and policies that align with our shared goal of a prosperous and resilient Australia._")
                    st.write("_Once again, congratulations on an outstanding first year. We are enthusiastic about what the future holds and the continued positive impact your leadership will bring to our nation's economy._")
                    st.write("_Yours Sincerely,_")
                    st.write("_The Treasurer_")

            case st.session_state.locale.footer_option4:
                plot_final()
            case st.session_state.locale.footer_option5:
                "Text Goes Here"





if __name__ == "__main__":
    run_agi()


# Update previous metrics for the next round

if st.session_state.decision_made and st.session_state.intra_updates: 
    st.session_state['prev_interest_rate'] = st.session_state['interest_rate']
    st.session_state['gdp'][-1] = st.session_state.final['gdp']
    st.session_state['inflation'][-1] = st.session_state.final['inflation']
    st.session_state['unemployment'][-1] = st.session_state.final['unemployment']
    st.session_state['asx_200'][-1] = st.session_state.final['asx_200']
    st.session_state['govt_debt'][-1] = st.session_state.final['govt_debt']
    st.session_state['imports'][-1] = st.session_state.final['imports']
    st.session_state['exports'][-1] = st.session_state.final['exports']
    st.session_state['consumer_sentiment'][-1] = st.session_state.final['consumer_sentiment']
    st.session_state.meeting = False
    st.session_state.decision_made = False 
    st.session_state.intra_updates = False
    clear_chat()  
