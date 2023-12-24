import logging
from typing import List  # NOQA: UP035

from openai import OpenAI_API_Client, OpenAI_Error
import streamlit as st
client = OpenAI(api_key=st.secrets.api_credentials.api_key)
#client = OpenAI(
    # This is the default and can be omitted
#    api_key=os.environ.get("OPENAI_API_KEY"),
#)



@st.cache_data()
def loading_data(ai_model: str, messages: List[dict]) -> dict:
    try:
            # Check if image processing is required
            model = ai_model

            completion = client.chat_completions.create(model=model, messages=messages)

        except (KeyError, AttributeError, OpenAI_Error) as error:
            # Handle specific errors (e.g., API errors, attribute errors)
            logging.error(f"Error loading data: {error}")
            raise

        logging.info(f"Loaded data with {messages=}")
        logging.info(f"{completion=}")

        return completion
