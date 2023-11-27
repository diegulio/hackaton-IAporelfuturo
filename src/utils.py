import json
import os
import re
from typing import Dict, List

import requests
from dotenv import load_dotenv

load_dotenv()

CODEGPT_APIKEY = os.getenv("CODEGPT_API_KEY")
AGENT_CALCULADORA_ID = os.getenv("AGENT_CALCULADORA_ID")
AGENT_MITIGADOR_ID = os.getenv("AGENT_MITIGADOR_ID")
AGENT_DISCRIMINADOR_ID = os.getenv("AGENT_DISCRIMINADOR_ID")
COMPLETION_URL = f"https://api.codegpt.co/v1/completion"


# This code is in major part from CodeGPT's documentation cookbook
# https://github.com/JudiniLabs/cookbook/tree/main
def agent(messages: List[Dict], agent_id: str):
    """Get completion for a conversation from an agent in CodeGPT plus

    Args:
        messages (List[Dict]): List of messages
        agent_id (str): Agent Id from CodeGPT Plus

    """
    headers = {"Authorization": f"Bearer {CODEGPT_APIKEY}"}
    body = {
        "agent": agent_id,
        "messages": messages,
    }
    completion_call = requests.post(COMPLETION_URL, json=body, headers=headers)
    if completion_call.status_code == 200:
        return parse_completion_response(completion_call.text)
    else:
        return f"Error, {json.loads(completion_call.text)['detail']}"


# COMPLETION FUNCTION
def parse_completion_response(completion_text):
    """
    Auxiliar function to format response from CodeGPT agents
    """
    pattern = r"data: (.+)"
    matches = re.findall(pattern, completion_text)
    completion = "".join(matches)
    return completion
