import streamlit as st
import pandas as pd
from models import MODEL_OPTIONS
from utils import get_content, truncate_message, encode_images, init_client, count_tokens


st.title("Chatterlite")

# --- Authentication ---
if not st.session_state.get("authenticated", False):
    if st.text_input("Enter password", type="password") == st.secrets.auth.password:
        st.session_state.authenticated = True
        st.rerun()
    st.error("Wrong password")
    st.stop()


# --- Model Selection ---
with st.expander("See all available models and their descriptions"):
    st.table(pd.DataFrame(MODEL_OPTIONS.items(), columns=["Model Name", "Description"]))

model_names = list(MODEL_OPTIONS)
selected_model = st.selectbox("Select Model", model_names, index=model_names.index("gpt-4.1-mini"))

client = init_client(selected_model)

add_short = st.checkbox("Short answer", value=True)
include_history = st.checkbox("Include history", value=True)

st.session_state.setdefault("chat_history", [])
st.session_state.setdefault("generating", False)

user_input = st.text_area("You:")
uploaded_images = st.file_uploader("Attach image(s) (optional)", type=["png", "jpg", "jpeg"], accept_multiple_files=True)


if st.button("Send", disabled=st.session_state.generating) and user_input:
    st.session_state.generating = True
    content = [{"type": "text", "text": user_input + (" short answer." if add_short else "")}] + list(encode_images(uploaded_images))
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
            st.markdown(f"{msg['content']}")
        if i % 2 == 1:  # Divider after each Q&A
            st.markdown("---")

