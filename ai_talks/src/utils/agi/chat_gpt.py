import logging
from typing import List  # NOQA: UP035

import openai
import streamlit as st


@st.cache_data()
def loading_data(ai_model: str, messages: List[dict]) -> dict:
    try:
        #openai.api_key = st.secrets.api_credentials.api_key
        openai.api_key = "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"
    except (KeyError, AttributeError):
        st.error(st.session_state.locale.empty_api_handler)
    logging.info(f"{messages=}")
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        # stream=True,
        # temperature=0.7,
    )
    logging.info(f"{completion=}")
    return completion
