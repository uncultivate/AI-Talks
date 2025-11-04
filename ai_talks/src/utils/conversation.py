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
    """Store AI content in generated list. Accepts string or list and normalizes to string."""
    if isinstance(ai_content, list):
        # If it's a list, take the first element
        ai_content = ai_content[0] if ai_content else ""
    
    # Initialize generated if it doesn't exist
    if 'generated' not in st.session_state:
        st.session_state.generated = []
    
    if ai_content and ai_content not in st.session_state.generated:
        st.session_state.generated.append(ai_content)
        import logging
        logging.info(f"show_chat: appended content, generated list now has {len(st.session_state.generated)} items")

def show_chat2(ai_content: str) -> None:
    """Store AI content in news list. Accepts string or list and normalizes to string."""
    if isinstance(ai_content, list):
        # If it's a list, take the first element
        ai_content = ai_content[0] if ai_content else ""
    
    if ai_content and ai_content not in st.session_state.generated:
        # store the ai content
        st.session_state.news.append(ai_content)

def extract_message_content(chat_completion):
    """Extract message content from chat completion. Returns the first choice's content as a string."""
    import logging
    
    if not chat_completion:
        logging.warning("extract_message_content: chat_completion is None")
        return None
    
    if not hasattr(chat_completion, 'choices'):
        logging.warning(f"extract_message_content: chat_completion has no 'choices' attribute. Type: {type(chat_completion)}")
        return None
    
    if not chat_completion.choices:
        logging.warning("extract_message_content: chat_completion.choices is empty")
        return None
    
    choice = chat_completion.choices[0]
    if not hasattr(choice, 'message'):
        logging.warning(f"extract_message_content: choice has no 'message' attribute. Choice: {choice}")
        return None
    
    content = choice.message.content
    if content is None or content == '':
        # Check if finish_reason indicates why content is empty
        finish_reason = getattr(choice, 'finish_reason', None)
        if finish_reason == 'length':
            logging.warning(f"extract_message_content: content is empty due to length limit (finish_reason='length'). "
                          f"Consider increasing max_completion_tokens. Usage: {getattr(chat_completion, 'usage', 'N/A')}")
        else:
            logging.warning(f"extract_message_content: message.content is empty or None. "
                          f"Finish reason: {finish_reason}, Message: {choice.message}")
        return None
    
    logging.info(f"extract_message_content: successfully extracted content of length {len(content)}")
    return content


def show_gpt_conversation(bm) -> None:
    """Get GPT response and store it in session state."""
    import logging
    
    try:
        logging.info(f"show_gpt_conversation for {bm}: calling loading_data with model={st.session_state.model}, messages count={len(st.session_state[bm])}")
        completion = loading_data(st.session_state.model, st.session_state[bm])
        logging.info(f"show_gpt_conversation for {bm}: completion received, type={type(completion)}")
        
        # Log completion structure for debugging
        if hasattr(completion, 'choices'):
            logging.info(f"show_gpt_conversation for {bm}: completion has {len(completion.choices)} choices")
            if completion.choices:
                logging.info(f"show_gpt_conversation for {bm}: first choice type={type(completion.choices[0])}, has message={hasattr(completion.choices[0], 'message')}")
        
        content = extract_message_content(completion)
        
        logging.info(f"show_gpt_conversation for {bm}: content extracted = {bool(content)}, length = {len(content) if content else 0}")
        
        if content:
            # Store the content as a string in the conversation history
            st.session_state[bm].append({"role": "assistant", "content": content})
            # Also store in generated list for UI display
            show_chat(content)
            logging.info(f"show_gpt_conversation for {bm}: stored in generated, count = {len(st.session_state.generated)}")
        else:
            logging.warning(f"show_gpt_conversation for {bm}: no content extracted from completion. Completion object: {completion}")
    except Exception as e:
        logging.exception(f"Error in show_gpt_conversation for {bm}: {e}")
        raise
    
    st.session_state.prompt = []
   
   

def show_gpt_conversation2() -> None:
    completion = loading_data(st.session_state.model, st.session_state.prompt)
    content = extract_message_content(completion)
    #calc_cost(completion.get("usage"))
    if content:
        show_chat(content)
    st.session_state.prompt = []
   

def show_gpt_conversation3() -> None:
    completion = loading_data(st.session_state.model, st.session_state.prompt)
    content = extract_message_content(completion)
    if content:
        st.session_state.messages.append({"role": "assistant", "content": content})
        show_chat2(content)
    st.session_state.prompt = []


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






