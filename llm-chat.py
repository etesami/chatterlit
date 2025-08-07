import streamlit as st
import pandas as pd
from models import MODEL_OPTIONS
from utils import get_content, truncate_message, encode_images, init_client, count_tokens
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

st.title("Chatterlite")

with open('./auth.config.yml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

try:
    authenticator.login()
except Exception as e:
    st.error(e)

if st.session_state.get('authentication_status') is False:
    st.error('Username/password is incorrect')
    st.stop()
elif st.session_state.get('authentication_status') is None:
    st.warning('Please enter your username and password')
    st.stop()


# --- Model Selection ---
with st.expander("See all available models and their descriptions"):
    st.table(pd.DataFrame(MODEL_OPTIONS.items(), columns=["Model Name", "Description"]))

st.session_state.setdefault("chat_history", [])
st.session_state.setdefault("generating", False)

with st.container():
    model_names = list(MODEL_OPTIONS)
    selected_model = st.selectbox("Select Model", model_names, index=model_names.index("gpt-5-mini"))
    col_text = st.columns([4,4])
    with col_text[0]:
        add_short = st.checkbox("Shorter", value=True, help="Generate a short answer instead of a detailed one.")
    with col_text[1]:
        include_history = st.checkbox("History", value=True, help="Include previous messages in the chat history for context.")

input_container = st.container()
with input_container:
    uploaded_images = st.file_uploader("Image(s)", type=["png", "jpg", "jpeg"], accept_multiple_files=True, label_visibility="collapsed")
    # user_input = st.text_area("You:", height=80)  # smaller height to be compact
    user_input = st.chat_input("You:", accept_file=True)  # smaller height to be compact
        
client = init_client(selected_model)

if user_input:
    st.session_state.generating = True
    content = [{"type": "text", "text": user_input.text + (" short answer." if add_short else "")}] + list(encode_images(uploaded_images))
    st.session_state.chat_history = (
        st.session_state.chat_history + [{"role": "user", "content": content}]
        if include_history else [{"role": "user", "content": content}]
    )
    with st.spinner("Generating response..."):
        reply = client.chat.completions.create(
            model=selected_model, messages=st.session_state.chat_history
        ).choices[0].message.content
    st.session_state.chat_history.append({"role": "assistant", "content": reply})
    st.session_state.generating = False

total_tokens = 0
for i, msg in enumerate(st.session_state.chat_history):
    with st.container():
        msg_tokens = count_tokens(msg, selected_model)
        total_tokens += msg_tokens
        if msg["role"] == "user":
            st.markdown(f"**({msg_tokens} tokens, total: {total_tokens})**")
            with st.expander("Show message"):
                st.markdown(get_content(msg))
        else:
            if i < len(st.session_state.chat_history) - 1:
                with st.expander(f"Show response {i}"):
                    st.markdown(get_content(msg))
            else:
                st.markdown(f"{msg['content']}", unsafe_allow_html=True)
        if i % 2 == 1:  # Divider after each Q&A
            st.markdown("---")
