from random import randrange

import streamlit as st
from openai import InvalidRequestError, OpenAIError
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


def show_gpt_conversation(bm) -> None:
    try:
        completion = loading_data(st.session_state.model, st.session_state[bm])
        ai_content = completion.get("choices")[0].get("message").get("content")
        #calc_cost(completion.get("usage"))
        st.session_state[bm].append({"role": "assistant", "content": ai_content})
        if ai_content:
            show_chat(ai_content)
    except InvalidRequestError as err:
        if err.code == "context_length_exceeded":
            st.session_state[bm].pop(1)
            if len(st.session_state[bm]) == 1:
                st.session_state.user_text = ""
            show_conversation()
        else:
            st.error(err)
    except (OpenAIError, UnboundLocalError) as err:
        st.error(err)

def show_gpt_conversation2() -> None:
    try:
        completion = loading_data(st.session_state.model, st.session_state.messages)
        ai_content = completion.get("choices")[0].get("message").get("content")
        #calc_cost(completion.get("usage"))
        st.session_state.messages.append({"role": "assistant", "content": ai_content})
        if ai_content:
            show_chat(ai_content)
    except InvalidRequestError as err:
        if err.code == "context_length_exceeded":
            st.session_state.messages.pop(1)
            if len(st.session_state.messages) == 1:
                st.session_state.user_text = ""
            show_conversation2()
        else:
            st.error(err)
    except (OpenAIError, UnboundLocalError) as err:
        st.error(err)    

def show_gpt_conversation3() -> None:
    try:
        completion = loading_data(st.session_state.model, st.session_state.messages)
        ai_content = completion.get("choices")[0].get("message").get("content")
        #calc_cost(completion.get("usage"))
        st.session_state.messages.append({"role": "assistant", "content": ai_content})
        if ai_content:
            show_chat2(ai_content)
    except InvalidRequestError as err:
        if err.code == "context_length_exceeded":
            st.session_state.messages.pop(1)
            if len(st.session_state.messages) == 1:
                st.session_state.user_text = ""
            show_conversation()
        else:
            st.error(err)
    except (OpenAIError, UnboundLocalError) as err:
        st.error(err)




def show_conversation(ai_role, economic_data, bm) -> None:
    if st.session_state[bm]:
        st.session_state[bm].append({"role": "user", "content": f'Given the following metrics: {economic_data}, what is your recommentation? Comment on 2-3 key metrics in your response' })
    else:        
        st.session_state[bm] = [
            {"role": "system", "content": ai_role},
            {"role": "user", "content": f'Given the following metrics: {economic_data}, what is your recommentation? Comment on 2-3 key metrics in your response'},
        ]
    show_gpt_conversation(bm)

def show_conversation2(ai_role) -> None:
    st.session_state.messages.append({"role": "user", "content": f'You strongly disagree with the previous advice and refute where possible. Choose different economic metrics to focus on in your response. {ai_role}'})
    
    show_gpt_conversation2()

def write_news(ai_role, economic_data, decision=None) -> None:
    if st.session_state.messages:
        st.session_state.messages.append({"role": "user", "content": f'Write a single headline for your publication: {ai_role} using the one of the following metrics: {economic_data}. Also consider {decision}' })
    else:        
        st.session_state.messages = [
            {"role": "system", "content": ai_role},
            {"role": "user", "content": f'Write a single headline for your publication: {ai_role}, using one of the following metrics: {economic_data}. Also consider {decision}' },
        ]
    show_gpt_conversation3()






