# chatterlit
A lightweight Streamlit app for chatting with custom LLMs, simple to run and easy to extend. 

## Prerequisites

- Create `~/.streamlit/config.toml` with content (adjust paths according to your environment):

```
[server]
port = 8501
sslCertFile = '~/streamlit/keys/fullchain.pem'
sslKeyFile = '~/streamlit/keys/privkey.pem'

[browser]
gatherUsageStats = false
```

- Enable password access with `~/.streamlit/secret.toml`:

```
[auth]
password = "MYCOMPLExPASS"
```

- Place your API keys in the file `source-me.sh`
- Enable python virtual environment:

```bash
python3 -mvenv ~/venv/streamlit
source ~/venv/streamlit/bin/activate
# Install streamlit
pip install streamlit
```

## Run 

```bash
. source-me.sh
streamlit run llm-chat.py
```

