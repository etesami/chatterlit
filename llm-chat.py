import streamlit as st
import pandas as pd
import base64
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from utils import get_content, truncate_message, init_client, count_tokens, process_uploaded_files
from models import MODEL_OPTIONS, MODEL_IMAGES
from prompt import PROMPTS


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
    col_text = st.columns([4,4,4])
    with col_text[0]:
        add_short = st.checkbox("Shorter", value=True, help="Generate a short answer instead of a detailed one.")
    with col_text[1]:
        include_history = st.checkbox("History", value=True, help="Include previous messages in the chat history for context.")
    with col_text[2]:
        include_interactive = st.checkbox("Interactive", value=True, help="Wait for user input after each response.")

input_container = st.container()
with input_container:
    uploaded_images = st.file_uploader("Image(s)", type=["png", "jpg", "jpeg", "txt"], accept_multiple_files=True, label_visibility="collapsed")
    # user_input = st.text_area("You:", height=80)  # smaller height to be compact
    user_input = st.chat_input("You:", accept_file=True)  # smaller height to be compact
        
client = init_client(selected_model)

if user_input:
    st.session_state.generating = True
    content = [{
        "type": "text", 
        "text": user_input.text + 
            (" short answer." if add_short else "") + 
            (PROMPTS["interactive"] if include_interactive else "") +
            PROMPTS["code_block"]
    }] + process_uploaded_files(uploaded_images)
    st.session_state.chat_history = (
        st.session_state.chat_history + [{"role": "user", "content": content}]
        if include_history else [{"role": "user", "content": content}]
    )
    if selected_model not in MODEL_IMAGES:
        with st.spinner("Generating response..."):
            reply = client.chat.completions.create(
                model=selected_model, messages=st.session_state.chat_history
            ).choices[0].message.content
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
    else:
        with st.spinner("Generating image..."):
            latest_message = st.session_state.chat_history[-1]["content"][0]["text"]
            response = client.images.generate(
                model=selected_model, prompt=latest_message, n=1, size="1024x1024"
            )
            image_bytes = base64.b64decode(response.data[0].b64_json)
        st.session_state.chat_history.append({"role": "assistant", "content": image_bytes, "is_image": True})
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
                if msg.get("is_image"):
                    st.image(msg["content"])
                else:
                    st.markdown(f"{msg['content']}", unsafe_allow_html=True)
        if i % 2 == 1:  # Divider after each Q&A
            st.markdown("---")
