# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the vLLM project
"""
Chatterlite - Streamlit Chat Interface (merged style)

This file adopts the layout/style and session management of the
vLLM example while integrating the features and utilities of the
original Chatterlite app (authentication, model selection,
file uploads, token counting, image generation support, etc).

Features:
- Authentication (streamlit_authenticator)
- Multi-chat-session management (create / switch sessions)
- Model selection and options in the sidebar (sidecar area)
- File upload support (images / tex / txt)
- Token counting and per-message display
- Image generation support for image-capable models
- Preserves original message structure and session persistence

Note: This code expects the same helper modules/constants used
in the original Chatterlite code to be available:
  - utils: get_content, truncate_message, init_client, count_tokens, process_uploaded_files
  - models: MODEL_OPTIONS, MODEL_IMAGES
  - prompt: PROMPTS
  - auth.config.yml file for streamlit_authenticator
"""
import os
from datetime import datetime

import streamlit as st
import pandas as pd
import base64
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth

from utils import get_content, truncate_message, init_client, count_tokens, process_uploaded_files
from models import MODEL_OPTIONS, MODEL_IMAGES
from prompt import PROMPTS

# -------------------------
# Authentication
# -------------------------
st.set_page_config(page_title="Chatterlite", layout="wide")
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

# -------------------------
# Session management (vLLM style)
# -------------------------
if "sessions" not in st.session_state:
    st.session_state.sessions = {}  # mapping session_id -> messages list

if "current_session" not in st.session_state:
    st.session_state.current_session = None

if "messages" not in st.session_state:
    # messages is the active session's message list.
    st.session_state.messages = []

if "active_session" not in st.session_state:
    st.session_state.active_session = None

# Generation flag used by UI
if "generating" not in st.session_state:
    st.session_state.generating = False

# show_reasoning kept for compatibility with the vLLM style (unused here)
if "show_reasoning" not in st.session_state:
    st.session_state.show_reasoning = {}

# -------------------------
# Helper session functions
# -------------------------
def create_new_chat_session():
    session_id = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.sessions[session_id] = []
    st.session_state.current_session = session_id
    st.session_state.active_session = session_id
    st.session_state.messages = []

def switch_to_chat_session(session_id):
    st.session_state.current_session = session_id
    st.session_state.active_session = session_id
    st.session_state.messages = st.session_state.sessions.get(session_id, [])

# Initialize first session if none exists
if st.session_state.current_session is None:
    create_new_chat_session()
    st.session_state.active_session = st.session_state.current_session

# -------------------------
# Sidebar / Model selection (acts as "sidecar")
# -------------------------
st.sidebar.title("Model & Options")

# Show models table in an expander
# with st.sidebar.expander("See all available models and their descriptions", expanded=False):
#     st.table(pd.DataFrame(MODEL_OPTIONS.items(), columns=["Model Name", "Description"]))

# Model selection
model_names = list(MODEL_OPTIONS.keys())
default_index = model_names.index("gpt-image-1-mini") if "gpt-image-1-mini" in model_names else 0
selected_model = st.sidebar.selectbox("Select Model", model_names, index=default_index)

# Option toggles
include_short = st.sidebar.checkbox("Shorter", value=False, help="Generate a short answer instead of a detailed one.")
# include_history = st.sidebar.checkbox("History", value=True, help="Include previous messages in the chat history for context.")
include_interactive = st.sidebar.checkbox("Interactive", value=False, help="Wait for user input after each response.")
include_jobs = st.sidebar.checkbox("Jobs", value=False, help="Adjust job titles to better fit the job description.")
include_image = st.sidebar.checkbox("Infographic", value=True, help="Create an infographic from the text.")
include_code_block = st.sidebar.checkbox("Code Block", value=False, help="Add a code block to the response.")

st.sidebar.divider()
# st.sidebar.title("Chat Sessions")
# if st.sidebar.button("New Session"):
#     create_new_chat_session()

# Display all sessions in the sidebar in reverse chronological order
for session_id in sorted(st.session_state.sessions.keys(), reverse=True):
    if session_id == st.session_state.active_session:
        st.sidebar.button(
            f"📍 {session_id}",
            key=f"session_pin_{session_id}",
            type="primary",
            on_click=switch_to_chat_session,
            args=(session_id,),
        )
    else:
        st.sidebar.button(
            f"Session {session_id}",
            key=f"session_btn_{session_id}",
            on_click=switch_to_chat_session,
            args=(session_id,),
        )

# -------------------------
# Initialize client for selected model
# -------------------------
client = init_client(selected_model)

# -------------------------
# Main UI - message display and input
# -------------------------
# Show active model at top of page
st.markdown(f"**Model:** {selected_model}")

