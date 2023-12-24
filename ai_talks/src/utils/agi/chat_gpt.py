import logging
from typing import List  # NOQA: UP035

from openai import OpenAI
import streamlit as st
client = OpenAI(api_key=st.secrets.api_credentials.api_key)
#client = OpenAI(
    # This is the default and can be omitted
#    api_key=os.environ.get("OPENAI_API_KEY"),
#)



@st.cache_data()
def loading_data(ai_model: str, messages: List[dict]) -> dict:

    logging.info(f"{messages=}")
    chat_completion = client.chat.completions.create(
        messages=messages,
        model="gpt-3.5-turbo",
    )
    logging.info(f"{chat_completion=}")
    return chat_completion

    
