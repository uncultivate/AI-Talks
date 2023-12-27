from random import randrange

import streamlit as st
from streamlit_chat import message

from .agi.chat_gpt import loading_data



def clear_chat() -> None:
    st.session_state.generated = []
    st.session_state.past = []
    st.session_state.messages = []
    st.session_state.bm1 = []
    st.session_state.bm2 = []
    st.session_state.bm3 = []
    st.session_state.user_text = ""
    st.session_state.seed = randrange(10**8)  # noqa: S311
    st.session_state.costs = []
    st.session_state.total_tokens = []


def show_chat_buttons() -> None:
    b0, b1, b2 = st.columns(3)
    with b0, b1, b2:
        b0.button(label=st.session_state.locale.chat_run_btn)
        b1.button(label=st.session_state.locale.chat_clear_btn, on_click=clear_chat)
        b2.download_button(
            label=st.session_state.locale.chat_save_btn,
            data="\n".join([str(d) for d in st.session_state.messages[1:]]),
            file_name="ai-talks-chat.json",
            mime="application/json",
        )


def show_chat(ai_content: str) -> None:
    if ai_content not in st.session_state.generated:
        st.session_state.generated.append(ai_content)

def show_chat2(ai_content: str) -> None:
    if ai_content not in st.session_state.generated:
        # store the ai content
        st.session_state.news.append(ai_content)

def extract_message_content(chat_completion):
    messages = []
    for choice in chat_completion.choices:
        messages.append(choice.message.content)
    return messages


def show_gpt_conversation(bm) -> None:

    completion = loading_data(st.session_state.model, st.session_state[bm])
    extracted_messages = extract_message_content(completion)
    #calc_cost(completion.get("usage"))
    st.session_state[bm].append({"role": "assistant", "content": extracted_messages})
    if extracted_messages:
        show_chat(extracted_messages)
   
   

def show_gpt_conversation2() -> None:
    completion = loading_data(st.session_state.model, st.session_state.prompt)
    extracted_messages = extract_message_content(completion)
    #calc_cost(completion.get("usage"))
    #st.session_state.messages.append({"role": "assistant", "content": ai_content})
    if extracted_messages:
        show_chat(extracted_messages)
   

def show_gpt_conversation3() -> None:
    completion = loading_data(st.session_state.model, st.session_state.prompt)
    extracted_messages = extract_message_content(completion)
    st.session_state.messages.append({"role": "assistant", "content": extracted_messages})
    if extracted_messages:
        show_chat2(extracted_messages)


def show_conversation(ai_role, economic_data, bm) -> None:
    if st.session_state[bm]:
        st.session_state[bm].append({"role": "user", "content": f'Given the following metrics: {economic_data}, what is your recommentation? Comment on 2-3 key metrics in your response' })
    else:        
        st.session_state[bm] = [
            {"role": "system", "content": ai_role},
            {"role": "user", "content": f'Given the following metrics: {economic_data}, what is your recommentation? Comment on 2-3 key metrics in your response'},
        ]
    show_gpt_conversation(bm)


def write_news(ai_role, economic_data, decision=None) -> None:
    if st.session_state.prompt:
        st.session_state.prompt.append({"role": "user", "content": f'Write a single headline for your publication: {ai_role} using the one of the following metrics: {economic_data}. Also consider {decision}' })
    else:        
        st.session_state.prompt = [
            {"role": "system", "content": ai_role},
            {"role": "user", "content": f'Write a single headline for your publication: {ai_role}, using one of the following metrics: {economic_data}. Also consider {decision}' },
        ]
    show_gpt_conversation3()