# Uploaded files / images
uploaded_files = st.file_uploader("Files/Images", type=["tex", "png", "jpg", "jpeg", "txt"], accept_multiple_files=True)

# Chat input
prompt = st.chat_input("You:")
text_piece = None

# When user submits a message
if prompt:
    st.session_state.generating = True

    # Build the message content in the same shape as the original Chatterlite expects
    # text content is built from the prompt + options/prompts
    if include_image:
        text_piece = PROMPTS["image"] + prompt

    if text_piece is None:
        text_piece = prompt

    if include_short:
        text_piece = text_piece + " short answer."
    if include_interactive:
        text_piece = text_piece + PROMPTS["interactive"]
    if include_jobs:
        text_piece = text_piece + PROMPTS["jobs"]
    if include_code_block:
        text_piece = text_piece + PROMPTS["code_block"]
    
    content = [{"type": "text", "text": text_piece}] + process_uploaded_files(uploaded_files)

    # Update messages list depending on include_history
    st.session_state.messages = st.session_state.messages + [{"role": "user", "content": content}]
    
    # Persist session messages into sessions store
    st.session_state.sessions[st.session_state.current_session] = st.session_state.messages

    # Echo the user message in the UI
    # with st.chat_message("user"):
    #     # get_content knows how to render the structured content
    #     st.markdown(get_content(st.session_state.messages[-1]), unsafe_allow_html=True)

    # Generate assistant reply (image or text)
    if selected_model not in MODEL_IMAGES:
        with st.spinner("Generating response..."):
            try:
                # The original client usage expected messages in their structured format,
                # we pass the session messages as-is.
                response = client.chat.completions.create(
                    model=selected_model,
                    messages=st.session_state.messages
                )
                # Extract text content; adjust depending on client return shape
                reply_text = None
                # Try common shapes
                if hasattr(response, "choices"):
                    choice = response.choices[0]
                    # Some clients return message.content as attribute
                    if hasattr(choice, "message") and hasattr(choice.message, "content"):
                        reply_text = choice.message.content
                    # Or choices[0].text
                    elif hasattr(choice, "text"):
                        reply_text = choice.text
                # Fallback
                if reply_text is None:
                    # try dictionary-like access
                    try:
                        reply_text = response["choices"][0]["message"]["content"]
                    except Exception:
                        reply_text = str(response)
            except Exception as e:
                reply_text = f"Error: {e}"

        # Append assistant message
        st.session_state.messages.append({"role": "assistant", "content": reply_text})
        st.session_state.sessions[st.session_state.current_session] = st.session_state.messages

        # # Display assistant answer
        # with st.chat_message("assistant"):
        #     st.markdown(reply_text, unsafe_allow_html=True)
    else:
        # Image generation path
        with st.spinner("Generating image..."):
            latest_message_text = st.session_state.messages[-1]["content"][0]["text"]
            response = client.images.generate(
                model=selected_model, prompt=latest_message_text, n=1, size="1024x1024"
            )
            image_b64 = response.data[0].b64_json
            image_bytes = base64.b64decode(image_b64)

        st.session_state.messages.append({"role": "assistant", "content": image_bytes, "is_image": True})
        st.session_state.sessions[st.session_state.current_session] = st.session_state.messages

        # with st.chat_message("assistant"):
        #     st.image(image_bytes)

    st.session_state.generating = False

# -------------------------
# Display chat history for active session
# -------------------------
st.markdown("---")
# st.header("Conversation")

total_tokens = 0
for i, msg in enumerate(st.session_state.messages):
    # Count tokens for this message
    try:
        msg_tokens = count_tokens(msg, selected_model)
    except Exception:
        # If the token counter fails, fallback to 0
        msg_tokens = 0
    total_tokens += msg_tokens

    if msg["role"] == "user":
        with st.container():
            st.markdown(f"**User ({msg_tokens} tokens, total: {total_tokens})**")
            with st.expander("Show message", expanded=False):
                st.markdown(get_content(msg), unsafe_allow_html=True)
    else:
        # Assistant messages: for every previous assistant message show it inside an expander
        with st.container():
            if i < len(st.session_state.messages) - 1:
                with st.expander(f"Show response {i}", expanded=False):
                    # Assistant content can be simple text, or structured, or bytes for images
                    if msg.get("is_image"):
                        st.image(msg["content"])
                    else:
                        st.markdown(msg["content"], unsafe_allow_html=True)
            else:
                # Last assistant message shown directly
                if msg.get("is_image"):
                    st.image(msg["content"])
                else:
                    st.markdown(msg["content"], unsafe_allow_html=True)

    # Divider after each Q&A pair (user followed by assistant)
    if i % 2 == 1:
        st.markdown("---")

# End of file
