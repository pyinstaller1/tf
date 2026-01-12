import os
import time
import json
import requests
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

APP_KEY = os.getenv("LS_APP_KEY")
APP_SECRET = os.getenv("LS_APP_SECRET")

BASE_DIR = Path(__file__).resolve().parent
TOKEN_FILE = BASE_DIR / "token.json"

def load_token():
    if TOKEN_FILE.exists():
        with open(TOKEN_FILE, "r") as f:
            return json.load(f)
    return None

def save_token(data):
    with open(TOKEN_FILE, "w") as f:
        json.dump(data, f)

def is_expired(token_data):
    return time.time() > token_data["expires_at"]

def create_token():
    url = "https://openapi.ls-sec.co.kr:8080/oauth2/token"
    payload = {
        "grant_type": "client_credentials",
        "appkey": APP_KEY,
        "appsecret": APP_SECRET
    }
    headers = {"Content-Type": "application/json"}
\
    r = requests.post(url, json=payload, headers=headers)
    data = r.json()

    access_token = data["access_token"]
    expires_in = data["expires_in"]  # 보통 3600초
    expires_at = time.time() + expires_in - 5

    token_data = {
        "access_token": access_token,
        "expires_at": expires_at
    }
    save_token(token_data)

    return access_token

def get_token():
    token_data = load_token()

    if token_data and not is_expired(token_data):
        return token_data["access_token"]

    return create_token()
