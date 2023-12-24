import logging
from typing import List  # NOQA: UP035

from openai import OpenAI

client = OpenAI(api_key=st.secrets.api_credentials.api_key)
import streamlit as st


@st.cache_data()
def loading_data(ai_model: str, messages: List[dict]) -> dict:
    try:
    except (KeyError, AttributeError):
        st.error(st.session_state.locale.empty_api_handler)
    logging.info(f"{messages=}")
    completion = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=messages)
    logging.info(f"{completion=}")
    return completion
