import ast
import os

import streamlit as st
from dotenv import load_dotenv

from src.utils import agent

# from dotenv import load_dotenv  # For loading environment variables from a .env file
load_dotenv()

CODEGPT_APIKEY = os.getenv("CODEGPT_API_KEY")
AGENT_CALCULADORA_ID = os.getenv("AGENT_CALCULADORA_ID")
AGENT_MITIGADOR_ID = os.getenv("AGENT_MITIGADOR_ID")
AGENT_DISCRIMINADOR_ID = os.getenv("AGENT_DISCRIMINADOR_ID")
COMPLETION_URL = f"https://api.codegpt.co/v1/completion"


def app():
    st.title("♻️ EcoTracker")
    st.write(
        "EcoTracker es un chatbot🤖 que te ayuda a calcular tu huella de carbono y te da consejos para mitigarla."
    )

    # Flag for change agent
    if "flag" not in st.session_state:
        st.session_state["flag"] = False

    # messages history
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    # Current agent id
    AGENT_ID = (
        AGENT_CALCULADORA_ID if not (st.session_state["flag"]) else AGENT_MITIGADOR_ID
    )

    prompt = st.chat_input("Ask something")
    if prompt:
        # save prompt and answer in messages
        st.session_state["messages"].append({"role": "user", "content": prompt})
        answer = agent(st.session_state["messages"], AGENT_ID)
        st.session_state["messages"].append({"role": "assistant", "content": answer})

        # If flag = False -> Discriminator agent should decide if
        # answer requirements are satisfied
        if st.session_state["flag"] == False:
            f = agent(st.session_state["messages"], AGENT_DISCRIMINADOR_ID)
            # if discriminator answer is a list -> we pass to mitigador agent
            # TODO: use isinstance(list)
            try:
                resultado = ast.literal_eval(f)
                st.session_state["flag"] = True
            # if not, we continue with calculadora agent
            except:
                pass

        # Load History messages (this includes the answer)
        for message in st.session_state["messages"]:
            if message["role"] == "user":
                with st.chat_message("user"):
                    st.write(message["content"])
            elif message["role"] == "assistant":
                with st.chat_message("assistant", avatar="🤖"):
                    st.write(message["content"])
